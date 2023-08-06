=====================================
 :mod:`travertine` -- Travertine API
=====================================

.. automodule:: travertine

Rust runtime
============

Travertine implements most of the `procedures <travertine.procedures>`:mod:
runtime in Rust so that we can generate price tables faster using this
runtime.

On the types annotations
------------------------

In the following signatures we use the type ``Index`` as an alias for
``int``.  The index is the identifier of a procedure in a program.  When a
procedure takes sub-procedures it know their indexes in order add itself to
the `Program`:class:.

.. note:: Implementation detail.

   The current implementation uses the funcion `id`:func: to produce the Index
   of the procedures.

The type ``AttrId`` is the type we use to identify our the demand's
attributes.  Currently this is just ``str``.

The type ``CustomValue`` is an alias for ``Union[datetime, timedelta, float,
int, str, ExternalObject]``, which are the possible values we pass to the Rust
runtime.


API
---

.. autofunction:: create_program

.. autoclass:: Program

   .. automethod:: add_undefined_procedure(index: Index, title: str = None, /)
   .. automethod:: add_constant_procedure(index: Index, value: float, /)
   .. automethod:: add_getattr_procedure(index: Index, attr, /)
   .. automethod:: add_varname_procedure(index: Index, varname, default: float, /)

   .. automethod:: add_formula_procedure(index: Index, code, procedures: list[Index], /)

   .. automethod:: add_ceil_procedure(index: Index, proc: Index, /)
   .. automethod:: add_floor_procedure(index: Index, proc: Index, /)
   .. automethod:: add_round_procedure(index: Index, proc: Index, /)

   .. automethod:: add_setenv_procedure(index: Index, env: Mapping[str, float],  proc: Procedureindex, /)
   .. automethod:: add_setfallback_procedure(index: Index, env: Mapping[str, float],  proc: Index, /)

   .. automethod:: add_branching_procedure_with_validity_pred(index: Index, branches: Sequence[Tuple[datetime, datetime, Index]], otherwise: Optional[Index], backtrack: bool, /)
   .. automethod:: add_branching_procedure_with_execution_pred(index: Index, branches: Sequence[Tuple[datetime, datetime, Index]], otherwise: Optional[Index], backtrack: bool, /)
   .. automethod:: add_branching_procedure_with_quantity_pred(index: Index, branches: Sequence[Tuple[float, float, Index]], otherwise: Optional[Index], backtrack: bool, /)
   .. automethod:: add_branching_procedure_with_match_attr_pred(index: Index, branches: Sequence[Tuple[AttrId, CustomValue, Index]], otherwise: Optional[Index], backtrack: bool, /)
   .. automethod:: add_branching_procedure_with_attr_in_range_pred(index: Index, branches: Sequence[Tuple[AttrId, CustomValue, CustomValue, Index]], otherwise: Optional[Index], backtrack: bool, /)

   .. automethod:: add_identity_procedure(index: Index, proc: Index, /)

   .. automethod:: add_matrix_procedure(index: Index, matrix: travertine.MatrixProcedure, /)

   .. automethod:: execute_many(demands: Sequence[UnitaryDemand], undefined: Result) -> Sequence[Result]
   .. automethod:: execute(demand: UnitaryDemand, undefined: Result) -> Result

.. autoclass:: ExternalObject

.. autoclass:: UnitaryDemand(date: datetime, quantity: float, start_date: datetime, attrs: Mapping[str, CustomValue]])


.. _api-to_travertine_external_object:

Converting to ExternalObject
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When `odoo`_ is installed Travertine will convert singleton recordsets to
`~travertine.ExternalObject`:class: that appear as values in
`~travertine.predicates.MatchesAttributePredicate`:class: and other classes
that may hold such values.

If you need to pass other types of objects predicates or a values of the
demand, the class may implement the ``_to_travertine_external_object_``
protocol:

.. class:: object

   .. method:: _to_travertine_external_object_() -> ExternalObject

      Convert the object to an ExternalObject suitable to be passed to the
      Rust runtime.

      Example:

      .. code-block:: python

        >>> from dataclasses import dataclass
        >>> from travertine import ExternalObject

        >>> @dataclass(frozen=True)
        ... class Foo:
        ...    id: int
        ...
        ...    def _to_travertine_external_object_(self) -> ExternalObject:
        ...        return ExternalObject(f"urn:Foo:{self.id}", self.id)
        ...
        ...    def __eq__(self, other):
        ...        if isinstance(other, Foo):
        ...            return self.id == other.id
        ...        elif isinstance(other, ExternalObject):
        ...            return self._to_travertine_external_object() == other
        ...        else:
        ...            return NotImplemented

      .. note:: The method is looked up in the *class* and not the instances.


Instances of `xotless.ImmutableWrapper`:class: are extracted before trying to
convert them to ExternalObject.

