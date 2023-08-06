===========
 Changelog
===========

Pre-releases 0.x
================

Unreleased.  Release 0.41.0
---------------------------

- Upgrade to PyO3 0.19.1.


2023-03-14.  Release 0.40.0
---------------------------

- Upgrade to PyO3 0.18.1.

- Fix signature of methods:

  - `~travertine.Program.add_branching_procedure_with_validity_pred`:meth:,
  - `~travertine.Program.add_branching_procedure_with_execution_pred`:meth:,
  - `~travertine.Program.add_branching_procedure_with_quantity_pred`:meth:,
  - `~travertine.Program.add_branching_procedure_with_match_attr_pred`:meth:, and
  - `~travertine.Program.add_branching_procedure_with_attr_in_range_pred`:meth:

  all their arguments are non-optional and positional-only.


2023-01-25.  Release 0.39.0
---------------------------

- Upgrade to PyO3 0.18.0.  Produce wheels for Python 3.11.

2022-07-18.  Release 0.38.0
---------------------------

- Allow variables in formulae to be unquoted if they only contain letters
  (a-z), digits (0-9) and/or underscore (_), and they start with a letter.

- Expose `travertine.floats.float_round`:func: (rust implemented) to Python
  code and use it in `~travertine.procedures.RoundProcedure`:class:.


2022-04-11.  Release 0.37.0
---------------------------

- Upgrade to PyO3 0.16.3


2022-03-22.  Release 0.36.0
---------------------------

- Upgrade to PyO3 0.15.1
- Allow xotless 3.5+


2021-12-17.  Release 0.35.0
---------------------------

- Don't raise an AssertionError for issue `#13`_.  We haven't fix the
  underlying issue, but not raising the assert will allow the users to get,
  albeit partially, the price tables.

.. _#13: https://gitlab.merchise.org/mercurio-2018/travertine/-/issues/13


2021-11-14.  Release 0.34.0
---------------------------

- Make sure all procedure classes have a ``__slots__``, and thus cannot be
  assigned extra attributes.

- Fix issue `#12`_: A KeyError was raised when generating price tables of
  procedures that didn't share an attribute configured
  `~travertine.tables.ATTR_FORMAT.BY_VALUE`:attr: in the table format.

.. _#12: https://gitlab.merchise.org/mercurio-2018/travertine/-/issues/12

2021-10-26.  Release 0.33.0
---------------------------

- Added support for Python 3.10.


2021-10-01.  Release 0.32.0
---------------------------

- Use `xotless.tracing`:mod: to trace portions of price computation
  algorithms and price tables.

2021-09-09.  Release 0.31.0
---------------------------

- Use xotl.tools 2.2.0+.

- Fix issue `#10`_: Travertine fails in Python 3.9.7 after `bpo-44806`_.

.. _#10: https://gitlab.merchise.org/mercurio-2018/travertine/-/issues/10
.. _bpo-44806: https://bugs.python.org/issue44806


2021-08-28.  Release 0.30.0
---------------------------

- Fix issue `xhg2#1818`__:

  When generating tables of different procedures, if some of them didn't share
  the same set of values being used in a column configured to be rendered
  `~travertine.tables.ATTR_FORMAT.BY_VALUE`:attr:, the rows of each procedure
  could produce a shorter amount of cells instead of using
  `~travertine.tables.MISSING_CELL`:obj:.

  This could create completely wrong rows because they could be displaced
  under the wrong header.  For example, if procedures A and B share a
  'regimen' attribute, but the procedure's AVM would yield values CP and MAP,
  and the second procedures's would yield values MAP and TI; the *right* table
  would look like::

      |  CP    |   MAP  |   TI   |  Attr
      +--------+--------+--------+-------
      |  $ 1   |  $ 2   |   ---  |  val
      +--------+--------+--------+-------
      |  ---   |  $ 3   |   $ 4  |  val

  However, this bug caused to be like::

      |  CP    |   MAP  |   TI   |  Attr
      +--------+--------+--------+-------
      |  $ 1   |  $ 2   |  val   |
      +--------+--------+--------+-------
      |  $ 3   |  $ 4   |  val   |

  The second row would be completely displaced, and the 'val' belonging under
  'Attr' would also be shifted in both cases.

  __ https://gitlab.merchise.org/mercurio-2018/xhg2/-/issues/1818


2021-07-29.  Release 0.29.0
---------------------------

- Add ``order`` to `travertine.types.TypedAttribute`:class:.  The class
  methods `travertine.types.AttributeLocator.of_demand`:any:,
  `travertine.types.AttributeLocator.of_request`:any:, and
  `travertine.types.AttributeLocator.of_commodity`:any: were updated
  accordingly.


