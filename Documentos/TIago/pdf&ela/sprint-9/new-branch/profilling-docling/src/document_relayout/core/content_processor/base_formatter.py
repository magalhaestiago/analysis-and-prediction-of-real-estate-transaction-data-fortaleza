from abc import ABC
from abc import abstractmethod

from document_relayout.core.hp_document import HPDocument


class BaseFormatter(ABC):
    @classmethod
    @abstractmethod
    def from_hp_doc(cls, document: HPDocument):
        raise NotImplementedError
