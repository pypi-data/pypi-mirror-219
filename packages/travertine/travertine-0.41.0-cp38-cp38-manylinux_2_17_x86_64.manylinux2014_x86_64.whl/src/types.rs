use core::convert::TryFrom;
use pyo3::class::basic::CompareOp;
use pyo3::prelude::*;
use pyo3::types::{
    PyDateAccess, PyDateTime, PyDelta, PyDeltaAccess, PyFloat, PyLong, PyString, PyTimeAccess,
    PyTuple, PyType,
};
use time::macros::*;

use lazy_static::lazy_static;
use regex::Regex;
use std::convert::TryInto;
use std::str::FromStr;

use travertine::totalize::Totalized;
use travertine_runtime as travertine;

#[derive(Clone, Debug, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub(crate) struct TravertinePyTypes;
impl travertine::types::TravertineTypes for TravertinePyTypes {
    type DateTime = BareDateTime;
    type Duration = BareTimeDelta;

    // TODO: Switch to an id-based attribute type.
    type AttrId = String;
    type VariableName = String;

    type CustomValue = TypedValue;

    fn resolve_variable_name(s: &str) -> Self::VariableName {
        s.to_string()
    }
}

macro_rules! is_instance {
    ($type: ty, $ob: expr) => {
        $ob.is_instance_of::<$type>()
    };
}

/// The values which can be used in programs as arguments to predicates.
///
/// This type implements [FromPyObject] so that suitable Python values are
/// converted seamlessly.  Values can be numbers which should fit in a f64,
/// strings, datetime, and timedelta and [ExternalObject](external objects)
/// which are basically objects which live in an external namespace and have an
/// u64 identifier.
#[derive(PartialOrd, PartialEq, Eq, Ord, Clone, Debug)]
pub(crate) enum TypedValue {
    Number(Totalized<f64>),
    Str(String),
    Duration(BareTimeDelta),
    DateTime(BareDateTime),

    Reference(ExternalObject),
}

impl TryInto<f64> for TypedValue {
    type Error = &'static str;
    fn try_into(self) -> Result<f64, Self::Error> {
        match self {
            Self::Number(t) => Ok(t.item),
            _ => Err("Impossible to convert a non-number typed value to f64"),
        }
    }
}

impl<'source> FromPyObject<'source> for TypedValue {
    fn extract(ob: &'source PyAny) -> PyResult<Self> {
        if is_instance!(PyTuple, ob) {
            Ok(Self::Reference(ExternalObject::from_tuple(
                ob.get_type(), // FIXME: find the actual type
                ob,
            )?))
        } else if is_instance!(ExternalObject, ob) {
            Ok(Self::Reference(ob.extract()?))
        } else if is_instance!(PyFloat, ob) || is_instance!(PyLong, ob) {
            Ok(Self::Number(ob.extract::<f64>()?.into()))
        } else if is_instance!(PyDelta, ob) {
            Ok(Self::Duration(ob.extract()?))
        } else if is_instance!(PyDateTime, ob) {
            Ok(Self::DateTime(ob.extract()?))
        } else if is_instance!(PyString, ob) {
            Ok(Self::Str(ob.extract()?))
        } else {
            Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(format!(
                "Invalid type as typed value in programs '{}'",
                ob.get_type().name().unwrap_or_default()
            )))
        }
    }
}

impl IntoPy<PyObject> for TypedValue {
    fn into_py(self, py: Python) -> PyObject {
        match self {
            TypedValue::Number(n) => {
                let r: f64 = n.into();
                r.to_object(py)
            }
            TypedValue::Str(s) => s.to_object(py),
            TypedValue::Duration(d) => d.to_object(py),
            TypedValue::DateTime(d) => d.to_object(py),
            TypedValue::Reference(r) => r.into_py(py),
        }
    }
}

/// External objects represent values which live in an external namespace (like
/// the Odoo model namespace) and have a identifiers or type [`u64`].
#[pyclass(subclass, module = "travertine")]
#[derive(PartialEq, PartialOrd, Eq, Ord, Clone, Debug)]
pub(crate) struct ExternalObject {
    name: String,
    id: u64,
}

#[pymethods]
impl ExternalObject {
    #[new]
    fn new(name: String, id: u64) -> Self {
        Self { name, id }
    }

    /// Create an external object from a tuple of `(name, id)`.
    #[classmethod]
    fn from_tuple(_cls: &PyType, ob: &PyAny) -> PyResult<Self> {
        if is_instance!(PyTuple, ob) {
            let tuple: &PyTuple = ob.downcast()?;
            if tuple.len() == 2 {
                let name: String = tuple.get_item(0)?.extract()?;
                let id: u64 = tuple.get_item(1)?.extract()?;
                return Ok(Self { name, id });
            }
            Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(
                "Expected a tuple with exactly two items",
            ))
        } else {
            Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
                "Expected a tuple with exactly two items",
            ))
        }
    }

    /// Create an external object from a string with format `(name, id)` -- the
    /// parenthesis are optional, but they MUST match if present.
    #[classmethod]
    fn from_reference_string(_cls: &PyType, ob: &PyAny) -> PyResult<Self> {
        if is_instance!(PyString, ob) {
            let mut reference: &str = ob.extract()?;
            if reference.starts_with('(') && reference.ends_with(')') {
                reference = &reference[1..reference.len() - 1]
            }
            lazy_static! {
                static ref RE: Regex =
                    Regex::new(r"(?P<name>[\w\._\-\d]+)\s*,\s*(?P<id>\d+)").unwrap();
            }
            if let Some(captures) = RE.captures(reference) {
                let name = captures.get(1).unwrap().as_str().to_string();
                let id: u64 = u64::from_str(captures.get(2).unwrap().as_str()).unwrap();
                return Ok(Self { name, id });
            }
        }
        Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(format!(
            "Expected a string with the format `(name, id)`, got '{}'",
            ob.to_string()
        )))
    }

    fn __richcmp__(&self, other: Self, op: CompareOp) -> PyResult<bool> {
        match op {
            CompareOp::Eq => Ok(self.name == other.name && self.id == other.id),
            CompareOp::Ne => Ok(!(self.name == other.name && self.id == other.id)),
            _ => Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(format!(
                "Invalid cmp operator {:?}",
                op
            ))),
        }
    }
}