2021-05-27.  Release 0.28.0
---------------------------

- Add ``find_by_value`` to `travertine.types.SimpleType`:class: and use it
  print the names of simple selections in price tables.


2021-03-11.  Release 0.27.0
---------------------------

- Ensure that the constant ``travertine.types.Undefined`` is not translated in
  `repr`:func:.


2021-02-12.  Release 0.26.0
---------------------------

- Mitigate issue `#1500 of xhg2`__.  FormulaProcedures are being created
  without all sub-procedures.  We simply return Undefined in such cases.

  __ https://gitlab.merchise.org/mercurio-2018/xhg2/-/issues/1500

2020-12-29. Release 0.25.1
--------------------------

- Fixes missing ``__module__`` for types implemented in Rust:

  - `travertine.Program`:class:,
  - `travertine.ExternalObject`:class:, and
  - `travertine.UnitaryDemand`:class:.

2020-12-29.  Release 0.25.0
---------------------------

- Update to `PyO3 0.13.0`__.

  __ https://docs.rs/pyo3/0.13.0/pyo3/


2020-12-05.  Release 0.24.0
---------------------------

- Add support for internationalization in `travertine.i18n`:mod:.

- Run doctests in the CI pipeline to ensure they are truly working examples.


2020-11-18.  Release 0.23.0
---------------------------

- Fix issue `#8`__: TypeError: 'float' object cannot be interpreted as an
  integer.

  Even though the attribute ``quantity`` of `!travertine.types.Request`:class:
  type is expected to be an integer, we're getting float numbers from one of
  our client projects.

  We updated `~travertine.splitters.UnitSplitter`:class: and
  `~travertine.splitters.UnitRequestSplitter`:class: to allow for float
  quantities.  The behaviour is iterate by excess: the quantity 1.1 will
  iterate two times, each with value of 1.0.

  __ https://gitlab.merchise.org/mercurio-2018/travertine/-/issues/8


2020-11-11.  Release 0.22.0
---------------------------

- Fix issue `#5`__: TypeError: Can't convert Infinity to PyDateTime

  This error happens when a predicate is boundless (e.g
  ``ValidityPredicate(None, datetime.utcnow())``).

  __ https://gitlab.merchise.org/mercurio-2018/travertine/-/issues/5

2020-11-02.  Release 0.21.0
---------------------------

- Update to hypothesis 5.26+, and xotless 3.0.0.

2020-10-27.  Release 0.20.0
---------------------------

- No visible changes.

  Build the wheel for Python 3.8 and 3.9.  Also uses Rust 1.47 to compile and
  upgrade several dependencies including PyO3.


2020-10-26.  Release 0.19.0
---------------------------

- Report the values of variables used in a `formula
  <travertine.procedures.FormulaProcedure>`:class: as sub-results.

2020-10-19.  Release 0.18.0
---------------------------

- Don't turn every exception while executing a
  `~travertine.procedures.FormulaProcedure`:class: into Undefined.  That may
  hide bugs from external code.

  See https://sentry.merchise.org/share/issue/8713fffcd8794bc9b24373489f67f079/

2020-09-22.  Release 0.17.0
---------------------------

- Fix transpilation of unary negation in
  `~travertine.procedures.FormulaProcedure`:class:.

  Trying to compile a formula like ``-'var'`` failed with a TypeError.  This
  error didn't affected the Rust runtime.


2020-09-21.  Release 0.16.0
---------------------------

- `travertine.MatrixProcedure.add_row`:meth: now accepts a formula without
  substeps indexes as the result of a row.


2020-09-16.  Release 0.15.0
---------------------------

- Update to `PyO3 0.12.0`__, which means that
  `travertine.ExternalObject`:class: doesn't raise a TypeError when compared
  to other type of object.

  __ https://docs.rs/pyo3/0.12.0/pyo3/


2020-08-31.  Release 0.14.0
---------------------------

- Integrate with `Celery's`__ SoftTimeLimitException_ to reraise it if caught
  in any of our code.

__ https://docs.celeryproject.org/en/stable/

.. _SoftTimeLimitException: https://github.com/celery/billiard/blob/3f9a8b0600de061077bbfe3e19a922163049942a/billiard/exceptions.py#L31



2020-08-19.  Release 0.13.0
---------------------------

- Fix IndexError while translating branching procedures without branches.


2020-08-16.  Release 0.12.0
---------------------------

