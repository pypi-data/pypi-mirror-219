#![allow(clippy::type_complexity)]
use pyo3::prelude::*;
use rayon::prelude::*;
use std::collections::HashMap;
use travertine_runtime::prelude::*;

use crate::demand::UnitaryDemand;
use crate::floats::parse_method;
use crate::matrix::MatrixProcedure;
use crate::types::TravertinePyTypes;

/// A representation of a pricing program.
///
/// This class is implemented in Rust and exposed to Python as an extension
/// class.
///
/// This class has a very *delicate* API, so you might want to use
/// `create_program`:func: instead.
///
/// You must comply with the following rules:
///
/// - Each procedure is identified uniquely by an integer (`usize`). All methods
///   take an `index` parameter for this purpose.
///
///   Trying to reuse an index will raise a ValueError.
///
/// - For procedures that take sub-procedures, you must first add the
///   sub-procedures and use the given identifiers to refer to them.
///
/// - The last procedure added to the program is the entry point of the pricing
///   program.
///
/// The API has two broad groups of methods:
///
/// - The methods ``add_`` to create the program (though you should use
///   `create_program`:func:), which update the Program's default the procedure.
///
/// - The methods that execute the program for a given demand.
#[pyclass(module = "travertine")]
#[derive(Clone)]
pub struct Program {
    vm: VM<TravertinePyTypes>,

    #[pyo3(get)]
    procedure_index: ProcedureIndex,
}

fn vmerror_to_pyerr(vmerror: VMError) -> PyErr {
    match vmerror {
        VMError::DuplicatedProcedure(_) => {
            PyErr::new::<pyo3::exceptions::PyValueError, _>("Duplicated procedure index")
        }

        VMError::MissingProcedure(id) => PyErr::new::<pyo3::exceptions::PyValueError, _>(format!(
            "Missing procedure index {}",
            id
        )),
    }
}

impl Default for Program {
    fn default() -> Self {
        Self {
            vm: VM::new(),
            procedure_index: 0,
        }
    }
}

#[pymethods]
impl Program {
    #[pyo3(text_signature = "(capacity: int = None)")]
    #[new]
    fn new(capacity: Option<usize>) -> Self {
        if let Some(cap) = capacity {
            Self {
                vm: VM::with_capacity(cap),
                procedure_index: 0,
            }
        } else {
            Self::default()
        }
    }

    /// Make a deep copy of the program.
    ///
    /// You can use this to cache programs that need further procedures.
    /// After you created a program, you may want enclose its top procedure
    /// as the sup-procedure, but keep the original program unaffected.
    ///
    fn copy(&self) -> Self {
        self.clone()
    }

    /// Add an IdentityProcedure to the current program with the given `index`
    #[pyo3(text_signature = "(index: ProcedureIndex, proc: ProcedureIndex, /)")]
    fn add_identity_procedure(
        &mut self,
        index: ProcedureIndex,
        proc: ProcedureIndex,
    ) -> PyResult<()> {
        self.procedure_index = self
            .vm
            .add_procedure(index, Procedure::Identity(proc))
            .map_err(vmerror_to_pyerr)?;
        Ok(())
    }

    /// Add an UndefinedProcedure to the current program with the given `index`.
    #[pyo3(text_signature = "(index: int, title: str = None)")]
    fn add_undefined_procedure(
        &mut self,
        index: ProcedureIndex,
        title: Option<String>,
    ) -> PyResult<()> {
        self.procedure_index = self
            .vm
            .add_procedure(index, Procedure::ReturnUndefined(title))
            .map_err(vmerror_to_pyerr)?;
        Ok(())
    }

    /// Add a ConstantProcedure to the current program with the given `index`.
    #[pyo3(text_signature = "(index: int, title: str = None)")]
    fn add_constant_procedure(&mut self, index: ProcedureIndex, value: f64) -> PyResult<()> {
        self.procedure_index = self
            .vm
            .add_procedure(index, Procedure::ReturnConstant(value))
            .map_err(vmerror_to_pyerr)?;
        Ok(())
    }

