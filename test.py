from manim import *
from manim.utils.space_ops import rotate_vector

class KochFractal(Scene):
    def koch(self, p1, p2, level):
        if level == 0:
            return [Line(p1, p2)]
        else:
            a = p1
            b = interpolate(p1, p2, 1 / 3)
            d = interpolate(p1, p2, 2 / 3)
            direction = d - b
            # Rotate by 60 degrees counterclockwise
            c = b + rotate_vector(direction, PI / 3)
            return (self.koch(a, b, level - 1) +
                    self.koch(b, c, level - 1) +
                    self.koch(c, d, level - 1) +
                    self.koch(d, p2, level - 1))

    def construct(self):
        p1 = LEFT * 4
        p2 = RIGHT * 4
        lines = self.koch(p1, p2, 3)
        self.play(*[Create(line) for line in lines])
        self.wait()