.. warning:: Unwrapping of ImmutableWrapper is not a stable feature.

   By unwrapping we lose the overrides in the wrapper and the object passed to
   Rust wouldn't behave the same as the Python object.  But we need this
   feature so that we can introduce travertine without requiring much changes
   in ``xhg2``.

.. _odoo: https://github.com/odoo/odoo

Python Runtime
==============

The Python runtime is the current stable implementation that backs the
computation of prices in `Mercurio 2018`.  The *language of prices* has just
four kinds of constructions:

- `Procedures`_,
- `Predicates`_,
- `Splitters`_, and
- `Aggregators`_

By combining them we can perform quite elaborate pricing programs, which are
guaranteed to terminate and for which prices tables generating algorithm are
feasible.

These constructions operate in a very restricted space.  A procedure takes a
`demand <travertine.types.Demand>`:class: (which is actually a type, of which
`~travertine.UnitaryDemand`:class: is an implementation suitable to generate
price tables in Rust), and an environment and return the result.

The types and environment
-------------------------

.. automodule:: travertine.types
   :members: Procedure, Predicate, Splitter, Aggregator, Undefined, Demand,
             Request, Commodity, Environment, format_result, parse_result,
			 AttributeLocator, TypeName, SimpleType, TypedAttribute


Procedures
----------

.. automodule:: travertine.procedures


``UndefinedProcedure``
~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: UndefinedProcedure


``ConstantProcedure``
~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: ConstantProcedure


``GetAttributeProcedure``
~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: GetAttributeProcedure


``VarnameProcedure``
~~~~~~~~~~~~~~~~~~~~

.. autoclass:: VarnameProcedure


``CeilRoundingProcedure``
~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: CeilRoundingProcedure


``FloorRoundingProcedure``
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: FloorRoundingProcedure


``RoundProcedure``
~~~~~~~~~~~~~~~~~~

.. autoclass:: RoundProcedure


``SetEnvProcedure``
~~~~~~~~~~~~~~~~~~~

.. autoclass:: SetEnvProcedure


``SetFallbackEnvProcedure``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: SetFallbackEnvProcedure


``BranchingProcedure``
~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: BranchingProcedure


``BacktrackingBranchingProcedure``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: BacktrackingBranchingProcedure


``FormulaProcedure``
~~~~~~~~~~~~~~~~~~~~

.. autoclass:: FormulaProcedure


``LoopProcedure``
~~~~~~~~~~~~~~~~~

.. autoclass:: LoopProcedure


``MapReduceProcedure``
~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: MapReduceProcedure


``MatrixProcedure``
~~~~~~~~~~~~~~~~~~~

.. module:: travertine.matrix

.. autoclass:: MatrixProcedure
   :members: add_row

.. autoclass:: MatrixRow


Predicates
----------

.. automodule:: travertine.predicates

``ValidityPredicate``
~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: ValidityPredicate


``ExecutionPredicate``
~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: ExecutionPredicate


``MatchesAttributePredicate``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: MatchesAttributePredicate


``AttributeInRangePredicate``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: AttributeInRangePredicate


``QuantityPredicate``
~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: QuantityPredicate


``Otherwise``
~~~~~~~~~~~~~

.. autoclass:: Otherwise


Splitters
---------

.. automodule:: travertine.splitters

``IdentitySplitter``
~~~~~~~~~~~~~~~~~~~~

.. autoclass:: IdentitySplitter

``RequestSplitter``
~~~~~~~~~~~~~~~~~~~

.. autoclass:: RequestSplitter

``UnitSplitter``
~~~~~~~~~~~~~~~~

.. autoclass:: UnitSplitter

``UnitRequestSplitter``
~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: UnitRequestSplitter


Aggregators
-----------

.. automodule:: travertine.aggregators

``SumAggregator``
~~~~~~~~~~~~~~~~~

.. autoclass:: SumAggregator

``MultAggregator``
~~~~~~~~~~~~~~~~~~

.. autoclass:: MultAggregator

``DivideAggregator``
~~~~~~~~~~~~~~~~~~~~

.. autoclass:: DivideAggregator

``MaxAggregator``
~~~~~~~~~~~~~~~~~

.. autoclass:: MaxAggregator

``MinAggregator``
~~~~~~~~~~~~~~~~~

.. autoclass:: MinAggregator

``CountAggregator``
~~~~~~~~~~~~~~~~~~~

.. autoclass:: CountAggregator

``CountDefinedAggregator``
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: CountDefinedAggregator

``TakeFirstAggregator``
~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: TakeFirstAggregator

``TakeFirstDefinedAggregator``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: TakeFirstDefinedAggregator

``TakeLastAggregator``
~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: TakeLastAggregator

``TakeLastDefinedAggregator``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: TakeLastDefinedAggregator

``AverageAggregator``
~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: AverageAggregator

