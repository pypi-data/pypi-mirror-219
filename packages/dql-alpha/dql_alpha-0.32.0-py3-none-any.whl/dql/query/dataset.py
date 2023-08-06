import os
import random
import string
from abc import ABC, abstractmethod
from copy import copy
from typing import TYPE_CHECKING, Iterable, List, Optional, TypeVar

import sqlalchemy
from sqlalchemy.sql.expression import label

from dql.catalog import get_catalog
from dql.data_storage.schema import DATASET_CORE_COLUMN_NAMES
from dql.data_storage.schema import DatasetRow as DatasetRowSchema
from dql.dataset import DatasetRow
from dql.dataset import Status as DatasetStatus

from .schema import C
from .udf import UDFType

if TYPE_CHECKING:
    from sqlalchemy.sql.base import Executable
    from sqlalchemy.sql.elements import ColumnElement

    from dql.catalog import Catalog
    from dql.query.udf import Generator


BATCH_SIZE = 1000


class StartingStep(ABC):
    """An initial query processing step, referencing a data source."""

    @abstractmethod
    def apply(self) -> "QueryGenerator":
        ...


class Step(ABC):
    """A query processing step (filtering, mutation, etc.)"""

    @abstractmethod
    def apply(self, query: "Executable") -> "QueryGenerator":
        """Apply the processing step."""


class QueryStep(StartingStep):
    def __init__(self, table):
        self.table = table

    def apply(self):
        """Return the query for the table the query refers to."""
        table = self.table

        def q(*columns):
            return sqlalchemy.select(*columns)

        return QueryGenerator(q, table.c)


class IndexingStep(StartingStep):
    def __init__(self, path, catalog, **kwargs):
        self.path = path
        self.catalog = catalog
        self.kwargs = kwargs

    def apply(self):
        """Return the query for the table the query refers to."""
        self.catalog.index([self.path], **self.kwargs)
        client_config = self.kwargs.get("client_config") or {}
        client, path = self.catalog.parse_url(self.path, **client_config)
        uri = client.uri

        def q(*columns):
            col_names = [c.name for c in columns]
            return self.catalog.data_storage.nodes_dataset_query(
                column_names=col_names, path=path, recursive=True, uri=uri
            )

        nodes = self.catalog.data_storage.nodes_table(uri)
        dataset_columns = DatasetRowSchema.calculate_all_columns([nodes])

        return QueryGenerator(q, dataset_columns)


class QueryGenerator:
    def __init__(self, func, columns):
        self.func = func
        self.columns = columns

    def exclude(self, column_names):
        return self.func(*[c for c in self.columns if c.name not in column_names])

    def select(self, column_names=None):
        if column_names is None:
            return self.func(*self.columns)
        return self.func(*[c for c in self.columns if c.name in column_names])


class UDFSignal(Step):
    """Add a custom column to the result set."""

    def __init__(self, name: str, udf: UDFType, catalog: "Catalog"):
        self.catalog = catalog
        self.name = name
        self.udf = udf
        self.temp_table_name = f"udf_{self.name}_" + _random_string(6)

    def clone(self):
        return self.__class__(self.name, self.udf, self.catalog)

    def apply(self, query):
        if self.name in DATASET_CORE_COLUMN_NAMES:
            # populating a core dataset column
            return self.overwrite_existing(query)
        return self.new_column(query)

    def overwrite_existing(self, query):
        """Handler for udfs populating core columns (e.g. the checksum column)."""
        tbl, col = self.udf_results_table(query)
        # Construct a new query that will join the udf-generated partial table.

        subquery = query.subquery()
        q_cols = [c if c.name != self.name else col for c in subquery.c]

        def q(*columns):
            cols = []
            for c in columns:
                if c.name == col.name:
                    cols.append(col)
                else:
                    cols.append(c)

            q = subquery.join(tbl, tbl.c.id == subquery.c.id)
            if cols:
                return sqlalchemy.select(*cols).select_from(q)
            return sqlalchemy.select(cols).select_from(q)

        return QueryGenerator(q, q_cols)

    def new_column(self, query):
        """Handler for udfs adding custom signals."""
        tbl, col = self.udf_results_table(query)
        # Construct a new query that will join the udf-generated partial table.
        subq = query.subquery()

        def q(*columns):
            cols1 = []
            cols2 = []
            for c in columns:
                if c.name == col.name:
                    cols2.append(c)
                else:
                    cols1.append(c)

            if cols2:
                return (
                    sqlalchemy.select(*cols1)
                    .select_from(subq)
                    .join(tbl, tbl.c.id == subq.c.id)
                    .add_columns(*cols2)
                )
            return sqlalchemy.select(*cols1).select_from(subq)

        return QueryGenerator(q, [*subq.c, col])

    def udf_results_table(self, query):
        """
        Create and populate a temporary UDF results table, this table
        will have two columns:
         - id, for joining to the original query
         - {self.name}, for storing UDF results.
        """
        execute = self.catalog.data_storage.execute

        id_cols = [c for c in query.selected_columns if c.name == "id"]
        col = sqlalchemy.Column(self.name, self.udf.output_type, nullable=True)
        tbl = self.catalog.data_storage.create_udf_table(
            self.temp_table_name,
            id_cols[0].type,
            [col],
        )
        selected_columns = [col.name for col in query.selected_columns]
        results = (
            DatasetRow.from_result_row(selected_columns, r) for r in execute(query)
        )
        rows = []
        for row in results:
            signal = {self.name: self.udf(self.catalog, row)}
            rows.append(dict(id=row.id, **signal))
            if len(rows) > BATCH_SIZE:
                update = tbl.insert().values(rows)
                execute(update)
                rows.clear()
        if rows:
            update = tbl.insert().values(rows)
            execute(update)
        return tbl, col


