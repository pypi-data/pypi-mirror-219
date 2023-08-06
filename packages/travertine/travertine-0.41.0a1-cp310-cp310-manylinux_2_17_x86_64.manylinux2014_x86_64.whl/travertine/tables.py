#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
import logging
import typing as t
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import IntFlag
from itertools import groupby, product

from xotl.tools.fp.iterators import kleisli_compose_foldl
from xotl.tools.fp.tools import compose, fst
from xotl.tools.future.itertools import slides
from xotless.domains import EquivalenceSet
from xotless.tracing import get_module_sentry_spanner
from xotless.types import TEq as ProcedureName

from . import Program, create_program
from .avm import MergedAVM
from .i18n import _
from .structs import EMPTY_ENV, Commodity, Demand
from .types import (
    ATTRIBUTE_OWNER,
    AVM,
    AttributeLocator,
    Domain,
    Procedure,
    Result,
    TypedAttribute,
    Undefined,
)


class ATTR_FORMAT(IntFlag):
    """Describe the format of a single attribute in a `TableFormat`:class:

    Attributes could be formatted either BY_VALUE or BY_NAME:

    .. attribute:: BY_VALUE

       The attribute's value is put in the header of the column.  Cells below
       this column will contain the prices corresponding the column's value.

    .. attribute:: BY_NAME

       The attribute's name is put in the header of the column and its values
       in the cells.

    """

    BY_VALUE = 0b00
    BY_NAME = 0b01


@dataclass
class AttrFormatConfiguration:
    """The configuration of a group of attributes in a table format.

    .. attribute:: attrs

       The sequence of attributes this configuration applies.

    .. attribute:: how

       One of the possible values of `ATTR_FORMAT`:class:.

    .. attribute:: visible

       A boolean value indicating if the group should be visible.

    """

    __slots__ = ("attrs", "how", "visible")

    attrs: t.Sequence[AttributeLocator]
    how: ATTR_FORMAT
    visible: bool

    def __init__(
        self,
        attrs: t.Iterable[AttributeLocator] = None,
        how: ATTR_FORMAT = ATTR_FORMAT.BY_NAME,
        visible: bool = True,
    ) -> None:
        self.attrs = tuple(attrs) if attrs else ()
        self.how = how
        self.visible = visible

    @classmethod
    def from_locators(cls, *locators: AttributeLocator) -> "AttrFormatConfiguration":
        return cls(tuple(locators))

    def __bool__(self):
        return bool(self.attrs)


@dataclass
class TableFormat:
    """A price table format.

    A table format is described by two attributes:

    .. attribute:: tables_conf

       Describe a `group of attributes <AttrFormatConfiguration>`:class: which
       are used to create instances of `Table`:class:.  This allows to group the
       price tables in smaller chunks.  For instance, if you add the attribute
       ``date`` in this configuration you'll get a table per each interval of
       possible validity dates.

       The attributes `how` and `visible` of `AttrFormatConfiguration`:class:
       are ignored this group.

    .. attribute:: columns_conf

       This is sequence of `AttrFormatConfiguration`:class:.  Each item in the
       sequence represents a single column in the table format which comprises
       the attributes in the group.

       There can be a single group with `~ATTR_FORMAT.BY_VALUE`:attr:.

    The same attribute cannot appear more than once in the groups.

    If the procedures' AVMs contain more attributes which are not listed in
    the configuration, they are automatically appended, each in a single
    column with a format `~ATTR_FORMAT.BY_NAME`:attr:.

    If the configuration has attributes which are not part of procedures' AVMs
    they are usually ignored.  When one (or more) procedure passed to
    `generate_tables`:func: has the attribute while others don't, you may get
    the value `MISSING_CELL`:obj: in the rows of attributes configured
    `~ATTR_FORMAT.BY_NAME`:attr:.

    """

    __slots__ = ("tables_conf", "columns_conf")

    tables_conf: AttrFormatConfiguration
    columns_conf: t.Sequence[AttrFormatConfiguration]

    def needs_price_column(self, avm: AVM):
        """Return True if an AVM needs a standalone Price column."""
        return not any(
            column_attr in avm
            for column in self.columns_conf
            if column.how == ATTR_FORMAT.BY_VALUE
            for column_attr in column.attrs
        )

    @classmethod
    def from_columns(cls, *columns: AttributeLocator) -> "TableFormat":
        """Create a configuration of a single table with ordered columns."""
        return cls(
            AttrFormatConfiguration(),
            tuple(AttrFormatConfiguration.from_locators(column) for column in columns),
        )

    @property
    def flattened(self) -> "TableFormat":
        """A flattened version of the format.

        A flattened version returns a single table, `tables_conf`:attr: are
        pushed down to the first columns `~ATTR_FORMAT.BY_NAME`:attr:.  Create
        a column per attribute in `!tables_conf`:attr:.

        .. versionadded:: 0.9.0

        """
        columns_conf = tuple(
            AttrFormatConfiguration.from_locators(column)
            for column in self.tables_conf.attrs
        ) + tuple(self.columns_conf)
        return type(self)(AttrFormatConfiguration(), columns_conf)


