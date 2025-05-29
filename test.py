from manim import *
import numpy as np
from manim.utils.space_ops import rotate_vector


def koch_points(A, B, depth):
    if depth == 0: # if we reach the depth to equal zero dont divide the line
        return [A, B]
    else:
        V = (B - A) / 3 # divides from a to b to equal thirds
        C = A + V #the first third between A and B
        E = A + 2 * V #the second third
        D = C + rotate_vector(V, np.pi / 3) # this is the peak  rotating v 60 degrees
        points = ( #recursively draw the koch
            koch_points(A, C, depth - 1)
            + koch_points(C, D, depth - 1)[1:]
            + koch_points(D, E, depth - 1)[1:]
            + koch_points(E, B, depth - 1)[1:]
        )
        return points


class KochSnowflakeDrawing(Scene):
    def construct(self): # the main animation logic happens in the constructthat inherits from scene
        # Bilding an equilateral triangle
        radius = 3.5  #sets how big the triangle is
        p1 = radius * UP #highest point oin the triangle
        p2 = rotate_vector(p1, -2 * PI / 3) #rotate clockwise by 120 to make one side of the triangle
        p3 = rotate_vector(p1, 2 * PI / 3) #rotate counter clock wise to make the other side
        max_depth = 5

        def get_snowflake_points(depth): #this calls the koch points recursion
            # so we can make division of the points for EACH side of the triangle
            side1 = koch_points(p1, p2, depth)
            side2 = koch_points(p2, p3, depth)[1:] # [1:] so we dont duplicate points on top of each other
                                                        # since the end of a side is the start of another
            side3 = koch_points(p3, p1, depth)[1:]
            return side1 + side2 + side3 + [side1[0]] # [side1[0]] connecting the last point to the start of the side1 so it doesnt leave a gap


        # Static "Depth:" label and dynamic number
        label = Text("Depth:").to_edge(UP).shift(LEFT * 4)
        number = Text("0").next_to(label, RIGHT, buff=0.2)

        self.play(Write(label), Write(number), run_time=0.5)

        snowflakes = [] #to store the snowflake layers so we are able to make the layers on top of each other

        for depth in range(max_depth + 1):
            if depth > 0:
                self.play(snowflakes[-1].animate.set_color(LIGHTER_GREY), run_time=0.5)
                #take the previous snowflake change its color to gray

            # Draw next snowflake
            points = get_snowflake_points(depth) #calls the function that will divide the sides and gives it thr current depth
            snowflake = VMobject().set_points_as_corners(points).set_stroke(LOGO_WHITE, 2)
            # draws the vector given the points
            snowflakes.append(snowflake) #adds the snowflakes to the list for reference

            # Only update the number next to "Depth:"
            new_number = Text(str(depth)).move_to(number)
            self.play(Transform(number, new_number), run_time=0.5)

            self.play(Create(snowflake, run_time=4))

        self.wait(2)