class RowGenerator(Step):
    """Extend dataset with new rows."""

    def __init__(self, generator: "Generator", catalog: "Catalog"):
        self.generator = generator
        self.catalog = catalog
        self.engine = catalog.data_storage.engine

    def clone(self):
        return self.__class__(self.generator, self.catalog)

    def apply(self, query):
        # Create a temporary table.
        temp_table_name = "generated_" + _random_string(6)
        selected_columns = [col.name for col in query.selected_columns]
        custom_columns: List["sqlalchemy.Column"] = [
            sqlalchemy.Column(col.name, col.type)
            for col in query.selected_columns
            if col.name not in DATASET_CORE_COLUMN_NAMES
        ]
        self.catalog.data_storage.create_dataset_rows_table(
            temp_table_name,
            custom_columns=custom_columns,
            if_not_exists=False,
        )
        tbl = self.catalog.data_storage.get_table(temp_table_name)

        execute = self.catalog.data_storage.execute

        results = (
            DatasetRow.from_result_row(selected_columns, r) for r in execute(query)
        )
        rows = []
        for row in results:
            for new_entry in self.generator(self.catalog, row):
                rows.append(new_entry)
                if len(rows) >= BATCH_SIZE:
                    execute(tbl.insert().values(rows))
                    rows.clear()
        if rows:
            execute(tbl.insert().values(rows))

        original_query = query.subquery()
        table_query = tbl.select().subquery()
        original_cols = [label(c.name, c) for c in original_query.columns]
        table_cols = [label(c.name, c) for c in table_query.columns]

        def q(*columns):
            names = {c.name for c in columns}
            cols1 = [c for c in original_cols if c.name in names]
            cols2 = [
                c for c in table_cols if c.name in names
            ]  # Columns for the generated table.
            q = sqlalchemy.union_all(
                sqlalchemy.select(*cols1).select_from(original_query),
                sqlalchemy.select(*cols2).select_from(table_query),
            )
            return q

        return QueryGenerator(q, [*original_cols])


class SQLClause(Step, ABC):
    def apply(self, query):
        new_query = self.apply_sql_clause(query)

        def q(*columns):
            return new_query.with_only_columns(*columns)

        return QueryGenerator(q, new_query.selected_columns)

    @abstractmethod
    def apply_sql_clause(self, query):
        pass


class SQLSelect(SQLClause):
    def __init__(self, *args):  # pylint: disable=super-init-not-called
        self.args = args

    def apply_sql_clause(self, query):
        subquery = query.subquery()
        args = self.args
        if not args:
            args = subquery.c
        return sqlalchemy.select(*args).select_from(subquery)


class SQLMutate(SQLClause):
    def __init__(self, *args):  # pylint: disable=super-init-not-called
        self.args = args

    def apply_sql_clause(self, query):
        subquery = query.subquery()
        return sqlalchemy.select(*subquery.c, *self.args).select_from(subquery)


class SQLFilter(SQLClause):
    def __init__(self, *args):  # pylint: disable=super-init-not-called
        self.expressions = args

    def __and__(self, other):
        return self.__class__(*(self.expressions + other))

    def apply_sql_clause(self, query):
        return query.filter(*self.expressions)


class SQLOrderBy(SQLClause):
    def __init__(self, *args):  # pylint: disable=super-init-not-called
        self.args = args

    def apply_sql_clause(self, query):
        return query.order_by(*self.args)


class SQLLimit(SQLClause):
    def __init__(self, n: int):  # pylint: disable=super-init-not-called
        self.n: int = n

    def apply_sql_clause(self, query):
        return query.limit(self.n)