// We can't use PyO3's PyDateTime and PyDelta directly because the are meant
// to reflect 1:1 the Python's structures with vtables and all the complexity
// they have but we don't need.  That's why we introduce some *bare*
// (data-only) structs.

/// A data-carrying wrapper for Python's *non tz-aware* datetime.
///
/// We implement FromPyObject so that Python's datetime can be converted to
/// this type.  This type implements the required traits of
/// [travertine::types::TravertineTypes::DateTime].
#[derive(PartialEq, Debug, Clone, Ord, Eq, PartialOrd, Copy)]
pub struct BareDateTime {
    value: time::PrimitiveDateTime,
}

impl<'source> FromPyObject<'source> for BareDateTime {
    fn extract(ob: &'source PyAny) -> PyResult<Self> {
        let dt = ob.downcast::<PyDateTime>()?;

        if let Ok(tzinfo) = dt.getattr("tzinfo") {
            if !tzinfo.is_none() {
                return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(
                    "Cannot pass a tz-aware datetime",
                ));
            }
        }

        if let Ok(fold) = dt.getattr("fold") {
            if let Ok(res) = fold.compare(0u8) {
                use core::cmp::Ordering::Equal;
                match res {
                    Equal => {}
                    _ => {
                        return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(
                            "Cannot pass a folded datetime",
                        ))
                    }
                }
            }
        }

        let value = time::PrimitiveDateTime::new(
            time::Date::from_calendar_date(
                dt.get_year(),
                time::Month::try_from(dt.get_month()).unwrap(),
                dt.get_day(),
            )
            .unwrap(),
            time::Time::from_hms_micro(
                dt.get_hour(),
                dt.get_minute(),
                dt.get_second(),
                dt.get_microsecond(),
            )
            .unwrap(),
        );
        Ok(Self { value })
    }
}

impl ToPyObject for BareDateTime {
    fn to_object(&self, py: Python) -> PyObject {
        let result = PyDateTime::new(
            py,
            self.value.year(),
            self.value.month().into(),
            self.value.day(),
            self.value.hour(),
            self.value.minute(),
            self.value.second(),
            self.value.microsecond(),
            None,
        )
        .unwrap();
        result.to_object(py)
    }
}

impl IntoPy<PyObject> for BareDateTime {
    fn into_py(self, py: Python) -> PyObject {
        ToPyObject::to_object(&self, py)
    }
}

impl Default for BareDateTime {
    #[inline]
    fn default() -> Self {
        Self {
            value: datetime!(1970-01-01 00:00:00),
        }
    }
}

/// A data-carrying wrapper for Python's timedelta.
///
/// We implement FromPyObject so that Python's timedelta can be converted to
/// this type.  This type implements the required traits of
/// [travertine::types::TravertineTypes::Duration].
#[derive(Clone, PartialEq, Debug, PartialOrd, Eq, Ord, Copy, Default)]
pub struct BareTimeDelta {
    value: time::Duration,
}

impl<'source> FromPyObject<'source> for BareTimeDelta {
    fn extract(ob: &'source PyAny) -> PyResult<Self> {
        let td = ob.downcast::<PyDelta>()?;
        let seconds = td.get_days() * 86400 + td.get_seconds();
        let value = time::Duration::new(seconds as i64, td.get_microseconds() * 1000);
        Ok(Self { value })
    }
}

impl ToPyObject for BareTimeDelta {
    fn to_object(&self, py: Python) -> PyObject {
        let result = PyDelta::new(py, 0, 0, 0, false).unwrap();
        result.to_object(py)
    }
}

impl IntoPy<PyObject> for BareTimeDelta {
    fn into_py(self, py: Python) -> PyObject {
        ToPyObject::to_object(&self, py)
    }
}

#[cfg(test)]
mod test {
    use super::*;
    use pyo3::types::IntoPyDict;

    #[test]
    fn python_naive_datetime_conversion() {
        pyo3::prepare_freethreaded_python();
        Python::with_gil(|py| -> PyResult<()> {
            let datetime = py.import("datetime").unwrap();
            let locals = [("datetime", datetime)].into_py_dict(py);
            let now: &PyAny = py
                .eval("datetime.datetime.utcnow()", None, Some(&locals))
                .unwrap();

            let bare = <BareDateTime as FromPyObject>::extract(now).unwrap();

            let back: PyObject = bare.to_object(py);
            assert_eq!(now.compare(back).unwrap(), std::cmp::Ordering::Equal);
            Ok(())
        })
        .expect("Test failed");
    }

    #[test]
    fn python_nonnaive_datetime_conversion() {
        pyo3::prepare_freethreaded_python();
        Python::with_gil(|py| -> PyResult<()> {
            let datetime = py.import("datetime").unwrap();
            let locals = [("d", datetime)].into_py_dict(py);
            let code = "d.datetime.utcnow().replace(tzinfo=d.timezone(d.timedelta(0), 'UTC'))";
            let now: &PyAny = py.eval(code, None, Some(&locals)).unwrap();
            assert!(<BareDateTime as FromPyObject>::extract(now).is_err());
            Ok(())
        })
        .expect("test failed");
    }
}
