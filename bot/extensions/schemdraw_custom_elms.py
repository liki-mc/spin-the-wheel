import numpy as np
import schemdraw.elements as elm
import schemdraw.segments as segments

from typing import Optional

class CirclePart(elm.Element):
    _element_defaults = {
        "radius": 1,
        "alpha": 120,
    }
    def __init__(
        self, 
        radius: Optional[float] = None, 
        alpha: Optional[int] = None,
        **kwargs
    ):
        super().__init__(**kwargs)

        alpha = (alpha if alpha is not None else self.params["alpha"]) / 180 * np.pi
        radius = radius if radius is not None else self.params["radius"]
        circle_segment = np.linspace(0, alpha, 50)
        x = np.cos(circle_segment) * radius
        y = np.sin(circle_segment) * radius
        self.segments = [
            segments.SegmentPoly([
                (0, 0), 
                *zip(x, y),
                (0, 0)
            ])
        ]

class Triangle(elm.Element):
    _element_defaults = {
        "width": 1,
        "height": 1,
    }
    def __init__(
        self, 
        width: Optional[float] = None,
        height: Optional[float] = None,
        **kwargs
    ):
        super().__init__(**kwargs)

        width = width if width is not None else self.params["width"]
        height = height if height is not None else self.params["height"]

        self.segments = [
            segments.SegmentPoly([
                (-width/2, -height/2),
                (width/2, -height/2),
                (0, height/2),
                (-width/2, -height/2)
            ])
        ]

class EquilateralTriangle(Triangle):
    _element_defaults = {
        "side_length": 1,
    }
    def __init__(
        self, 
        side_length: Optional[float] = None,
        **kwargs
    ):
        self.params["width"] = side_length
        self.params["height"] = np.sqrt(3)/2 * side_length
        super().__init__(width = 1, height = np.sqrt(3)/2, **kwargs)


if __name__ == "__main__":
    import schemdraw
    d = schemdraw.Drawing()
    d += CirclePart()
    d += EquilateralTriangle(4)
    d.draw()

async def setup(*args):
    pass