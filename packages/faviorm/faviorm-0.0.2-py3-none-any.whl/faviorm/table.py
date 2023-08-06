import hashlib

from .column import Column
from .isql_struct import ISqlStruct


class Table(ISqlStruct):
    table_name: str

    def __init__(self, name: str) -> None:
        self.table_name = name

    def get_columns(self) -> list[Column]:
        columns = []
        for key in dir(self):
            v = getattr(self, key)
            if isinstance(v, Column):
                columns.append(v)
        return columns

    def get_sql_hash(self) -> bytes:
        h = hashlib.md5(self.table_name.encode())
        for c in self.get_columns():
            h.update(c.get_sql_hash())
        return h.digest()
