from typing import List, Optional

import sql_metadata
from sql_metadata import Parser, QueryType

DDL = {QueryType.CREATE, QueryType.DROP, QueryType.ALTER, QueryType.SELECT}
DML = {QueryType.INSERT, QueryType.UPDATE, QueryType.DELETE}


class ParseSqlError(Exception):
    ...


class UnsupportedQueryType(ParseSqlError):
    ...


class SqlStatement:
    def __init__(self, sql: str, skip_wc: bool = True):
        self.inputs: Optional[List[str]] = []
        self.outputs: Optional[List[str]] = []
        self.comments: Optional[List[str]] = []
        self.skip_wc = skip_wc

        self._columns: Optional[List[str]] = []
        self._sql = sql

        self.parse_sql()

    @property
    def columns(self) -> List[str]:
        return self._columns

    @columns.setter
    def columns(self, columns: List[str]):
        if self.skip_wc:
            self._columns = [col for col in columns if "*" not in col]
        else:
            self._columns = columns

    def parse_sql(self) -> None:
        parser = sql_metadata.Parser(self._sql)

        try:
            query_type: str = parser.query_type

            if query_type in DDL:
                self.__parse_ddl(parser)
            elif query_type in DML:
                self.__parse_dml(parser)
            else:
                raise ValueError(f"Unsupported type {query_type}")

            self.comments = parser.comments

        except ValueError as e:
            raise UnsupportedQueryType from e

    def __parse_dml(self, parser: Parser):
        self.outputs = parser.tables
        self.columns = parser.columns

    def __parse_ddl(self, parser: Parser):
        self.inputs = parser.tables
        self.columns = parser.columns