class SQLUnion(Step):
    def __init__(self, query1, query2):
        self.query1 = query1
        self.query2 = query2

    def apply(self, query):
        q1 = self.query1.apply_steps().select().subquery()
        q2 = self.query2.apply_steps().select().subquery()
        columns1, columns2 = fill_columns(q1.columns, q2.columns)

        def q(*columns):
            names = {c.name for c in columns}
            col1 = [c for c in columns1 if c.name in names]
            col2 = [c for c in columns2 if c.name in names]
            return (
                sqlalchemy.select(*col1)
                .select_from(q1)
                .union_all(sqlalchemy.select(*col2).select_from(q2))
            )

        return QueryGenerator(q, columns1)


def fill_columns(
    *column_iterables: Iterable["ColumnElement"],
) -> List[List["ColumnElement"]]:
    column_dicts = [{c.name: c for c in columns} for columns in column_iterables]
    combined_columns = {n: c for col_dict in column_dicts for n, c in col_dict.items()}

    result: List[List["ColumnElement"]] = [[] for _ in column_dicts]
    for n in combined_columns:
        col = next(col_dict[n] for col_dict in column_dicts if n in col_dict)
        for col_dict, out in zip(column_dicts, result):
            if n in col_dict:
                out.append(col_dict[n])
            else:
                # Cast the NULL to ensure all columns are aware of their type
                # Label it to ensure it's aware of its name
                out.append(sqlalchemy.cast(sqlalchemy.null(), col.type).label(n))
    return result


SQLQueryT = TypeVar("SQLQueryT", bound="SQLQuery")


class SQLQuery:
    def __init__(
        self,
        starting_step: StartingStep,
        steps: Optional[Iterable["Step"]] = None,
        catalog: Optional["Catalog"] = None,
        client_config=None,
    ):  # pylint: disable=super-init-not-called
        self.steps: List["Step"] = list(steps) if steps is not None else []
        self.starting_step: StartingStep = starting_step
        self.catalog = catalog or get_catalog(client_config=client_config)
        self._chunk_index: Optional[int] = None
        self._chunk_total: Optional[int] = None
        self._temp_tables: List[str] = []

    def __iter__(self):
        return iter(self.results())

    def __or__(self, other):
        return self.union(other)

    def apply_steps(self):
        """
        Apply the steps in the query and return the resulting
        sqlalchemy.Executable.
        """
        query = self.clone()

        index = os.getenv("DQL_QUERY_CHUNK_INDEX", self._chunk_index)
        total = os.getenv("DQL_QUERY_CHUNK_TOTAL", self._chunk_total)

        if None not in (index, total):
            index, total = int(index), int(total)  # os.getenv returns str

            if not (0 <= index < total):
                raise ValueError("chunk index must be between 0 and total")

            # Prepend the chunk filter to the step chain.
            query = query.filter(C.random % total == index)
            query.steps = query.steps[-1:] + query.steps[:-1]

        generator = query.starting_step.apply()
        for step in query.steps:
            generator = step.apply(
                generator.select()
            )  # a chain of steps linked by results
        return generator

    def results(self, row_factory=None, **kwargs):
        query = self.apply_steps()
        execute = self.catalog.data_storage.data_execute

        query = query.select()
        if row_factory:
            selected_columns = [col.name for col in query.selected_columns]
            result = [
                row_factory(selected_columns, r) for r in execute(query, **kwargs)
            ]
        else:
            result = list(execute(query, **kwargs))
        self.catalog.data_storage.cleanup_temp_tables(self._temp_tables)
        return result

    def clone(self: SQLQueryT) -> SQLQueryT:
        obj = copy(self)
        obj.steps = obj.steps.copy()
        return obj

    def select(self, *args, **kwargs):
        """
        Select the given columns or expressions from this query.

        If used with no arguments, this simply creates a subqery and
        select all columns from it.

        Note that the `save` function expects default dataset columns to
        be present. This function is meant to be followed by a call to
        `results` if used to exclude any default columns.

        Example:
            >>> ds.select(C.name, C.size * 10).results()
            >>> ds.select(C.name, size10x=C.size * 10).order_by(C.size10x).results()
        """
        named_args = [v.label(k) for k, v in kwargs.items()]
        query = self.clone()
        query.steps.append(SQLSelect(*args, *named_args))
        return query

    def mutate(self, **kwargs):
        """
        Add new columns to this query.

        This function selects all existing columns from this query and
        adds in the new columns specified.

        Example:
            >>> ds.mutate(size10x=C.size * 10).order_by(C.size10x).results()
        """
        args = [v.label(k) for k, v in kwargs.items()]
        query = self.clone()
        query.steps.append(SQLMutate(*args))
        return query

    def filter(self, *args):
        query = self.clone()
        steps = query.steps
        if steps and isinstance(steps[-1], SQLFilter):
            steps[-1] = steps[-1] & args
        else:
            steps.append(SQLFilter(*args))
        return query

    def order_by(self, *args):
        query = self.clone()
        query.steps.append(SQLOrderBy(*args))
        return query

    def limit(self, n: int):
        query = self.clone()
        query.steps.append(SQLLimit(n))
        return query

    def union(self, dataset_query):
        left = self.clone()
        right = dataset_query.clone()
        new_query = self.clone()
        new_query.steps = [SQLUnion(left, right)]
        return new_query

    def chunk(self, index: int, total: int):
        """Split a query into smaller chunks for e.g. parallelization.
        Example:
            >>> query = DatasetQuery(...)
            >>> chunk_1 = query._chunk(0, 2)
            >>> chunk_2 = query._chunk(1, 2)
        Note:
            Bear in mind that `index` is 0-indexed but `total` isn't.
            Use 0/3, 1/3 and 2/3, not 1/3, 2/3 and 3/3.
        """
        query = self.clone()
        query._chunk_index, query._chunk_total = index, total
        return query