@dataclass(frozen=True)
class DemandData:
    __slots__ = ("attrs", "demand")

    attrs: t.Tuple[t.Tuple[AttributeLocator, Domain], ...]
    demand: Demand

    @classmethod
    def new(cls, now=None):
        return cls((), Demand.from_commodities([_ARBITRARY_COMMODITY], date=now))

    @property
    def attr_locators(self) -> t.Tuple[AttributeLocator, ...]:
        return tuple(locator for locator, _domain in self.attrs)

    @property
    def attr_names(self) -> t.Tuple[TypedAttribute, ...]:
        return tuple(locator.attr for locator, _domain in self.attrs)

    @property
    def attr_samples(self) -> t.Tuple[t.Any, ...]:
        return tuple(domain.sample for _loc, domain in self.attrs)

    def _extract_basic_values(self, attrs: t.Sequence[AttributeLocator]):
        """Extract the values of the `attrs` in the demand data.

        The order in `self.attrs` MUST BE COMPATIBLE with the order of the
        argument passed to parameter `attrs`.  This is for any two attributes
        A1, A2 appearing in both sequences, A1 is before A2 in `attrs` if and
        only if A1 is before A2 in `self.attrs`.

        Return a generator of the basic values.  The basic values are domains,
        or values of single-item domains.  An EquivalenceSet with a single
        value is flattened to its value.  Other instances yield the entire
        domain.

        """
        # NOTE: The expectation of COMPATIBLE order matches the way we
        # generate demands.  It has to do being the expected order of the
        # table_format.
        #
        # We order the attributes according to _get_table_avm_index and each
        # demand is generate following this order; so, when extracting the
        # basic values, following table index will be a compatible order.
        attrs = list(attrs)
        ours = list(self.attrs)
        while ours and attrs:
            locator, data = ours.pop(0)
            if locator == attrs[0]:
                attrs.pop(0)
                if isinstance(data, EquivalenceSet):
                    if len(data.values) == 1:
                        yield _map_value_to_selection(locator, data.sample)
                    else:
                        yield _map_eqset_to_selection(locator, data)
                else:
                    yield data

    def getattr(self, locator: AttributeLocator):
        if locator.owner == ATTRIBUTE_OWNER.DEMAND:
            return getattr(self.demand, locator.attr.name)
        elif locator.owner == ATTRIBUTE_OWNER.REQUEST:
            return getattr(self.demand.requests[0], locator.attr.name)
        else:
            assert locator.owner == ATTRIBUTE_OWNER.COMMODITY
            return getattr(self.demand.requests[0].commodity, locator.attr.name)


@dataclass(frozen=True)
class Table:
    """A price table.

    This is the type of objects we get from `generate_tables`:func:

    """

    __slots__ = ("name", "attrs", "columns_headers", "rows")

    name: ProcedureName  # type: ignore
    attrs: t.Tuple[t.Tuple[AttributeLocator, t.Any], ...]
    columns_headers: t.Tuple[t.Any, ...]
    rows: t.Iterable[t.Tuple[t.Any, ...]]


NULL_FORMAT = TableFormat(AttrFormatConfiguration(), ())