    /// Add a GetAttributeProcedure to the current program with the given
    /// `index`.
    #[pyo3(text_signature = "(index: int, attr: str)")]
    fn add_getattr_procedure(
        &mut self,
        index: ProcedureIndex,
        attr: <TravertinePyTypes as TravertineTypes>::AttrId,
    ) -> PyResult<()> {
        self.procedure_index = self
            .vm
            .add_procedure(index, Procedure::GetAttribute(attr))
            .map_err(vmerror_to_pyerr)?;
        Ok(())
    }

    /// Add a GetAttributeProcedure to the current program with the given
    /// `index`.
    #[pyo3(text_signature = "(index: ProcedureIndex, varname: str, default: float, /)")]
    fn add_varname_procedure(
        &mut self,
        index: ProcedureIndex,
        varname: <TravertinePyTypes as TravertineTypes>::VariableName,
        default: f64,
    ) -> PyResult<()> {
        self.procedure_index = self
            .vm
            .add_procedure(index, Procedure::GetVariable(varname, default))
            .map_err(vmerror_to_pyerr)?;
        Ok(())
    }

    /// Add a FormulaProcedure to the current program with the given `index`.
    ///
    /// All sub-procedures must have been already added to the program.
    /// Otherwise, raise a ValueError.
    #[pyo3(text_signature = "(index: ProcedureIndex, code: str, procedures: List[ProcedureIndex])")]
    fn add_formula_procedure(
        &mut self,
        index: ProcedureIndex,
        code: String,
        procedures: Vec<ProcedureIndex>,
    ) -> PyResult<()> {
        let formula = Formula::from_code(code.as_ref())
            .map_err(PyErr::new::<pyo3::exceptions::PyValueError, _>)?;
        self.procedure_index = self
            .vm
            .add_procedure(index, Procedure::Formula(formula, procedures))
            .map_err(vmerror_to_pyerr)?;
        Ok(())
    }

    /// Add a CeilRoundingProcedure to the current program with the given
    /// `index`.
    #[pyo3(text_signature = "(index: ProcedureIndex, proc: ProcedureIndex, /)")]
    fn add_ceil_procedure(&mut self, index: ProcedureIndex, proc: ProcedureIndex) -> PyResult<()> {
        self.procedure_index = self
            .vm
            .add_procedure(index, Procedure::Ceil(proc))
            .map_err(vmerror_to_pyerr)?;
        Ok(())
    }

    /// Add a FloorRoundingProcedure to the current program with the given
    /// `index`.
    #[pyo3(text_signature = "(index: ProcedureIndex, proc: ProcedureIndex, /)")]
    fn add_floor_procedure(&mut self, index: ProcedureIndex, proc: ProcedureIndex) -> PyResult<()> {
        self.procedure_index = self
            .vm
            .add_procedure(index, Procedure::Floor(proc))
            .map_err(vmerror_to_pyerr)?;
        Ok(())
    }

    /// Add a RoundProcedure to the current program with the given
    /// `index`.
    #[pyo3(text_signature = "(index: ProcedureIndex, digits: int, proc: ProcedureIndex, /)")]
    fn add_round_procedure(
        &mut self,
        index: ProcedureIndex,
        digits: u8,
        method: &str,
        proc: ProcedureIndex,
    ) -> PyResult<()> {
        let method = parse_method(method)?;
        self.procedure_index = self
            .vm
            .add_procedure(index, Procedure::Round(digits, method, proc))
            .map_err(vmerror_to_pyerr)?;
        Ok(())
    }

