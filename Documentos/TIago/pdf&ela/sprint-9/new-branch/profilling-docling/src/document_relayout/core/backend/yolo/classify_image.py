import base64
import os

import cv2
import pytesseract
from dotenv import load_dotenv
from PIL import Image
from ultralytics import YOLO

from document_relayout.core.backend.types.box import Box
from document_relayout.core.postprocess.postprocess import postprocess
from document_relayout.core.postprocess.remove_by_confidence import remove_by_confidence
from document_relayout.core.postprocess.remove_key_value_region import remove_key_value_region
from document_relayout.core.postprocess.remove_overlapping import remove_overlapping

load_dotenv()
YOLO_MODEL_PATH = os.getenv("YOLO_MODEL_PATH")


def get_img(box: Box, img) -> str:
    cropped = img[
        box.cordinates[1] : box.cordinates[3],
        box.cordinates[0] : box.cordinates[2],
    ]
    return base64.b64encode(cv2.imencode(".jpeg", cropped)[1].tobytes()).decode()


@postprocess([remove_key_value_region, remove_by_confidence, remove_overlapping])
def classify_yolo(img, model_path: str = YOLO_MODEL_PATH) -> list[Box]:
    model = YOLO(model_path)

    result = model.predict(img)[0]

    height = result.orig_shape[0]
    width = result.orig_shape[1]
    label_boxes = []

    for label, cords in zip(result.boxes.cls.tolist(), result.boxes.xyxyn.tolist(), strict=False):
        label_boxes.append(
            Box(
                len(label_boxes),
                result.names[int(label)],
                [
                    int(cords[0] * width),
                    int(cords[1] * height),
                    int(cords[2] * width),
                    int(cords[3] * height),
                ],
            ),
        )
    return label_boxes


def get_text(box: Box, img) -> str:
    return pytesseract.image_to_string(
        Image.fromarray(
            img[
                box.cordinates[1] : box.cordinates[3],
                box.cordinates[0] : box.cordinates[2],
            ],
        ),
    )


def label_mapping(label: str) -> str | None:
    match label:
        case "formula" | "picture" | "table":
            return "picture"
        case "section-header" | "title":
            return "header"
        case "list-item":
            return "list-item"
        case "text" | "caption" | "footnote" | "page-header" | "page-footer":
            return "paragraph"
        case _:
            return None
