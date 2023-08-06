import hashlib
from dataclasses import dataclass

from .isql_struct import ISqlStruct


class UUID(ISqlStruct):
    def get_sql_hash(self) -> bytes:
        return hashlib.md5(b"0").digest()


@dataclass
class VARCHAR(ISqlStruct):
    max_length: int

    def get_sql_hash(self) -> bytes:
        return hashlib.md5(str(self.max_length).encode()).digest()


COLUMN_TYPE = UUID | VARCHAR


@dataclass
class Column(ISqlStruct):
    name: str
    type: COLUMN_TYPE

    def get_sql_hash(self) -> bytes:
        h = hashlib.md5(self.type.get_sql_hash())
        h.update(self.name.encode())
        return h.digest()
