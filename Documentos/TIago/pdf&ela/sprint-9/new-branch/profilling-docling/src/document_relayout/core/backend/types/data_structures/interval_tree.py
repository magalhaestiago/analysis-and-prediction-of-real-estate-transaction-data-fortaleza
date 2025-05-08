import bisect


class Interval:
    """Helper class for sortable intervals."""

    def __init__(self, min_val: float, max_val: float, interval_id: int):
        self.min_val = min_val
        self.max_val = max_val
        self.id = interval_id

    def __lt__(self, other):
        if isinstance(other, Interval):
            return self.min_val < other.min_val
        return self.min_val < other


class IntervalTree:
    """Memory-efficient interval tree for 1D overlap queries."""

    def __init__(self):
        self.intervals: list[Interval] = []  # Sorted by min_val

    def insert(self, min_val: float, max_val: float, interval_id: int):
        interval = Interval(min_val, max_val, interval_id)
        bisect.insort(self.intervals, interval)

    def find_containing(self, point: float) -> set[int]:
        """Find all intervals containing the point."""
        pos = bisect.bisect_left(self.intervals, point)
        result = set()

        # Check intervals starting before point
        for interval in reversed(self.intervals[:pos]):
            if interval.min_val <= point <= interval.max_val:
                result.add(interval.id)
            else:
                break

        # Check intervals starting at/after point
        for interval in self.intervals[pos:]:
            if point <= interval.max_val:
                if interval.min_val <= point:
                    result.add(interval.id)
            else:
                break

        return result
