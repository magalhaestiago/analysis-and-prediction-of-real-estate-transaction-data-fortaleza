from rtree import index

from document_relayout.core.backend.types.box import Box

from .interval_tree import IntervalTree


class SpatialClusterIndex:
    """Efficient spatial indexing for clusters using R-tree and interval trees."""

    def __init__(self, boxes: list[Box]):
        p = index.Property()
        p.dimension = 2
        self.spatial_index = index.Index(properties=p)
        self.x_intervals = IntervalTree()
        self.y_intervals = IntervalTree()
        self.clusters_by_id: dict[int, Box] = {}

        for box in boxes:
            self.add_cluster(box)

    def add_cluster(self, box: Box):
        self.spatial_index.insert(box.id, box.cordinates)
        self.x_intervals.insert(box.left, box.r, box.id)
        self.y_intervals.insert(box.t, box.b, box.id)
        self.clusters_by_id[box.id] = box

    def remove_cluster(self, box: Box):
        self.spatial_index.delete(box.id, box.cordinates)
        del self.clusters_by_id[box.id]

    def find_candidates(self, bbox: Box) -> set[int]:
        """Find potential overlapping cluster IDs using all indexes."""
        spatial = set(self.spatial_index.intersection(bbox.cordinates))
        x_candidates = self.x_intervals.find_containing(
            bbox.left,
        ) | self.x_intervals.find_containing(bbox.r)
        y_candidates = self.y_intervals.find_containing(
            bbox.t,
        ) | self.y_intervals.find_containing(bbox.b)
        return spatial.union(x_candidates).union(y_candidates)

    def check_overlap(
        self,
        box1: Box,
        box2: Box,
        overlap_threshold: float,
        containment_threshold: float,
    ) -> bool:
        """Check if two bboxes overlap sufficiently."""
        area1, area2 = box1.area(), box2.area()
        if area1 <= 0 or area2 <= 0:
            return False

        overlap_area = box1.overlaping_area(box2, 0)
        if overlap_area <= 0:
            return False

        iou = overlap_area / (area1 + area2 - overlap_area)
        containment1 = overlap_area / area1
        containment2 = overlap_area / area2

        return iou > overlap_threshold or containment1 > containment_threshold or containment2 > containment_threshold
