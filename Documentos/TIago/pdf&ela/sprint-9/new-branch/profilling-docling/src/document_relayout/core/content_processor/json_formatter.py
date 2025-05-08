import json
from pathlib import Path
from urllib.parse import unquote

from docling_core.types.doc.document import ImageRef
from docling_core.types.doc.document import PictureItem
from PIL import Image as PILImage
from pydantic import AnyUrl

from document_relayout.core.hp_document import HPDocument

from .base_formatter import BaseFormatter


class JsonFormatter(BaseFormatter):
    @classmethod
    def __generate_read_order(cls, body: list[dict], doc: dict):
        order = []

        for element in body:
            _, typing, pos = element["$ref"].split("/")
            if typing in ("groups", "pictures"):
                order.extend(cls.__generate_read_order(doc[typing][int(pos)]["children"], doc))

            if typing in ("pictures", "texts", "tables"):
                order.append(element)

        return order

    @classmethod
    def __get_dict(cls, document: HPDocument) -> dict:
        obj = document.export_to_dict()

        obj["read_order"] = cls.__generate_read_order(obj["body"]["children"], obj)
        return obj

    @classmethod
    def __get_dict_embeded(cls, document: HPDocument) -> dict:
        output_dir = Path("./results")

        doc_filename = "file.pdf"

        picture_counter = 0
        for element, _level in document.iterate_items():
            if isinstance(element, PictureItem):
                picture_counter += 1
                element_image_filename = output_dir / f"{doc_filename}-picture-{picture_counter}.png"
                with element_image_filename.open("wb") as fp:
                    element.get_image(document).save(fp, "PNG")

        for _, (item, _) in enumerate(document.iterate_items(with_groups=True)):
            if isinstance(item, PictureItem):
                if item.image is not None:
                    if isinstance(item.image.uri, AnyUrl) and item.image.uri.scheme == "file":
                        assert isinstance(item.image.uri.path, str)

                        tmp_image = PILImage.open(str(unquote(item.image.uri.path)))
                        item.image = ImageRef.from_pil(tmp_image, dpi=item.image.dpi)

                    elif isinstance(item.image.uri, Path):
                        tmp_image = PILImage.open(str(item.image.uri))
                        item.image = ImageRef.from_pil(tmp_image, dpi=item.image.dpi)

        return cls.__get_dict(document)

    @classmethod
    def __remove_children_of_types(cls, parents: list[dict], types: list[str]):
        for parent in parents:
            to_remove = []

            for pos, element in enumerate(parent["children"]):
                _, typing, _ = element["$ref"].split("/")
                if typing in types:
                    to_remove.append(pos)

            for pos in reversed(to_remove):
                parent["children"].pop(pos)

    @classmethod
    def from_hp_doc(cls, document: HPDocument) -> str:
        obj = cls.__get_dict_embeded(document)

        return json.dumps(obj)

    @classmethod
    def texts_from_hp_doc(cls, document: HPDocument) -> str:
        obj = cls.__get_dict(document)

        remove_list = ("pictures", "tables", "form_items", "key_value_items")

        for key in remove_list:
            if key in obj:
                del obj[key]

        cls.__remove_children_of_types(
            parents=[obj["body"], *obj["groups"], {"children": obj["read_order"]}],
            types=remove_list,
        )

        return json.dumps(obj)

    @classmethod
    def imgs_from_hp_doc(cls, document: HPDocument) -> str:
        obj = cls.__get_dict_embeded(document)

        remove_list = ("texts", "tables", "form_items", "key_value_items")

        for key in remove_list:
            if key in obj:
                del obj[key]

        cls.__remove_children_of_types(
            parents=[obj["body"], *obj["groups"], *obj["pictures"], {"children": obj["read_order"]}],
            types=remove_list,
        )

        # docling also does json.dumps(export_to_dict())
        return json.dumps(obj)

    @classmethod
    def tables_from_hp_doc(cls, document: HPDocument) -> str:
        obj = cls.__get_dict(document)

        remove_list = ("texts", "pictures", "form_items", "key_value_items")

        for key in remove_list:
            if key in obj:
                del obj[key]

        cls.__remove_children_of_types(
            parents=[obj["body"], *obj["groups"], *obj["tables"], {"children": obj["read_order"]}],
            types=remove_list,
        )
        # docling also does json.dumps(export_to_dict())
        return json.dumps(obj)

    @classmethod
    def from_yolo_doc(cls, elements: list[dict]) -> str:
        output = {
            "pages": [],
        }

        pages = {}
        for element in elements:
            page_number = element.get("page", 1)
            if page_number not in pages:
                pages[page_number] = []
            pages[page_number].append(
                {
                    "label": element.get("label"),
                    "content": element.get("content"),
                    "coordinates": element.get("coordinates", []),
                },
            )

        for page_number, page_elements in sorted(pages.items()):
            output["pages"].append(
                {
                    "page_number": page_number,
                    "elements": page_elements,
                },
            )
        return json.dumps(output)
