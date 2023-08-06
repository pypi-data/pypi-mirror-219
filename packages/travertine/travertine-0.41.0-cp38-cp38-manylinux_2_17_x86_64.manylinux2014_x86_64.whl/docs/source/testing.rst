===========================================================
 :mod:`travertine.testing` -- Utilities to test travertine
===========================================================

We provide classes, functions, Hypothesis_ strategies to test travertine,
there are several modules and packages.


Basic tools
===========

.. automodule:: travertine.testing.base
   :members: PriceCaseMixin, PriceCase, DomainCaseMixin


.. automodule:: travertine.testing.tables
   :members: generate_full_tables, read_table_rows, process_table_rows,
             process_row, process_cell


Hypothesis Strategies
=====================

.. automodule:: travertine.testing.strategies.programs
   :members: BasicProcedureMachine, ProcedureMachine, BasicProgramMachine,
             ProgramMachine


.. _hypothesis: https://hypothesis.readthedocs.io/en/latest/