def generate_tables(
    procedures: t.Sequence[t.Tuple[ProcedureName, Procedure]],
    table_format: TableFormat = NULL_FORMAT,
    now=None,
    pricecls: t.Callable[[Result], t.Any] = None,
    chunk_size: int = 1000,
    *,
    _use_rust_runtime: bool = False,
    rust_runtime: t.Optional[t.Mapping[Procedure, Program]] = None,
) -> t.Iterator[Table]:
    """Generates formatted price tables for many procedures.

    :param procedures: A sequence of pairs of ``(name, procedure)``.  The name is any
                       object that can be used to identify the procedure.  It's usually a
                       string, but that is not enforced.

    :param table_format: An instance of `TableFormat`:class: that describes how to group
           the prices in several tables and the layout of columns.  Refer to
           `TableFormat`:class: for a complete description.

           All the tables will have the same column layout even if the procedures don't
           have the same attributes in the AVM.  In such cases, the cell may contain the
           value `MISSING_CELL`:obj: when the column is configured with `BY_NAME
           <ATTR_FORMAT.BY_NAME>`:data:.

    :param now: Defaults to `datetime.datetime.utcnow`:meth:.  This is the value used to
                construct demands.  The AVM's may alter this value.

    :param pricecls: A callable which allows to *wrap* prices in the rows of the tables so
           that you can distinguish prices from non-prices values.  It defaults to the
           identity function (ie. no wrapping).  Example::

             >>> @dataclass
             ... class Price:
             ...     value: Result
             ...
             ...     def __str__(self):
             ...         return f'$ {self.value!s}'


    :param chunk_size: Allows you control an internal buffering of rows we keep before
           yielding the rows in each table.  This allows to compute prices using bulk
           operations which is much faster than computing each price on-demand.

    :param rust_runtime: If not None, it MUST be a mapping from procedures to
           `~travertine.Program`:class:.  If the `_use_rust_runtime` is True, use this
           mapping to look up the program for the `procedures`; if a procedure is not part
           of the mapping raise a KeyError.  If `_use_rust_runtime` is False, ignore this
           argument.

    :param _use_rust_runtime: If True, but `rust_runtime` is None, automatically `create
           <travertine.create_program>`:func: the programs.

    .. warning:: You must ensure that the programs in `rust_rustime` are
       actually a translation from the `procedures` otherwise you'll
       unexpected results.

    .. versionchanged:: 0.2.0 Added parameter `chunk_size`.

    .. versionchanged:: 0.2.0 Added provisional parameter `_use_rust_runtime`
       to opt-in tables generation using the Rust runtime.

    .. versionchanged:: 0.6.0 Added the parameter `rust_runtime` to profit
       from cache instances of `Program`.

    .. versionchanged:: 0.8.0 Removed parameter ``single_table``.
       `Table`:class: gained a new attribute `~Table.name`:attr: to identify
       the table.

       Computes the prices in parallel.

    """
    with sentry_span("generate_tables"):
        yield from _generate_tables(
            procedures,
            table_format=table_format,
            now=now,
            pricecls=pricecls,
            chunk_size=chunk_size,
            _use_rust_runtime=_use_rust_runtime,
            rust_runtime=rust_runtime,
        )


def estimate_table_size(
    procedures: t.Iterable[Procedure],
    *,
    table_format: TableFormat = NULL_FORMAT,
) -> int:
    """Return an estimate of the number of total rows to generated in the price
    tables.

    .. versionchanged:: 0.11.0 Add the parameter `table_format`, so that we
       can estimate the number of rows instead of the number of demands.

    """
    expanded_attrs = next(
        (
            tuple(conf.attrs)
            for conf in table_format.columns_conf
            if conf.how == ATTR_FORMAT.BY_VALUE
        ),
        (),
    )
    result = 0
    for procedure in procedures:
        size = 1
        for attr, domains in procedure.avm.items():
            # BY_VALUE columns contribute a single row to the price table, so
            # cannot multiply by the len of the domains, or we would severely
            # overestimate the size.
            if attr not in expanded_attrs:
                size *= len(domains)
        result += size
    return result


