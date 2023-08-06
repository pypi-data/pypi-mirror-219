import hashlib

from .isql_struct import ISqlStruct
from .table import Table


class Database(ISqlStruct):
    name: str
    tables: list[Table]

    def __init__(self, name: str) -> None:
        self.name = name

    def get_tables(self) -> list[Table]:
        tables = []
        for key in dir(self):
            v = getattr(self, key)
            if isinstance(v, Table):
                tables.append(v)
        return tables

    def get_sql_hash(self) -> bytes:
        h = hashlib.md5(self.name.encode())
        for t in self.get_tables():
            h.update(t.get_sql_hash())
        return h.digest()
