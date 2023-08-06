from abc import ABC, abstractmethod


class ISqlStruct(ABC):
    @abstractmethod
    def get_sql_hash(self) -> bytes:
        pass