def _generate_tables(
    procedures: t.Sequence[t.Tuple[ProcedureName, Procedure]],
    *,
    table_format: TableFormat = NULL_FORMAT,
    now=None,
    pricecls: t.Callable[[Result], t.Any] = None,
    chunk_size: int = 1000,
    _use_rust_runtime: bool = False,
    rust_runtime: t.Optional[t.Mapping[Procedure, Program]] = None,
) -> t.Iterator[Table]:
    """Return an iterator of price tables.

    You may generate price tables for many `procedures`.  Each procedure is
    *identified* by a name of any type you like as long as different
    procedures have different names.

    """

    avm = MergedAVM(*(p.avm for _name, p in procedures))
    table_generators = [
        _get_demand_data_generator(attr, domains)
        for attr, domains in avm.items()
        if table_format.tables_conf and attr in table_format.tables_conf.attrs
    ]
    initial_demand_data = DemandData.new(now=now)
    if _use_rust_runtime:
        chunker = _chunk_and_resolve_in_rust
    else:
        chunker = _chunk_and_resolve_in_python
    for name, procedure in procedures:
        for demand_seed in kleisli_compose_foldl(*table_generators)(initial_demand_data):
            rows = chunker(
                _demand_datas(
                    demand_seed,
                    avm,
                    procedure,
                    name,
                    table_format=table_format,
                ),
                chunk_size=chunk_size,
                pricecls=pricecls,
                rust_runtime=rust_runtime,
            )
            headers = _get_headers(demand_seed, avm, table_format=table_format)
            yield Table(name, demand_seed.attrs, tuple(headers), rows)


def _get_columns(
    table: DemandData,
    avm: AVM,
    table_format: TableFormat = NULL_FORMAT,
) -> t.Dict[t.Tuple[AttributeLocator, ...], ATTR_FORMAT]:
    table_attrs = {attr for attr, _ in table.attrs if attr in avm}
    elegible_attrs = [attr for attr in avm if attr not in table_attrs]
    columns = {}
    for conf in table_format.columns_conf:
        attrs = tuple(attr for attr in conf.attrs if attr in elegible_attrs)
        if attrs:
            columns[attrs] = conf.how
    for attr in elegible_attrs:
        if not any(attr in key for key in columns):
            columns[(attr,)] = ATTR_FORMAT.BY_NAME
    return columns


def _get_headers(
    table: DemandData,
    avm: AVM,
    table_format: TableFormat = NULL_FORMAT,
):
    columns = _get_columns(table, avm, table_format)
    for locators, how in columns.items():
        if how == ATTR_FORMAT.BY_NAME:
            attrs = tuple(locator.attr for locator in locators)
            if len(attrs) == 1:
                yield attrs[0]
            else:
                yield attrs
        else:
            values = [
                _map_domain_to_selection(locator, avm[locator]) for locator in locators
            ]
            yield from product(*values)
    if table_format.needs_price_column(avm):
        yield _("Price")


def _map_value_to_selection(locator: AttributeLocator, value: t.Any) -> t.Any:
    """Extract the selection name of a value, given the locator is a SELECTION."""
    member = locator.attr.type.find_by_value(value)
    if member is not None:
        return member.name
    return value


def _map_domain_to_selection(
    locator: AttributeLocator,
    domains: t.Sequence[Domain],
) -> t.Sequence[t.Any]:
    """Extract domains of EquivalenceSet to selections if possible."""
    return tuple(_map_eqset_to_selection(locator, domain) for domain in domains)


def _map_eqset_to_selection(locator: AttributeLocator, domain: Domain) -> Domain:
    if isinstance(domain, EquivalenceSet):
        return EquivalenceSet(
            {_map_value_to_selection(locator, val) for val in domain.values}
        )
    else:
        return domain


