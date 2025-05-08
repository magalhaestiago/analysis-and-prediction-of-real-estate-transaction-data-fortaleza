"""
Filename: content_extractor.py
Author: Alan Bandeira
Date: 20/02/2025
Version: 0.1
Description:
    This file contains the api for document content
    extraction based on the docling library.

Contact: alan.bandeira1@hp.com
"""

# Imports
from dataclasses import dataclass

from PIL.PngImagePlugin import PngImageFile


@dataclass
class RasterDoc:
    """Class for manipulating raster image based PDF files."""

    pages: list[PngImageFile]


class ContentExtractor:
    """docstring"""

    def __init__(self):
        pass

    def process_document(self, document: RasterDoc) -> str:
        raise NotImplementedError
