"""
Filename: content_extractor.py
Author: Rhavy Frota
Date: 10/03/2025
Version: 0.1
Description:
    This file defines the default interface for
    a document processing engine.

Contact: rhavy.souza1@hp.com
"""

from abc import ABC
from abc import abstractmethod
from io import BytesIO
from pathlib import Path

from document_relayout.core.hp_document import HPDocument


class BaseEngine(ABC):
    @abstractmethod
    def _process_from_bytes_io(self, b_io: BytesIO) -> HPDocument:
        raise NotImplementedError

    def _process_from_path(self, path: str) -> HPDocument:
        # TODO investigate possible issues ('rb' mode? and missing 'encoding' param)
        with Path.open(path, "rb") as f:
            return self._process_from_bytes_io(BytesIO(f.read()))

    def process(self, file: str | BytesIO):
        if type(file) is str:
            return self._process_from_path(file)
        return self._process_from_bytes_io(file)