def _demand_datas(
    table: DemandData,
    avm: AVM,
    procedure: Procedure,
    name: ProcedureName,
    table_format: TableFormat = NULL_FORMAT,
):
    proc_avm = procedure.avm
    key = _get_table_group_key(
        proc_avm,
        table_format,
        without_attrs={attr for attr, _ in table.attrs},
        with_value_columns=False,
    )
    table_attrs = {attr for attr, _ in table.attrs}
    columns = _get_columns(table, avm, table_format)
    demand_datas = generate_demand_datas(
        proc_avm,
        without_attrs=table_attrs,
        initial_demand_data=table,
        order_by=_get_table_avm_index(proc_avm, table_format),
    )
    for _key, datas in groupby(demand_datas, key=key):
        row: t.List[t.Any] = []
        price_computed = False
        # In a single row we can have several demand data when the
        # table has a BY_VALUE column configuration.  For instance:
        #
        #          |      Regime    |
        #          +--------+-------|
        #     Attr |  MAP   |   CP  |  Attr 2
        #     -----+--------+-------+---------
        #     xxx  |  $ 1   |  $ 2  |  yyyy
        #
        # Also we know that there must not be more than one BY_VALUE group of
        # attributes.  So we start with the first demand data, and at least
        # one configuration is BY_VALUE we put as many columns as items in
        # data.
        #
        # The alternative is that no column is BY_VALUE and we must
        # append a last column Price.
        #
        # There is one catch, though: When we're given an MergedAVM of several products
        # that don't the same set of the values of the BY_VALUES columns.
        #
        # For instance, let's the first product only have Regimen with CP, and the second
        # with MAP, we must produce a table like:
        #
        #          |      Regime    |
        #          +--------+-------|
        #     Attr |  MAP   |   CP  |  Attr 2
        #     -----+--------+-------+---------
        #     xxx  |  ---   |  $ 2  |  yyyy
        #     xxx  |  $ 1   |  ---  |  yyyy
        #
        data = next(datas)  # type: DemandData
        for attrs, how in columns.items():
            if how == ATTR_FORMAT.BY_NAME:
                # fmt: off
                cell = tuple(
                    data._extract_basic_values([attr]) if attr in proc_avm else MISSING_CELL
                    for attr in attrs
                )
                # fmt: on
                if len(cell) == 1:
                    row.append(cell[0])
                else:
                    row.append(cell)
            else:
                assert not price_computed
                price_computed = True
                # We need to check every possible combination of the attrs value in the
                # combined AVM and see if they all match the current's procedures AVM, if
                # they don't then we need to introduce a MISSING_CELL.
                #
                # Notice that we've already consumed one data (just before entering the
                # `for` loop above); this means we need to be sure this data matches the
                # first of values.
                #
                # We build a list of boolean columns that simply tells us if that column
                # matches the data.  In the example above the list will be `[False, True]`
                # on the first product and `[True, False]` on the second.
                matches = [
                    all(
                        (
                            any(
                                sample in d
                                for d in proc_avm[attr]
                                if (sample := domain.sample) is not None
                            )
                            if attr in proc_avm
                            else True
                        )
                        for (domain, attr) in column_attrs
                    )
                    for column_attrs in list(
                        product(
                            *([(domain, attr) for domain in avm[attr]] for attr in attrs)
                        )
                    )
                ]
                for match in matches:
                    if match:
                        row.append(PriceCell(procedure, data.demand))
                        # Leave the last data just in case there are BY_NAME attrs after
                        # the BY_VALUES
                        data = next(datas, data)
                    else:
                        row.append(MISSING_CELL)
        if not price_computed:
            row.append(PriceCell(procedure, data.demand))
        # The following should be an 'assert'.  Because of #13
        # (https://gitlab.merchise.org/mercurio-2018/travertine/-/issues/13) we're
        # currently switching to a log so that users a little less affected by our
        # mistakes.
        if (what := next(datas, Unset)) is not Unset:
            logger.error("Expecting Unset, found %s", what, exc_info=True)
        yield row


@dataclass
class PriceCell:
    """A placeholder for cells which contains prices.

    While computing the price tables the algorithm generates each rows but
    don't compute the price immediately.  Instead wherever a price is
    expected, it puts an instance of PriceCell to defer the actual computation
    so that we can collect and compute prices in bulk.

    This is faster than computing each price on-the-fly.

    """

    procedure: Procedure
    demand: Demand


