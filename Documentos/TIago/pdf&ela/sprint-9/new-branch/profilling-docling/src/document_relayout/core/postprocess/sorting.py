import numpy as np

from document_relayout.core.backend.types.box import Box


def sort_boxes(boxes: list[Box], img: np.ndarray) -> list[Box]:
    height, width, channels = img.shape

    threshold = width / 2

    first = []
    second = []

    for box in boxes:
        x1, y1, x2, y2 = box.cordinates
        if x1 < threshold:
            first.append(box)
        else:
            second.append(box)

    return sorted(first, key=lambda x: x.cordinates[1]) + sorted(
        second,
        key=lambda x: x.cordinates[1],
    )
