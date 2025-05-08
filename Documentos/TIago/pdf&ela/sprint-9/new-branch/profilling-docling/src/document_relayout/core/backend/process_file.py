from abc import ABC
from abc import abstractmethod
from pathlib import Path

from document_relayout.core.backend.docling.docling_engine import DoclingEngine
from document_relayout.core.backend.yolo_engine import process_to_dict
from document_relayout.core.content_processor.html_formatter import HtmlFormatter
from document_relayout.core.content_processor.json_formatter import JsonFormatter


class DocumentProcessor(ABC):
    @abstractmethod
    def process(self, input_file, output_file) -> str:
        pass


class YoloProcessor(DocumentProcessor):
    def process(self, input_file, output_file):
        doc = process_to_dict(input_file)
        yolo_file = JsonFormatter.from_yolo_doc(doc)
        with Path(f"{output_file}.json").open("w") as f:
            f.write(yolo_file)


class DoclingProcessor(DocumentProcessor):
    def process(self, input_file, output_file):
        doc = DoclingEngine().process(input_file)
        for name, j in (
            ("full", JsonFormatter.from_hp_doc(doc)),
            ("texts", JsonFormatter.texts_from_hp_doc(doc)),
            ("imgs", JsonFormatter.imgs_from_hp_doc(doc)),
            ("tables", JsonFormatter.tables_from_hp_doc(doc)),
        ):
            with Path(f"{name}.json").open("w") as f:
                f.write(j)

            with Path(f"{output_file}.html").open("w", encoding="utf-8") as f:
                f.write(HtmlFormatter.from_hp_doc(doc))


def process_file(input_file, doc_processor: DocumentProcessor, output_file) -> str:
    return doc_processor.process(input_file, output_file)
