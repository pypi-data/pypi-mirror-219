use pyo3::prelude::*;
use travertine_runtime::prelude::*;

pub(crate) fn parse_method(method: &str) -> PyResult<RoundingMethod> {
    match method {
        "UP" => Ok(RoundingMethod::UP),
        "DOWN" => Ok(RoundingMethod::DOWN),
        "HALF-UP" => Ok(RoundingMethod::HALF_UP),
        _ => Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(format!(
            "Invalid rounding method {}",
            method
        ))),
    }
}

/// Rounds the 'value' with as many precision digits (after the decimal point)
/// using a rounding method (one of "UP", "DOWN", "HALF-UP").
#[pyfunction]
#[pyo3(text_signature = "(value, precision_digits=2, rounding_method='HALF-UP')")]
pub fn float_round(value: f64, precision_digits: u8, rounding_method: &str) -> PyResult<f64> {
    let method = parse_method(rounding_method)?;
    Ok(method.round(value, precision_digits))
}
