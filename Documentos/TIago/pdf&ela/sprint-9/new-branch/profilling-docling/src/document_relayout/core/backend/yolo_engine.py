import logging

import cv2
import numpy as np
import pdf2image

from document_relayout.core.backend.yolo.classify_image import classify_yolo
from document_relayout.core.backend.yolo.classify_image import get_img
from document_relayout.core.backend.yolo.classify_image import get_text
from document_relayout.core.backend.yolo.classify_image import label_mapping
from document_relayout.core.postprocess.sorting import sort_boxes

logger = logging.getLogger(__name__)


def img_to_dict(img: np.ndarray, page_number: int) -> list[dict]:
    page = []
    boxes = classify_yolo(img)
    boxes = sort_boxes(boxes, img)

    for box in boxes:
        d = box.to_dict()

        d["label"] = label_mapping(d["label"])

        if d["label"] is None:
            continue

        d["page"] = page_number
        if d["label"] in ("picture", "table"):
            d["content"] = get_img(box, img)
        else:
            d["content"] = get_text(box, img)

        page.append(d)

    return page


logging.basicConfig(level=logging.INFO)


def process_to_dict(path_or_bytes: str | bytes) -> list[dict]:
    if isinstance(path_or_bytes, str):
        logger.info("Processing PDF from path")  # Substitui logging.info por logger.info
        images = pdf2image.convert_from_path(path_or_bytes)
    else:
        logger.info("Processing PDF from bytes")  # Substitui logging.info por logger.info
        images = pdf2image.convert_from_bytes(path_or_bytes)

    output = []

    for page_number, image in enumerate(images):
        output += img_to_dict(
            cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR),
            page_number,
        )

    return output
