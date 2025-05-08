from typing import Self


class Box:
    def __init__(
        self,
        box_id,
        label: str,
        cordinates: list[int],
        confidence: float = 1.0,
    ) -> None:
        self.label = label.lower()
        self.cordinates = cordinates
        self.confidence = confidence
        self.id = box_id

    def to_dict(self):
        return {
            "label": self.label,
        }

    def __str__(self):
        return {
            "label": self.label,
            "cordinates": {
                "x1": self.cordinates[0],
                "y1": self.cordinates[1],
                "x2": self.cordinates[2],
                "y2": self.cordinates[3],
            },
            "confidence": self.confidence,
        }.__str__()

    def area(self) -> float:
        return float(
            abs(
                (self.cordinates[0] - self.cordinates[2]) * (self.cordinates[1] - self.cordinates[3]),
            ),
        )

    def overlaping_area(self, other: Self, frac: float = 1e-7) -> float:
        begin_x = max(self.cordinates[0], other.cordinates[0])
        end_x = min(self.cordinates[2], other.cordinates[2])
        begin_y = max(self.cordinates[1], other.cordinates[1])
        end_y = min(self.cordinates[3], other.cordinates[3])

        if begin_x > end_x or begin_y > end_y:
            return float(frac)

        return float((end_y - begin_y) * (end_x - begin_x) + frac)

    @property
    def left(self):
        return self.cordinates[0]

    @property
    def r(self):
        return self.cordinates[2]

    @property
    def b(self):
        return self.cordinates[1]

    @property
    def t(self):
        return self.cordinates[3]
