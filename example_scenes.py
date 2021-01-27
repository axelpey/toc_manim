from manim import *

toc_font = "Proxima Nova Bold"
toc_blue = "#01CBE1"
toc_navy_blue = "#003755"
toc_red = "#D61418"
toc_pale_yellow = "#F6D77E"
toc_manta_blue = "#2E5DA7"
toc_light_grey = "#F2F5F6"
toc_dark_blue = "#01283C"
toc_extra_dark_blue = "#0E1F2B"
white = "#FFFFFF"


theme = "light"

if theme == "dark":
    color_background = toc_navy_blue
    color_current = toc_manta_blue
    color_wind = toc_pale_yellow
    color_speed_plastic = toc_blue
    color_dot = white
    color_text = white
    color_grid = toc_light_grey
    color_circle = toc_red

elif theme == "light":
    color_background = white
    color_current = toc_navy_blue
    color_wind = toc_manta_blue
    color_speed_plastic = toc_blue
    color_dot = toc_dark_blue
    color_text = toc_dark_blue
    color_grid = toc_extra_dark_blue
    color_circle = toc_red


class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        square.flip(RIGHT)
        square.rotate(-3 * TAU / 8)
        circle.set_fill(PINK, opacity=0.5)

        self.play(ShowCreation(square))
        self.play(Transform(square, circle))
        self.play(FadeOut(square))


class Monon(Scene):
    def construct(self):
        text = Text(
            "Monon",
        )
        self.play(Write(text))
        self.wait()
        self.play(FadeOut(text))


class SumVectors(Scene):
    def construct(self):
        wind_speed = [1, 2, 0]
        current_speed = [1, -1, 0]

        self.camera.background_color = color_background
        dot_plastic = Dot(color=color_dot)
        text_plastic = (
            Text("Plastic particle", font=toc_font, color=color_text)
            .scale(0.5)
            .next_to(dot_plastic)
        )

        arrow_current = Arrow(ORIGIN, current_speed, buff=0).set_color(color_current)
        text_current = (
            Text("Current speed", font=toc_font, color=color_text)
            .scale(0.5)
            .next_to(arrow_current)
        )

        arrow_wind = Arrow(ORIGIN, wind_speed, buff=0).set_color(color_wind)
        text_wind = (
            Text("Wind speed", font=toc_font, color=color_text)
            .scale(0.5)
            .next_to(arrow_wind)
        )

        arrow_plastic = Arrow(
            ORIGIN, sum_v(wind_speed, current_speed), buff=0
        ).set_color(color_speed_plastic)
        text_speed_plast = (
            Text("Plastic speed", font=toc_font, color=color_text)
            .scale(0.5)
            .next_to(arrow_plastic, direction=UP)
        )

        self.add(dot_plastic, text_plastic)
        self.play(FadeIn(arrow_current), FadeIn(text_current))
        self.play(FadeIn(arrow_wind), FadeIn(text_wind))
        self.wait()
        self.play(FadeOut(text_current), FadeOut(text_wind), FadeOut(text_plastic))
        self.play(arrow_wind.animate.shift(current_speed))
        self.play(FadeIn(arrow_plastic), FadeIn(text_speed_plast))
        self.wait()
        self.play(
            FadeOut(arrow_plastic),
            FadeOut(text_speed_plast),
            FadeOut(arrow_current),
            FadeOut(arrow_wind),
            dot_plastic.animate.shift(sum_v(current_speed, wind_speed)),
        )
        self.wait()


def sum_v(v1, v2):
    return [v1[i] + v2[i] for i in range(len(v1))]


class InterpolateDummy(Scene):
    def construct(self):
        position_plastic = [1.5, 1.5, 0]

        self.camera.background_color = color_background

        numberplane = NumberPlane(x_line_frequency=2, y_line_frequency=2)

        dot_plastic = Dot(position_plastic, color=color_dot)
        text_plastic = (
            Text("Plastic particle", font=toc_font, color=color_text)
            .scale(0.5)
            .next_to(dot_plastic, direction=DOWN)
        )

        current_values = [
            ([0, 0, 0], [1, 0.5, 0]),
            ([2, 2, 0], [0.75, 0.25, 0]),
            ([0, 2, 0], [0.5, 0.5, 0]),
            ([2, 0, 0], [0.75, 0.25, 0]),
        ]
        closest_arrow_idx = 1

        arrows_currents = [
            Arrow(x[0], sum_v(x[0], x[1]), buff=0).set_color(color_current)
            for x in current_values
        ]

        arrow_plastic_speed = Arrow(
            position_plastic,
            sum_v(position_plastic, current_values[closest_arrow_idx][1]),
            buff=0,
        ).set_color(color_speed_plastic)

        closest_point_circle = Circle(radius=0.4, color=color_circle).shift(
            current_values[closest_arrow_idx][0]
        )
        closest_point_text = (
            Text("Closest recorded current speed", font=toc_font, color=color_text)
            .scale(0.4)
            .next_to(closest_point_circle, direction=UP)
        )

        # Show all close vectors
        copy_closest_arrow = arrows_currents[closest_arrow_idx].copy()
        self.add(numberplane, dot_plastic, text_plastic)
        self.add(copy_closest_arrow)
        self.add(*arrows_currents)

        # Indicate closest vector
        self.play(GrowFromCenter(closest_point_circle), FadeIn(closest_point_text))
        self.wait(duration=4)
        self.play(FadeOut(closest_point_circle), FadeOut(closest_point_text))

        # Move closest vector to dot
        self.play(Transform(arrows_currents[closest_arrow_idx], arrow_plastic_speed))
        self.play(FadeOut(text_plastic))

        # Move plastic
        self.play(
            FadeOut(copy_closest_arrow),
            *[FadeOut(arrows_currents[i]) for i in range(len(current_values))],
            dot_plastic.animate.shift(current_values[closest_arrow_idx][1]),
        )
        self.wait()
