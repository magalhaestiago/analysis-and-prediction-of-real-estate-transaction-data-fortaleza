from document_relayout.core.backend.types.box import Box

CONFIDENCE_THRESHOLDS = {
    "caption": 0.5,
    "footnote": 0.5,
    "formula": 0.5,
    "list-item": 0.5,
    "page-footer": 0.5,
    "page-header": 0.5,
    "picture": 0.5,
    "section-header": 0.45,
    "table": 0.5,
    "text": 0.5,  # 0.45,
    "title": 0.45,
    "code": 0.45,
    "checkbox-selected": 0.45,
    "key-value region": 0.45,
}


def remove_by_confidence(boxes: list[Box]) -> list[Box]:
    return [box for box in boxes if box.confidence > CONFIDENCE_THRESHOLDS[box.label]]