- Reduce the amount of calls to hash while computing prices using the Python
  runtime.  This greatly improves the performance of price computations.
  Because part of our algorithm to generate price tables is still done in
  Python, this change makes both implementations comparable.


2020-08-05.  Release 0.11.0
---------------------------

- Add parameter `table_format` to
  `~travertine.tables.estimate_table_size`:func:.  Now this functions estimate
  the number of rows in the price tables.


2020-08-05.  Release 0.10.0
---------------------------

- Build wheel with Rust stable (using PyO3 0.11+)

- Actually enable parallelism by running potentially parallel code
  with ``Python::allow_threads``.

  I'm seeing only marginal usage of Rayon threads.  Which indicates that with
  travertine, computing prices is *the fastest* part of the code.  Most of the
  time is being spent by Python collecting the results.


2020-08-04.  Release 0.9.0
--------------------------

- Add property `travertine.tables.TableFormat.flattened`:attr:.


2020-08-04.  Release 0.8.0
--------------------------

- Remove parameter ``single_table`` from
  `~travertine.tables.generate_tables`:func:.

- Add attribute `travertine.tables.Table.name`:attr:.

- `~travertine.Program.execute_many`:meth: may compute the prices in parallel
  using `Rayon`_.

.. _Rayon: https://crates.io/crates/rayon


2020-08-01.  Release 0.7.0
--------------------------

- Complete translation of `~travertine.procedures.RoundProcedure`:class:.  Now
  we translate correctly the `method` argument so that the results match the
  Python implementation.

  At least, we hope so.  We rely on `rust_decimal`__ to implement the same
  rounding strategies.

  __ https://crates.io/crates/rust_decimal

- Provide a basic Rust-only implementation of
  `travertine.matrix.MatrixProcedure`:class: so that we can build it and use
  `~travertine.Program.add_matrix_procedure`:func:.


2020-07-29.  Release 0.6.0
--------------------------

- Add an API for user-controlled staged computation of programs.  The API is
  embodied by the:

  - new parameter `base_program` to `~travertine.create_program`:func:, and

  - the class `travertine.ProgramPseudoProcedure`:class:

- Add parameter `rust_runtime` to `~travertine.tables.generate_tables`:func:
  to allow you to pass already computed `programs
  <travertine.Program>`:class:.


2020-07-28.  Release 0.5.0
--------------------------

- Correct conversion to `~travertine.structs.UnitaryDemand`:class: when
  computing price tables.

  The attributes which were not already converted to admissible types
  (`float`:class:, `int`:class:, `str`:class:, `~datetime.datetime`:class:,
  `~datetime.timedelta`:class:, `~travertine.ExternalObject`:class:) were
  being ignored.

  Instead we now first apply `protocol
  <api-to_travertine_external_object>`:ref: and ignore invalid values only
  after conversion.

- Mitigate translation of invalid SetEnvProcedure and SetFallbackEnvProcedure
  due to `invalid arguments`__.

  __ https://sentry.merchise.org/share/issue/b8ef54bc854d447b8f9503b001eea41d/


2020-07-28.  Release 0.4.0
--------------------------

- Provide more facilities in `travertine.testing`:mod:.


2020-07-27.  Release 0.3.0
--------------------------

- Add an `API protocol <api-to_travertine_external_object>`:ref: to convert from
  arbitrary external objects to instances of
  `~travertine.ExternalObject`:class:.

  The predicates `~travertine.predicates.MatchesAttributePredicate`:class: and
  `~travertine.predicates.AttributeInRangePredicate`:class: use this protocol
  to ensure its arguments are properly converted.


2020-07-27.  Release 0.2.0
--------------------------

- Change `travertine.tables.generate_tables`:func: to take an argument
  `chunk_size` so that we can buffer the computation of that many rows before
  yielding.

  This function gained a temporary `_use_rust_runtime` argument to opt-in the
  generation of price tables using the Rust runtime.

  With this release we can now test generating price tables using Rust.


2020-07-25.  Release 0.1.1
--------------------------

Make the package comply with PEP :pep:`0561` and remove the tests from the
wheel.


2020-07-24.  Release 0.1.0
--------------------------

Implements the basic procedures in Rust.  The goal is to be able to produce
price tables using `travertine.Program.execute_many`:meth:.

Ports almost all the Python runtime to travertine so that we can iterate and
compare the previous stable implementation with the one in Rust.

This is release is not yet ready for production.  Price tables are still
computed in Python.  The goal of this release is to allow xhg2 to include
travertine and replace the the xhg2's Python runtime, with the travertine's
Python runtime.  Baby steps.