def _get_table_avm_index(
    avm: AVM,
    table_format: TableFormat,
    without_attrs: t.Container[AttributeLocator] = None,
    with_value_columns=True,
) -> t.Sequence[AttributeLocator]:
    """Return an ordered sequence of the attributes according to the table format.

    Ignore attributes in `without_attrs`.

    If `with_value_columns` is True, include the ATTR_FORMAT.BY_VALUE as the
    last attributes in the index.

    The order is staged like this:

    - First came the attributes that make up whole tables.

    - Then all the attributes in the format's column configuration which are
      to be displayed by NAME (ignoring those not present in the AVM).

    - Next all attributes in the AVM which are not already ordered and are not
      in the columns configuration by VALUE.

    - Finally (if `with_value_columns` is True) the attributes to included by
      VALUE.

    """
    if not without_attrs:
        without_attrs = set([])
    index = tuple(
        attr
        for attr in table_format.tables_conf.attrs
        if attr in avm and attr not in without_attrs
    )
    index += tuple(
        attr
        for conf in table_format.columns_conf
        if conf.how == ATTR_FORMAT.BY_NAME
        for attr in conf.attrs
        if attr in avm and attr not in without_attrs
    )
    last_columns = tuple(
        attr
        for conf in table_format.columns_conf
        if conf.how == ATTR_FORMAT.BY_VALUE
        for attr in conf.attrs
        if attr in avm and attr not in without_attrs
    )
    seen_already = index + last_columns
    index += tuple(
        attr for attr in avm if attr not in without_attrs and attr not in seen_already
    )
    if with_value_columns:
        index += last_columns
    return index


def _get_table_group_key(
    avm: AVM,
    table_format: TableFormat,
    without_attrs: t.Container[AttributeLocator] = None,
    with_value_columns: bool = False,
):
    index = _get_table_avm_index(avm, table_format, without_attrs, with_value_columns)
    return lambda x: tuple(x.getattr(attr) for attr in index)


def generate_demand_datas(
    avm: AVM,
    order_by: t.Sequence[AttributeLocator],
    now=None,
    without_attrs: t.Container[AttributeLocator] = None,
    initial_demand_data: DemandData = None,
    table_format: TableFormat = NULL_FORMAT,
) -> t.Iterable[DemandData]:
    sort_key: t.Callable[[t.Tuple[AttributeLocator, t.Sequence[Domain]]], int] = compose(
        lambda attr: order_by.index(attr), fst  # type: ignore
    )
    generators = [
        _get_demand_data_generator(attr, domains)
        for attr, domains in sorted(avm.items(), key=sort_key)
        if not without_attrs or attr not in without_attrs
    ]
    if initial_demand_data is None:
        demand_data = DemandData(
            (),
            Demand.from_commodities([_ARBITRARY_COMMODITY], date=now),
        )
    else:
        demand_data = initial_demand_data
    return kleisli_compose_foldl(*generators)(demand_data)


_ARBITRARY_START_DATE = datetime(2021, 10, 21)
_ARBITRARY_COMMODITY = Commodity(_ARBITRARY_START_DATE, timedelta(0))


def _get_demand_data_generator(
    attr: AttributeLocator,
    domains: t.Sequence[t.Any],
) -> t.Callable[[DemandData], t.Iterable[DemandData]]:
    """Return a *generator* of demands for a given `attr` and domain sequence.

    The generator takes a single *demand data* and creates new demands by updating `attr`
    with different samples of the `domains`.

    """

    def result(demand_data: DemandData) -> t.Iterable[DemandData]:
        demand = demand_data.demand

        def _new_attrs(domain: Domain) -> t.Tuple[t.Tuple[AttributeLocator, t.Any], ...]:
            return demand_data.attrs + ((attr, domain),)

        for domain in domains:
            # It's possible that we get empty domains here because the AVM of
            # a trivially empty predicate (eg. QuantityPredicate(0, 0))
            # contains the empty domain.
            #
            # In such a case, we cannot actually get any sample from the
            # domain (it's empty); and then we cannot produce a valid demand.
            if domain:
                yield DemandData(
                    _new_attrs(domain),
                    attr.update(demand, domain.sample),
                )

    return result


