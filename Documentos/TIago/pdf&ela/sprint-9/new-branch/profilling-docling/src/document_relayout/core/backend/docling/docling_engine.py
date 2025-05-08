"""
Filename: docling_engine.py
Author: Alan Bandeira
Date: 20/02/2025
Version: 0.1
Description:
    This file contains the code the docling backend engine.

Contact: alan.bandeira1@hp.com
"""

# Imports

from io import BytesIO
from pathlib import Path

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter
from docling.document_converter import PdfFormatOption
from docling_core.types.io import DocumentStream

from document_relayout.core.backend.base_engine import BaseEngine
from document_relayout.core.hp_document import HPDocument

# Methods and classes


class DoclingEngine(BaseEngine):
    def _process_from_bytes_io(self, b_io: BytesIO) -> HPDocument:
        output_dir = Path("./results")

        pipeline_options = PdfPipelineOptions()
        pipeline_options.images_scale = 2.0
        pipeline_options.generate_page_images = True
        pipeline_options.generate_picture_images = True

        converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options),
            },
        )

        output_dir.mkdir(parents=True, exist_ok=True)

        return converter.convert(DocumentStream(name="file.pdf", stream=b_io)).document
