from pathlib import Path

import cv2
import numpy as np

from document_relayout.core.backend.types.box import Box

COLORS = {
    "text": (150, 205, 197),
    "picture": (255, 255, 0),
    "caption": (255, 0, 255),
    "section-header": (0, 255, 255),
    "footnote": (122, 0, 122),
    "formula": (122, 122, 0),
    "table": (0, 122, 122),
    "list-item": (122, 122, 122),
    "page-header": (0, 0, 255),
    "page-footer": (0, 255, 0),
    "title": (255, 0, 0),
    "key-value region": (0, 0, 0),
}


def gen_color_indices(height: int) -> list[int]:
    image = np.zeros((height, 500, 3), np.uint8)
    image[:, :, 0] = 255
    image[:, :, 1] = 255
    image[:, :, 2] = 255

    start = 10
    pace = 50
    dim = 40
    font = cv2.FONT_HERSHEY_SIMPLEX

    for k, v in COLORS.items():
        cv2.rectangle(image, (5, start), (5 + dim, start + dim), v, -1)
        image = cv2.putText(
            image,
            k,
            (60, start + 30),
            font,
            1,
            (0, 0, 0),
            4,
            cv2.LINE_AA,
        )
        start += pace

    return image


def gen_boxed_img(img, boxes: list[Box]) -> str:
    img = np.array(img)

    img_folder = Path("imgs")

    if not img_folder.is_dir():
        img_folder.mkdir(img_folder)

    n_images = sum(1 for _ in img_folder.iterdir() if _.is_file())

    path = img_folder / f"{n_images + 1}.jpeg"

    for box in boxes:
        cv2.rectangle(
            img,
            (box.cordinates[0], box.cordinates[1]),
            (box.cordinates[2], box.cordinates[3]),
            COLORS[box.label.replace("_", "-")],
            thickness=2,
        )

    img = cv2.hconcat([img, gen_color_indices(img.shape[0])])
    cv2.imwrite(path, img)

    return path