def _chunk_and_resolve_in_python(
    rows: t.Iterable[t.Tuple[t.Any, ...]],
    chunk_size: int = 1000,
    pricecls: t.Callable[[Result], t.Any] = None,
    rust_runtime: t.Optional[t.Mapping[Procedure, Program]] = None,
) -> t.Iterable[t.Tuple[t.Any, ...]]:
    """Consumes rows by chunks and resolves price cells by computing prices.

    Externally the `rows` are given one by one.  Internally we eagerly consume
    the items in `rows` by `chunk_size` and compute the prices in those rows
    in bulk before yielding the result.

    """
    if pricecls is None:
        Price = lambda x: x  # noqa
    else:
        Price = pricecls
    for chunk in slides(rows, chunk_size, fill=Unset):
        # tally: maps the procedures to both the *coordinates* in the
        # `result` list and the demand.  This accumulates all the demands for
        # a procedure and the allows to replace PriceCell in `results`.
        tally: t.Dict[Procedure, t.Tuple[t.List[t.Tuple[int, int]], t.List[Demand]]] = {}
        result: t.List[t.List[t.Any]] = []  # accumulated rows
        for rowindex, row in enumerate(row for row in chunk if row is not Unset):
            result.append(list(row))  # type: ignore
            for colindex, cell in enumerate(row):  # type: ignore
                if isinstance(cell, PriceCell):
                    cells, demands = tally.setdefault(cell.procedure, ([], []))
                    cells.append((rowindex, colindex))
                    demands.append(cell.demand)
        for procedure, (cells, demands) in tally.items():
            with sentry_span("execute_many (Python)"):
                for (rowindex, colindex), demand in zip(cells, demands):
                    price = Price(procedure(demand, EMPTY_ENV).result)
                    result[rowindex][colindex] = price
        yield from iter(tuple(row) for row in result)


def _chunk_and_resolve_in_rust(
    rows: t.Iterable[t.Tuple[t.Any, ...]],
    chunk_size: int = 1000,
    pricecls: t.Callable[[Result], t.Any] = None,
    rust_runtime: t.Optional[t.Mapping[Procedure, Program]] = None,
) -> t.Iterable[t.Tuple[t.Any, ...]]:
    if pricecls is None:
        Price = lambda x: x  # noqa
    else:
        Price = pricecls
    for chunk in slides(rows, chunk_size, fill=Unset):
        # tally: maps the procedures to both the *coordinates* in the
        # `result` list and the demand.  This accumulates all the demands for
        # a procedure and the allows to replace PriceCell in `results`.
        tally: t.Dict[Procedure, t.Tuple[t.List[t.Tuple[int, int]], t.List[Demand]]] = {}
        if rust_runtime is not None:
            programs: t.Mapping[Procedure, Program] = rust_runtime
        else:
            programs = ProgramDict()
        result: t.List[t.List[t.Any]] = []  # accumulated rows
        for rowindex, row in enumerate(row for row in chunk if row is not Unset):
            result.append(list(row))  # type: ignore
            for colindex, cell in enumerate(row):  # type: ignore
                if isinstance(cell, PriceCell):
                    cells, demands = tally.setdefault(cell.procedure, ([], []))
                    cells.append((rowindex, colindex))
                    demands.append(cell.demand)
        for procedure, (cells, demands) in tally.items():
            program = programs[procedure]
            with sentry_span("execute_many (Rust)"):
                results = program.execute_many(
                    tuple(d.to_unitary_demand() for d in demands),
                    Undefined,
                )
            for (rowindex, colindex), price in zip(cells, results):
                result[rowindex][colindex] = Price(price)
        yield from iter(tuple(row) for row in result)


class ProgramDict(t.Dict[Procedure, Program]):
    """A dict that resolves procedures to programs.

    We implement ``__missing__`` so that it calls `travertine.create_program`:func: and
    store the result.  This allows to cache the `programs <travertine.Program>`:class:
    obtained from procedures.

    """

    def __missing__(self, key: Procedure) -> Program:
        self[key] = res = create_program(key)
        return res


HOUR = timedelta(hours=1)


class _MissingCell:
    def __repr__(self):
        return "NA"

    def __str__(self):
        return "-"


MISSING_CELL = _MissingCell()
sentry_span = get_module_sentry_spanner(__name__)
Unset = object()
logger = logging.getLogger(__name__)
