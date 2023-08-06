mod demand;
mod floats;
mod matrix;
mod program;
mod types;

use crate::demand::{NullDemand, UnitaryDemand};
use crate::floats::float_round;
use crate::matrix::{MatrixProcedure, MatrixRow};
use crate::program::Program;
use crate::types::ExternalObject;

use pyo3::prelude::*;

/// Rust runtime to compute price-tables at light speed.
///
/// Travertine exposes a simple API to compute several demands in a row.  This
/// allows to faster computation of the price tables because the hot spot of
/// such use case is the computation of many prices.
///
/// The Python side will still be in charge of creating the demands.  This is
/// because the AVM is still reasonably fast to compute in Python, and it
/// would take more time for us to do it in Rust now.  I'm still a Rust newbie.
///
#[pymodule]
fn _impl(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Program>()?;
    m.add_class::<NullDemand>()?;
    m.add_class::<ExternalObject>()?;
    m.add_class::<UnitaryDemand>()?;
    m.add_class::<MatrixProcedure>()?;
    m.add_class::<MatrixRow>()?;
    m.add_function(wrap_pyfunction!(float_round, m)?)?;
    Ok(())
}