class DatasetQuery(SQLQuery):
    def __init__(
        self,
        path: str = "",
        name: str = "",
        version: Optional[int] = None,
        catalog=None,
        client_config=None,
    ):
        if catalog is None:
            catalog = get_catalog(client_config=client_config)

        data_storage = catalog.data_storage
        starting_step: StartingStep
        if path:
            starting_step = IndexingStep(path, catalog, client_config=client_config)
        elif name:
            ds = data_storage.get_dataset(name)
            version = version or ds.latest_version
            ds_table = catalog.data_storage.get_table(
                data_storage.dataset_table_name(dataset_id=ds.id, version=version)
            )
            starting_step = QueryStep(ds_table)
        else:
            raise ValueError("must provide path or name")

        super().__init__(
            starting_step=starting_step, catalog=catalog, client_config=client_config
        )

    def add_signal(self, udf: UDFType, name: Optional[str] = None):
        query = self.clone()
        steps = query.steps
        column_name = name or getattr(udf, "column", None)
        if not column_name:
            raise ValueError("column name not specified")
        signal = UDFSignal(column_name, udf, self.catalog)
        steps.append(signal)
        self._temp_tables.append(signal.temp_table_name)
        return query

    def generate(self, generator: "Generator"):
        query = self.clone()
        steps = query.steps
        steps.append(RowGenerator(generator, self.catalog))
        return query

    def save(self, name: str, **kwargs):
        """Save the query as a shadow dataset."""
        query = self.apply_steps()

        # Save to a temporary table first.
        temp_table_name = f"tmp_{name}_" + _random_string(6)
        custom_columns: List["sqlalchemy.Column"] = [
            sqlalchemy.Column(col.name, col.type)
            for col in query.columns
            if col.name not in DATASET_CORE_COLUMN_NAMES
        ]
        self.catalog.data_storage.create_dataset_rows_table(
            temp_table_name,
            custom_columns=custom_columns,
            if_not_exists=False,
        )
        temp_table = self.catalog.data_storage.get_table(temp_table_name)
        # Exclude the id column and let the db create it to avoid unique
        # constraint violations, and parent_id is not used in datasets.
        cols = [col.name for col in temp_table.c if col.name not in ("id", "parent_id")]

        self.catalog.data_storage.execute(
            sqlalchemy.insert(temp_table).from_select(
                cols, query.exclude(("id", "parent_id"))
            ),
            **kwargs,
        )

        # Create a shadow dataset.
        self.catalog.data_storage.create_shadow_dataset(name, create_rows=False)
        dataset = self.catalog.data_storage.get_dataset(name)
        if dataset is None:
            raise RuntimeError(f"No dataset found with {name=}")
        # pylint: disable=protected-access
        table_name = self.catalog.data_storage.dataset_table_name(dataset.id)

        self.catalog.data_storage._rename_table(temp_table_name, table_name)
        self.catalog.data_storage.update_dataset_status(dataset, DatasetStatus.COMPLETE)
        self.catalog.data_storage.cleanup_temp_tables(self._temp_tables)


T = TypeVar("T")


def return_ds(dataset_query: T) -> T:
    if isinstance(dataset_query, DatasetQuery):
        ds_id = _random_string(6)
        ds_name = f"ds_return_{ds_id}"
        dataset_query.catalog.data_storage.return_ds_hook(ds_name)
        dataset_query.save(ds_name)
    return dataset_query


def _random_string(length: int) -> str:
    return "".join(
        random.choice(string.ascii_letters + string.digits)  # nosec B311
        for i in range(length)
    )
