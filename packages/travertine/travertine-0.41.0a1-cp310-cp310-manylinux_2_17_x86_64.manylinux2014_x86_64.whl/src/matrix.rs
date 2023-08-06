use crate::types::*;
use either::{Either, Left, Right};
use pyo3::prelude::*;
use pyo3::types::PyString;
use travertine_runtime::prelude::*;

/// A procedure which computes prices based on a matrix.
///
/// Each row has many conditions, variables, defaults and a result.  All the
/// conditions must match in order to get the result.  The first row for which
/// the demand matches all conditions returns.
///
/// If no row matches, signal a backtrack or return Undefined.
///
#[pyclass(module = "travertine")]
#[derive(Clone, Debug)]
pub struct MatrixProcedure {
    rows: Vec<(
        Vec<MatrixCell<TravertinePyTypes>>,
        Either<Formula<TravertinePyTypes>, f64>,
    )>,
}

#[pymethods]
impl MatrixProcedure {
    #[new]
    fn new() -> Self {
        Self { rows: Vec::new() }
    }

    /// Add a row to the matrix.
    ///
    /// :param row: The conditions, variables and defaults in a row
    /// :type row: `MatrixRow`:class:
    ///
    /// :param code: The result or formula code.  If `code` is a string, it
    ///              will be regarded as a formula.  If it is a number, then
    ///              it's a direct result.
    /// :type code: int | float | str
    #[pyo3(text_signature = "(self, row, code)")]
    fn add_row(&mut self, row: MatrixRow, code: FormulaOrResult) -> PyResult<()> {
        let result: Either<_, _> = match code {
            FormulaOrResult::Formula(f) => {
                let subprocs = f.max_substep_index();
                if subprocs > 0 {
                    return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(format!(
                        "Unexpected sub-procedures in Matrix result specification, found {}",
                        subprocs
                    )));
                }
                Left(f)
            }
            FormulaOrResult::Result(val) => Right(val),
        };
        let cells: Vec<MatrixCell<_>> = row
            .conditions
            .iter()
            .map(|cond| MatrixCell::Condition(cond.clone()))
            .chain(
                row.variables
                    .iter()
                    .map(|(var, value)| MatrixCell::Variable(var.clone(), *value)),
            )
            .chain(
                row.defaults
                    .iter()
                    .map(|(var, value)| MatrixCell::Default(var.clone(), *value)),
            )
            .collect();
        self.rows.push((cells, result));
        Ok(())
    }
}

#[derive(Clone, Debug)]
enum FormulaOrResult {
    Formula(Formula<TravertinePyTypes>),
    Result(f64),
}

impl<'source> FromPyObject<'source> for FormulaOrResult {
    fn extract(ob: &'source PyAny) -> PyResult<Self> {
        if ob.is_instance_of::<PyString>() {
            Formula::from_code(ob.extract()?)
                .map(|f| Self::Formula(f))
                .map_err(PyErr::new::<pyo3::exceptions::PyValueError, _>)
        } else {
            Ok(Self::Result(ob.extract()?))
        }
    }
}

/// The row of conditions, variables and defaults.
///
#[pyclass(module = "travertine")]
#[derive(Clone, Debug)]
pub struct MatrixRow {
    conditions: Vec<MatrixCondition<TravertinePyTypes>>,
    variables: Vec<(<TravertinePyTypes as TravertineTypes>::VariableName, f64)>,
    defaults: Vec<(<TravertinePyTypes as TravertineTypes>::VariableName, f64)>,
}

#[pymethods]
impl MatrixRow {
    #[new]
    fn new() -> Self {
        Self {
            conditions: Vec::new(),
            variables: Vec::new(),
            defaults: Vec::new(),
        }
    }

    /// Add a condition checking the demand's date is in the range `start`,
    /// `end` (excluding `end`).
    fn add_condition_demand_date_in_range(&mut self, start: BareDateTime, end: BareDateTime) {
        self.conditions
            .push(MatrixCondition::DemandDateInRange(start, end))
    }

    /// Add a condition checking the demand's date is exactly a given value.
    fn add_condition_demand_date_is(&mut self, date: BareDateTime) {
        self.conditions.push(MatrixCondition::DemandDateIs(date))
    }

    /// Add a condition checking the commodities's date are all in the range
    /// `start`, `end` (excluding `end`).
    fn add_condition_start_date_in_range(&mut self, start: BareDateTime, end: BareDateTime) {
        self.conditions
            .push(MatrixCondition::ExecutionDateInRange(start, end))
    }

    /// Add a condition checking the commodities's date are all the given
    /// value.
    fn add_condition_start_date_is(&mut self, date: BareDateTime) {
        self.conditions.push(MatrixCondition::ExecutionDateIs(date))
    }

    /// Add a condition checking the requests' quantities are all in the range
    /// `start`, `end` (excluding `end`).
    fn add_condition_quantity_in_range(&mut self, min: f64, max: f64) {
        self.conditions
            .push(MatrixCondition::QuantityInRange(min, max))
    }

    /// Add a condition checking the requests' quantities are all the given
    /// value.
    fn add_condition_quantity_is(&mut self, quantity: f64) {
        self.conditions.push(MatrixCondition::QuantityIs(quantity))
    }

    /// Add a condition checking that the attribute named `attr` has a value
    /// in the range `start`, `end` (excluded) for all the commodities in the
    /// demand.
    fn add_condition_attr_in_range(&mut self, attr: String, lower: TypedValue, upper: TypedValue) {
        self.conditions
            .push(MatrixCondition::AttributeInRange(attr, lower, upper))
    }

    /// Add a condition checking that the attribute named `attr` has the given
    /// value for all the commodities in the demand.
    fn add_condition_attr_is(&mut self, attr: String, value: TypedValue) {
        self.conditions
            .push(MatrixCondition::AttributeIs(attr, value))
    }

    /// Set the value of the given variable.  This overrides the value of the
    /// variable.  The scope of this binding is just the row.
    fn add_variable(&mut self, variable: String, value: f64) {
        self.variables.push((variable, value))
    }

    /// Set the default value of the given variable.  This doesn't overrides
    /// the value of the variable, only sets the default. The scope of this
    /// default is just the row.
    fn add_default(&mut self, variable: String, value: f64) {
        self.defaults.push((variable, value))
    }
}

impl MatrixProcedure {
    pub(crate) fn procedure(&self) -> Procedure<TravertinePyTypes> {
        Procedure::Matrix(self.rows.clone())
    }
}
