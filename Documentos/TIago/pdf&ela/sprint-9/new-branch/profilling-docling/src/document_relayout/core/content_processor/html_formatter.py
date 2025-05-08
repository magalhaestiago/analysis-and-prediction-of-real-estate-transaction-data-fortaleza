from docling_core.types.doc.base import ImageRefMode

from document_relayout.core.hp_document import HPDocument

from .base_formatter import BaseFormatter


class HtmlFormatter(BaseFormatter):
    @classmethod
    def from_hp_doc(cls, document: HPDocument) -> str:
        return document.export_to_html(image_mode=ImageRefMode.EMBEDDED)