    /// Add a SetEnvProcedure to the current program with the given `index`.
    #[pyo3(
        text_signature = "(index: ProcedureIndex, env: Mapping[str, float],  proc: ProcedureIndex, /)"
    )]
    fn add_setenv_procedure(
        &mut self,
        index: ProcedureIndex,
        environment: HashMap<<TravertinePyTypes as TravertineTypes>::VariableName, f64>,
        proc: ProcedureIndex,
    ) -> PyResult<()> {
        self.procedure_index = self
            .vm
            .add_procedure(index, Procedure::SetEnv(environment, proc))
            .map_err(vmerror_to_pyerr)?;
        Ok(())
    }

    /// Add a SetFallbackEnvProcedure to the current program with the given
    /// `index`.
    #[pyo3(
        text_signature = "(index: ProcedureIndex, env: Mapping[str, float],  proc: ProcedureIndex, /)"
    )]
    fn add_setfallback_procedure(
        &mut self,
        index: ProcedureIndex,
        environment: HashMap<<TravertinePyTypes as TravertineTypes>::VariableName, f64>,
        proc: ProcedureIndex,
    ) -> PyResult<()> {
        self.procedure_index = self
            .vm
            .add_procedure(index, Procedure::SetFallback(environment, proc))
            .map_err(vmerror_to_pyerr)?;
        Ok(())
    }

    /// Add a branching procedure with branches using ValidityPredicate.
    ///
    /// If `backtrack` is True we create a BacktrackingBranchingProcedure
    /// instead of the BranchingProcedure.
    #[pyo3(
        signature=(index, branches, otherwise_procedure, backtrack, /),
        text_signature = "(index: ProcedureIndex, branches: Sequence[Tuple[datetime, datetime, ProcedureIndex]], otherwise_procedure: Optional[ProcedureIndex], backtrack: bool, /)"
    )]
    fn add_branching_procedure_with_validity_pred(
        &mut self,
        index: ProcedureIndex,
        branches: Vec<(
            Option<<TravertinePyTypes as TravertineTypes>::DateTime>,
            Option<<TravertinePyTypes as TravertineTypes>::DateTime>,
            ProcedureIndex,
        )>,
        otherwise_procedure: Option<ProcedureIndex>,
        backtrack: bool,
    ) -> PyResult<()> {
        if !backtrack {
            self.add_branching_procedure_with_two_args(
                index,
                branches,
                otherwise_procedure,
                Predicate::Validity,
                Procedure::MatchBranch,
            )
        } else {
            self.add_branching_procedure_with_two_args(
                index,
                branches,
                otherwise_procedure,
                Predicate::Validity,
                Procedure::MatchBacktrackingBranch,
            )
        }
    }

    /// Add a branching procedure with branches using ExecutionPredicate.
    ///
    /// If `backtrack` is True we create a BacktrackingBranchingProcedure
    /// instead of the BranchingProcedure.
    #[pyo3(
        signature=(index, branches, otherwise_procedure, backtrack, /),
        text_signature = "(index: ProcedureIndex, branches: Sequence[Tuple[datetime, datetime, ProcedureIndex]], otherwise_procedure: Optional[ProcedureIndex], backtrack: bool, /)"
    )]
    fn add_branching_procedure_with_execution_pred(
        &mut self,
        index: ProcedureIndex,
        branches: Vec<(
            Option<<TravertinePyTypes as TravertineTypes>::DateTime>,
            Option<<TravertinePyTypes as TravertineTypes>::DateTime>,
            ProcedureIndex,
        )>,
        otherwise_procedure: Option<ProcedureIndex>,
        backtrack: bool,
    ) -> PyResult<()> {
        if !backtrack {
            self.add_branching_procedure_with_two_args(
                index,
                branches,
                otherwise_procedure,
                Predicate::Execution,
                Procedure::MatchBranch,
            )
        } else {
            self.add_branching_procedure_with_two_args(
                index,
                branches,
                otherwise_procedure,
                Predicate::Execution,
                Procedure::MatchBacktrackingBranch,
            )
        }
    }

    /// Add a branching procedure with branches using QuantityPredicate.
    ///
    /// If `backtrack` is True we create a BacktrackingBranchingProcedure
    /// instead of the BranchingProcedure.
    #[pyo3(
        signature=(index, branches, otherwise_procedure, backtrack, /),
        text_signature = "(index: ProcedureIndex, branches: Sequence[Tuple[float, float, ProcedureIndex]], otherwise_procedure: Optional[ProcedureIndex], backtrack: bool, /)"
    )]
    fn add_branching_procedure_with_quantity_pred(
        &mut self,
        index: ProcedureIndex,
        branches: Vec<(Option<f64>, Option<f64>, ProcedureIndex)>,
        otherwise_procedure: Option<ProcedureIndex>,
        backtrack: bool,
    ) -> PyResult<()> {
        if !backtrack {
            self.add_branching_procedure_with_two_args(
                index,
                branches,
                otherwise_procedure,
                Predicate::Quantity,
                Procedure::MatchBranch,
            )
        } else {
            self.add_branching_procedure_with_two_args(
                index,
                branches,
                otherwise_procedure,
                Predicate::Quantity,
                Procedure::MatchBacktrackingBranch,
            )
        }
    }

    /// Add a branching procedure with branches using MatchesAttributePredicate
    ///
    /// If `backtrack` is True we create a BacktrackingBranchingProcedure
    /// instead of the BranchingProcedure.
    ///
    /// In this implementation, the type AttrId is just a string (we assume
    /// these attributes are always from the commodity).  The type CustomValue
    /// can be numbers (float, and int), strings, datetime, timedelta and
    /// `ExternalObject`:class:
    ///
    #[pyo3(
        signature=(index, branches, otherwise_procedure, backtrack, /),
        text_signature = "(index: ProcedureIndex, branches: Sequence[Tuple[AttrId, CustomValue, ProcedureIndex]], otherwise_procedure: Optional[ProcedureIndex], backtrack: bool, /)"
    )]
    fn add_branching_procedure_with_match_attr_pred(
        &mut self,
        index: ProcedureIndex,
        branches: Vec<(
            <TravertinePyTypes as TravertineTypes>::AttrId,
            <TravertinePyTypes as TravertineTypes>::CustomValue,
            ProcedureIndex,
        )>,
        otherwise_procedure: Option<ProcedureIndex>,
        backtrack: bool,
    ) -> PyResult<()> {
        if !backtrack {
            self.add_branching_procedure_with_two_args(
                index,
                branches,
                otherwise_procedure,
                Predicate::MatchesAttributes,
                Procedure::MatchBranch,
            )
        } else {
            self.add_branching_procedure_with_two_args(
                index,
                branches,
                otherwise_procedure,
                Predicate::MatchesAttributes,
                Procedure::MatchBacktrackingBranch,
            )
        }
    }

    /// Add a branching procedure with branches using AttributeInRangePredicate
    ///
    /// If `backtrack` is True we create a BacktrackingBranchingProcedure
    /// instead of the BranchingProcedure.
    ///
    /// In this implementation, the type AttrId is just a string (we assume
    /// these attributes are always from the commodity).  The type CustomValue
    /// can be numbers (float, and int), strings, datetime, timedelta and
    /// `ExternalObject`:class:
    ///
    #[pyo3(
        signature=(index, branches, otherwise_procedure, backtrack, /),
        text_signature = "(index: ProcedureIndex, branches: Sequence[Tuple[AttrId, CustomValue, CustomValue, ProcedureIndex]], otherwise_procedure: Optional[ProcedureIndex], backtrack: bool, /)"
    )]
    fn add_branching_procedure_with_attr_in_range_pred(
        &mut self,
        index: ProcedureIndex,
        branches: Vec<(
            <TravertinePyTypes as TravertineTypes>::AttrId,
            Option<<TravertinePyTypes as TravertineTypes>::CustomValue>,
            Option<<TravertinePyTypes as TravertineTypes>::CustomValue>,
            ProcedureIndex,
        )>,
        otherwise_procedure: Option<ProcedureIndex>,
        backtrack: bool,
    ) -> PyResult<()> {
        if !backtrack {
            self.add_branching_procedure_with_three_args(
                index,
                branches,
                otherwise_procedure,
                Predicate::AttributeInRange,
                Procedure::MatchBranch,
            )
        } else {
            self.add_branching_procedure_with_three_args(
                index,
                branches,
                otherwise_procedure,
                Predicate::AttributeInRange,
                Procedure::MatchBacktrackingBranch,
            )
        }
    }

    /// Add a matrix procedure to the program.
    fn add_matrix_procedure(
        &mut self,
        index: ProcedureIndex,
        matrix: &MatrixProcedure,
    ) -> PyResult<()> {
        self.procedure_index = self
            .vm
            .add_procedure(index, matrix.procedure())
            .map_err(vmerror_to_pyerr)?;
        Ok(())
    }

    /// Execute the program on a given unitary demand.  The value of `undefined`
    /// is any Python object which is passed back when the program returns
    /// Undefined.
    fn execute<'p>(&'p self, demand: &UnitaryDemand, undefined: &'p PyAny) -> PyResult<PyObject> {
        let result = self.vm.execute(demand, self.procedure_index);
        Ok(self.map_result(result, undefined))
    }

    fn execute_many<'p>(
        &'p self,
        demands: Vec<UnitaryDemand>,
        undefined: &'p PyAny,
    ) -> PyResult<Vec<PyObject>> {
        let py = undefined.get_type().as_ref().py();
        let result: Vec<ProcessResult> = py.allow_threads(move || {
            demands
                .par_iter()
                .map(|demand| self.vm.execute(demand, self.procedure_index))
                .collect()
        });
        let res: Vec<PyObject> = result
            .iter()
            .map(|res| self.map_result(res.clone(), undefined))
            .collect();
        Ok(res)
    }
}

