from document_relayout.core.backend.types.box import Box


def remove_key_value_region(boxes: list[Box]) -> list[Box]:
    return [box for box in boxes if box.label != "key-value region"]
