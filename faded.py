from manim import *
import numpy as np
from manim.utils.space_ops import rotate_vector


def koch_points(A, B, depth):
    if depth == 0:
        return [A, B]
    else:
        V = (B - A) / 3
        C = A + V
        E = A + 2 * V
        D = C + rotate_vector(V, np.pi / 3)
        points = (
            koch_points(A, C, depth - 1)
            + koch_points(C, D, depth - 1)[1:]
            + koch_points(D, E, depth - 1)[1:]
            + koch_points(E, B, depth - 1)[1:]
        )
        return points


class KochSnowflakeDrawing(Scene):
    def construct(self):
        radius = 3.5
        p1 = radius * UP
        p2 = rotate_vector(p1, -2 * PI / 3)
        p3 = rotate_vector(p1, 2 * PI / 3)
        max_depth = 6

        def get_snowflake_points(depth):
            side1 = koch_points(p1, p2, depth)
            side2 = koch_points(p2, p3, depth)[1:]
            side3 = koch_points(p3, p1, depth)[1:]
            return side1 + side2 + side3 + [side1[0]]

        # Create static "Depth:" label and dynamic number
        label = Text("Depth:").to_edge(UP).shift(LEFT * 4)
        number = Text("0").next_to(label, RIGHT, buff=0.2)

        self.play(Write(label), Write(number), run_time=0.5)

        previous_snowflake = None

        for depth in range(max_depth + 1):
            points = get_snowflake_points(depth)
            snowflake = VMobject().set_points_as_corners(points).set_stroke(WHITE, 2)

            # Remove previous snowflake
            if previous_snowflake:
                self.play(FadeOut(previous_snowflake), run_time=0.5)

            # Update number and draw new snowflake
            new_number = Text(str(depth)).move_to(number)
            self.play(Transform(number, new_number), run_time=0.5)
            self.play(Create(snowflake, run_time=4))

            previous_snowflake = snowflake

        self.wait(2)
