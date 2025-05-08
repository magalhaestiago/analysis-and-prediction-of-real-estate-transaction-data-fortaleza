from document_relayout.core.backend.types.box import Box
from document_relayout.core.backend.types.data_structures.spatial_cluster_index import SpatialClusterIndex
from document_relayout.core.backend.types.data_structures.union_find import UnionFind

std_params = {
    "overlap_thrs": 1.3,
    "conf_thrs": 0.05,
}


def __is_better_than(box: Box, other_box: Box, params: dict = std_params):
    """Returns true if box is considered better than other_box"""
    # Rule 1: LIST_ITEM vs TEXT
    if box.label == "list_item" and other_box.label == "text":
        # Check if areas are similar (within 20% of each other)
        threshold = 0.2
        area_ratio = box.area() / other_box.area()
        area_similarity = abs(1 - area_ratio) < threshold
        if area_similarity:
            return True

    # Rule 2: CODE vs others
    if box.label == "code":
        # Calculate how much of the other cluster is contained within the CODE cluster
        threshold = 0.8
        overlap = other_box.overlaping_area(box)
        containment = overlap / other_box.area()
        if containment > threshold:  # other is 80% contained within CODE
            return True

    # If no label-based rules matched, fall back to area/confidence thresholds
    area_ratio = box.area() / other_box.area()
    conf_diff = other_box.confidence - box.confidence

    # Default to keeping candidate if no rules triggered rejection
    return not (area_ratio <= params["overlap_thrs"] and conf_diff > params["conf_thrs"])


def __get_best_box(boxes: list[Box], params: dict = std_params) -> Box:
    best = None

    for box in boxes:
        is_apt = True

        for other_box in boxes:
            if other_box.id == box.id:
                continue
            if not __is_better_than(box, other_box):
                is_apt = False
                break

        if is_apt:
            if best is None:
                best = box
            elif box.area() > best.area() and best.confidence - box.confidence < params["conf_thrs"]:
                """
                In this case, acourding to doclings matrics, both boxes are apt to
                be considered the best, even when compared to eachother. In this case
                the one with bigger area is considered if the condifence is
                not too low in relation
                """
                best = box
    return best if (best or len(boxes) == 0) else boxes[0]


def remove_overlapping(boxes: list[Box], params: dict = std_params) -> list[Box]:
    uf = UnionFind(list(range(len(boxes))))

    box_index = SpatialClusterIndex(boxes)

    # Future optimizations with R-Tree and interval trees
    for box_pos, box in enumerate(boxes):
        candidates = box_index.find_candidates(box)
        candidates.discard(box.id)

        for other_box_id in candidates:
            other_box = next(b for b in boxes if b.id == other_box_id)
            # Merge overlapping boxes considering a threshold
            overlap = box.overlaping_area(other_box)
            if box.area() / overlap < params["overlap_thrs"]:
                uf.union(box_pos, boxes.index(other_box))

    response = []

    for group in uf.get_groups().values():
        group_b = [boxes[pos] for pos in group]
        response.append(__get_best_box(group_b, params))

    return response