impl Program {
    #[inline]
    fn map_result<'p>(&'p self, result: ProcessResult, undefined: &'p PyAny) -> PyObject {
        let py = undefined.get_type().as_ref().py();
        result
            .map_result()
            .map_or(undefined.to_object(py), |r| r.to_object(py))
    }

    #[inline]
    fn add_branching_procedure_with_two_args<B, P, T: Clone, F: Clone>(
        &mut self,
        index: ProcedureIndex,
        branches: Vec<(F, T, ProcedureIndex)>,
        otherwise: Option<ProcedureIndex>,
        pred: P,
        proc: B,
    ) -> PyResult<()>
    where
        B: Fn(Vec<(Predicate<TravertinePyTypes>, ProcedureIndex)>) -> Procedure<TravertinePyTypes>,
        P: Fn(F, T) -> Predicate<TravertinePyTypes>,
    {
        let mut predicates: Vec<(Predicate<TravertinePyTypes>, ProcedureIndex)> = branches
            .iter()
            .map(|(first, second, proc)| (pred(first.clone(), second.clone()), *proc))
            .collect();
        if let Some(otherwise) = otherwise {
            predicates.push((Predicate::Otherwise, otherwise))
        }
        self.procedure_index = self
            .vm
            .add_procedure(index, proc(predicates))
            .map_err(vmerror_to_pyerr)?;
        Ok(())
    }

    #[inline]
    fn add_branching_procedure_with_three_args<B, P, T: Clone, F: Clone, Z: Clone>(
        &mut self,
        index: ProcedureIndex,
        branches: Vec<(F, T, Z, ProcedureIndex)>,
        otherwise: Option<ProcedureIndex>,
        pred: P,
        proc: B,
    ) -> PyResult<()>
    where
        B: Fn(Vec<(Predicate<TravertinePyTypes>, ProcedureIndex)>) -> Procedure<TravertinePyTypes>,
        P: Fn(F, T, Z) -> Predicate<TravertinePyTypes>,
    {
        let mut predicates: Vec<(Predicate<TravertinePyTypes>, ProcedureIndex)> = branches
            .iter()
            .map(|(first, second, third, proc)| {
                (pred(first.clone(), second.clone(), third.clone()), *proc)
            })
            .collect();
        if let Some(otherwise) = otherwise {
            predicates.push((Predicate::Otherwise, otherwise))
        }
        self.procedure_index = self
            .vm
            .add_procedure(index, proc(predicates))
            .map_err(vmerror_to_pyerr)?;
        Ok(())
    }
}
