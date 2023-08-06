"""langchain_sql_test package."""
from importlib import metadata

from langchain_sql_test.chain import SQLDatabaseChain, SQLDatabaseSequentialChain
from langchain_sql_test.database import SQLDatabase
from langchain_sql_test.tool import (
    InfoSQLDatabaseTool,
    ListSQLDatabaseTool,
    QuerySQLCheckerTool,
    QuerySQLDataBaseTool,
)

try:
    __version__ = metadata.version(__package__)
except metadata.PackageNotFoundError:
    # Case where package metadata is not available.
    __version__ = ""

__all__ = [
    __version__,
    "SQLDatabaseChain",
    "SQLDatabaseSequentialChain",
    "SQLDatabase",
    "InfoSQLDatabaseTool",
    "ListSQLDatabaseTool",
    "QuerySQLCheckerTool",
    "QuerySQLDataBaseTool",
]