``ModeAggregator``
~~~~~~~~~~~~~~~~~~

.. autoclass:: ModeAggregator

``FirstTimesCountAggregator``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: FirstTimesCountAggregator

``LastTimesCountAggregator``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: LastTimesCountAggregator


Price tables (Python)
=====================

Price tables are computed just by "looking" at the branches in pricing program
and generating all possibles unitary demands for the program.

.. automodule:: travertine.tables

.. autofunction:: generate_tables

.. autoclass:: ProgramDict

.. autofunction:: estimate_table_size

.. autoclass:: Table

   .. attribute:: name
      :type: str

      The name of the table.  This is the name of procedure (passed to
      `generate_tables`:func:) from which this table is being generated.

   .. attribute:: attrs
      :type: Tuple[Tuple[travertine.types.AttributeLocator, Any], ...]

      The shared attributes and values of all rows which are not part of the
      columns.  This will correspond to the group of attributes in
      `tables_conf <TableFormat.tables_conf>`:attr:.

   .. attribute:: columns_headers
      :type: Tuple[Any, ...]

   .. attribute:: rows
      :type: Iterator[Tuple[Any, ...]]



.. autoclass:: TableFormat
   :members: flattened

.. data:: NULL_FORMAT

.. autoclass:: ATTR_FORMAT

.. autoclass:: AttrFormatConfiguration


.. data:: MISSING_CELL

   A value to mark cells in a row for which the row's procedure has no
   possible value in that column.


Attribute Variability Map (AVM)
--------------------------------

An AVM is a map of attribute names to the set of values that might affect the
price result.  AVMs are computed automatically from procedures.  By looking at
the conditions the pricing program makes, we build a map of attributes and the
values they are compared to.

AVMs are defined for each type of the `procedures`_ and then combined together
when procedures takes sub-procedures.

.. automodule:: travertine.avm

``CombinedAVM``
~~~~~~~~~~~~~~~

.. autoclass:: CombinedAVM

``CascadingAVM``
~~~~~~~~~~~~~~~~

.. autoclass:: CascadingAVM

``FilteringAVM``
~~~~~~~~~~~~~~~~

.. autoclass:: FilteringAVM

``MergedAVM``
~~~~~~~~~~~~~

.. autoclass:: MergedAVM

``BranchingAVM``
~~~~~~~~~~~~~~~~

.. autofunction:: BranchingAVM


Internationalization (:mod:`travertine.i18n`)
=============================================

.. module:: travertine.i18n

Travertine's code contains just a few messages which are meant to be shown to
the user.

We use `gettext`:mod: to implement the function `_`:func: to get translated
messages.  Currently, we don't implement other functions like
`~gettext.ngettext`:func:, `~gettext.pgettext`:func:, nor
`~gettext.npgettext`:func:; but we plan to do so.

All messages are in the domain "travertine", so the functions taking a domain
name won't be supported.

.. function:: _(msgid: str) -> str

   Find and return the translation for the message given the `msgid`.  If no
   translation can be made return the same msgid.

   If you call this function within the context of a `locale`:func:, we try to
   perform we perform the translation for that locale or fallback to
   `~gettext.NullTranslation`:class:.  If the call is not within the context
   of `!locale`:func:, use the the standard `gettext`:mod: (i.e the
   translation depends on the value ``LC_MESSAGE``, ``LC_ALL``, etc.)

.. function:: locale(locale: str) -> ContextManager

   A context manager that instructs `_`:func: how to perform translations in a
   given locale without depending on ``LC_*`` environment variables.

   Example:

     >>> from travertine import i18n
     >>> from travertine.procedures import ConstantProcedure
     >>> from travertine.testing.base import NULL_DEMAND, EMPTY_ENV
     >>> with i18n.locale("es"):
     ...     proc = ConstantProcedure(42)
     ...     print(proc(NULL_DEMAND, EMPTY_ENV))
     Precio fijo = 42.00.


Note that procedure's titles are translated when the procedure is created and
not when running the procedure.  This is because you SHOULD really pass the
apropiate title and not use the default.  Other messages (predicates,
aggregators, etc) are translated on-demand.


Extra
=====

.. module:: travertine.floats

.. function:: float_round(value: float, precision_digits: int = 2, rounding_method: Literal["UP", "DOWN", "HALF-UP"] = "HALF-UP")

   Similar to `round`:func:, but allows a rounding method.  Internally, we use
   rust's `RoundingStrategy`_, with the following map:

   - ``"UP"`` means ``RoundingStrategy.AwayFromZero``,
   - ``"DOWN"`` means ``RoundingStrategy.ToZero``, and
   - ``"HALF-UP"`` means ``RoundingStrategy.MidpointAwayFromZero``.

.. _RoundingStrategy: https://docs.rs/rust_decimal/1.25.0/rust_decimal/prelude/enum.RoundingStrategy.html
