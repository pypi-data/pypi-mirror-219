from manim.utils.color import Colors

class VisualSettings:
    point_color: Colors
    stoke_color: Colors
    polygon_color: Colors
    point_size: float
    stoke_width: float

    def __init__(self, point_color, stoke_color, polygon_color, point_size, stoke_width):
        self.point_color = point_color
        self.stoke_color = stoke_color
        self.polygon_color = polygon_color
        self.point_size = point_size
        self.stoke_width = stoke_width
