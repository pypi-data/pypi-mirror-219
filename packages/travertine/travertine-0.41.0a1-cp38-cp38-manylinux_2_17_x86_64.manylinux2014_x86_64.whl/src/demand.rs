use pyo3::prelude::*;
use pyo3::types::PyType;
use std::collections::HashMap;
use travertine_runtime::prelude::*;

use crate::types::{BareDateTime, TravertinePyTypes, TypedValue};

/// The null demand.
///
/// This demand does implement any of the replace methods.  It mostly serves
/// to test procedures which are invariant to the demand.
#[pyclass(module = "travertine")]
pub struct NullDemand {}

#[pymethods]
impl NullDemand {
    #[new]
    fn new() -> Self {
        Self::default()
    }
}

impl Default for NullDemand {
    #[inline]
    fn default() -> Self {
        Self {}
    }
}

impl PriceDemand<TravertinePyTypes> for NullDemand {
    #[inline]
    fn date(&self) -> <TravertinePyTypes as TravertineTypes>::DateTime {
        <TravertinePyTypes as TravertineTypes>::DateTime::default()
    }

    #[inline]
    fn attr<K>(&self, _k: K) -> Option<<TravertinePyTypes as TravertineTypes>::CustomValue>
    where
        K: Into<<TravertinePyTypes as TravertineTypes>::AttrId>,
    {
        None
    }

    #[inline]
    fn quantity(&self) -> f64 {
        0.0
    }
}

// This pyclass holds the values of a unitary demand, its replace
// implementation is done in Python, though.
#[pyclass(module = "travertine")]
#[derive(Clone, Debug)]
pub struct UnitaryDemand {
    #[pyo3(get)]
    date: BareDateTime,

    quantity: f64,
    start_date: BareDateTime,
    attrs: HashMap<String, TypedValue>,
}

#[pymethods]
impl UnitaryDemand {
    #[new]
    fn new(
        date: BareDateTime,
        quantity: f64,
        start_date: BareDateTime,
        attrs: HashMap<String, TypedValue>,
    ) -> Self {
        UnitaryDemand {
            date,
            quantity,
            start_date,
            attrs,
        }
    }

    #[classmethod]
    fn default(_cls: &PyType) -> Self {
        UnitaryDemand {
            date: BareDateTime::default(),
            quantity: 1.0,
            start_date: BareDateTime::default(),
            attrs: HashMap::new(),
        }
    }

    fn attr<'p>(&'p self, attr: &'p PyAny) -> PyResult<PyObject> {
        let attr_name: String = attr.extract()?;
        if let Some(value) = PriceDemand::attr(self, attr_name) {
            Ok(value.into_py(attr.py()))
        } else {
            Ok(attr.py().None())
        }
    }

    fn replace_attr(
        &self,
        attr: <TravertinePyTypes as TravertineTypes>::AttrId,
        value: <TravertinePyTypes as TravertineTypes>::CustomValue,
    ) -> Self {
        ReplaceablePriceDemand::replace_attr(self, attr, value)
    }
}

impl PriceDemand<TravertinePyTypes> for UnitaryDemand {
    #[inline]
    fn date(&self) -> <TravertinePyTypes as TravertineTypes>::DateTime {
        self.date
    }

    #[inline]
    fn quantity(&self) -> f64 {
        self.quantity
    }

    #[inline]
    fn start_date(&self) -> <TravertinePyTypes as TravertineTypes>::DateTime {
        self.start_date
    }

    #[inline]
    fn attr<K>(&self, k: K) -> Option<<TravertinePyTypes as TravertineTypes>::CustomValue>
    where
        K: Into<<TravertinePyTypes as TravertineTypes>::AttrId>,
    {
        self.attrs.get(&k.into()).map(|r| r.to_owned())
    }
}

impl ReplaceablePriceDemand<TravertinePyTypes> for UnitaryDemand {
    fn replace_date(&self, date: <TravertinePyTypes as TravertineTypes>::DateTime) -> Self {
        let attrs = self.attrs.clone();
        Self {
            date,
            attrs,
            ..*self
        }
    }
    fn replace_quantity(&self, quantity: f64) -> Self {
        let attrs = self.attrs.clone();
        Self {
            quantity,
            attrs,
            ..*self
        }
    }
    fn replace_start_date(
        &self,
        start_date: <TravertinePyTypes as TravertineTypes>::DateTime,
    ) -> Self {
        let attrs = self.attrs.clone();
        Self {
            start_date,
            attrs,
            ..*self
        }
    }
    fn replace_attr<K>(
        &self,
        attr: K,
        value: <TravertinePyTypes as TravertineTypes>::CustomValue,
    ) -> Self
    where
        K: Into<<TravertinePyTypes as TravertineTypes>::AttrId>,
    {
        let mut attrs = self.attrs.clone();
        attrs.insert(attr.into(), value);
        Self { attrs, ..*self }
    }
}
