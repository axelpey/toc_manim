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
    color_speed_plastic = white
    color_dot = toc_blue
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
    color_grid = toc_dark_blue
    color_circle = toc_red


def sum_v(v1, v2):
    return [v1[i] + v2[i] for i in range(len(v1))]


class InterpolateTwoSteps(Scene):
    def construct(self):
        self.camera.background_color = color_background

        numberplane = NumberPlane(
            x_line_frequency=2,
            y_line_frequency=2,
            axis_config={
                "stroke_color": color_background,
                "stroke_width": 1,
                "stroke_opacity": 0.5,
                "include_ticks": False,
                "include_tip": False,
                "line_to_number_buff": SMALL_BUFF,
                "label_direction": DR,
                "number_scale_val": 0.5,
                "color": RED,
            },
            background_line_style={
                "stroke_color": color_grid,
                "stroke_width": 1,
                "stroke_opacity": 1,
            },
            faded_line_style={
                "stroke_color": RED,
                "stroke_width": 1,
                "stroke_opacity": 1,
            },
            faded_line_ratio=0,
        )

        position_plastic = [0.6, 0.7, 0]

        current_values = [
            ([0, 0, 0], [0.65, 0.5, 0], [0.75, 0.25, 0]),
            ([0, 2, 0], [0.4, 0.6, 0], [0.6, 0.4, 0]),
            ([2, 0, 0], [0.75, 0.25, 0], [0.8, -0.15, 0]),
            ([2, 2, 0], [0.7, 0.25, 0], [0.85, 0.1, 0]),
            ([4, 0, 0], [0.8, -0.1, 0], [0.65, -0.3, 0]),
            ([4, 2, 0], [0.7, -0.1, 0], [0.5, -0.4, 0]),
        ]
        closest_arrow_idx = [0, 3]

        dot_plastic = Dot(position_plastic, color=color_dot)
        text_plastic = (
            Text("Plastic particle", font=toc_font, color=color_text)
            .scale(0.3)
            .next_to(dot_plastic, direction=UP)
        )

        arrows_currents = [
            [
                Arrow(
                    x[0],
                    sum_v(x[0], x[1 + i]),
                    buff=0,
                ).set_color(color_current)
                for x in current_values
            ]
            for i in range(2)
        ]

        arrow_plastic_speed = Arrow(
            position_plastic,
            sum_v(position_plastic, current_values[closest_arrow_idx[0]][1]),
            buff=0,
        ).set_color(color_speed_plastic)

        closest_point_circle = Circle(radius=0.4, color=color_circle).shift(
            current_values[closest_arrow_idx[0]][0]
        )
        closest_point_circle_2 = Circle(radius=0.4, color=color_circle).shift(
            current_values[closest_arrow_idx[1]][0]
        )
        closest_point_text = (
            Text("Closest recorded current speed", font=toc_font, color=color_text)
            .scale(0.3)
            .next_to(closest_point_circle, direction=DOWN)
        )
        closest_point_text_2 = (
            Text("Closest recorded current speed", font=toc_font, color=color_text)
            .scale(0.3)
            .next_to(closest_point_circle_2, direction=UP)
        )

        ### ANIMATE

        path = VMobject()
        path.set_points_as_corners([dot_plastic.get_center(), dot_plastic.get_center()])
        path.set_color(toc_blue)

        def update_path(path):
            previous_path = path.copy()
            previous_path.add_points_as_corners([dot_plastic.get_center()])
            path.become(previous_path)

        path.add_updater(update_path)
        self.add(path, dot_plastic)

        # Show all close vectors
        copy_closest_arrow = arrows_currents[0][closest_arrow_idx[0]].copy()
        self.add(dot_plastic, text_plastic)
        self.play(
            FadeIn(numberplane),
            FadeIn(copy_closest_arrow),
            *[FadeIn(arrows_currents[0][i]) for i in range(len(current_values))],
        )
        self.wait(duration=2)

        # Indicate closest vector
        self.play(GrowFromCenter(closest_point_circle), FadeIn(closest_point_text))
        self.wait(duration=4)

        # Move closest vector to dot
        self.play(
            FadeOut(closest_point_circle),
            FadeOut(closest_point_text),
            FadeOut(text_plastic),
            Transform(arrows_currents[0][closest_arrow_idx[0]], arrow_plastic_speed),
        )
        self.wait(duration=1)

        # Move plastic
        self.play(
            dot_plastic.animate.shift(current_values[closest_arrow_idx[0]][1]),
            FadeOut(arrows_currents[0][closest_arrow_idx[0]]),
        )
        self.wait()

        arrows_currents[0][closest_arrow_idx[0]] = copy_closest_arrow

        # Display the new arrows
        self.play(
            *[
                Transform(arrows_currents[0][i], arrows_currents[1][i])
                for i in range(len(current_values))
            ],
            run_time=3,
        )
        self.wait(duration=1)

        # Indicate closest vector
        self.play(GrowFromCenter(closest_point_circle_2), FadeIn(closest_point_text_2))
        self.wait(duration=3)

        arrow_plastic_speed_2 = Arrow(
            dot_plastic.get_center(),
            sum_v(dot_plastic.get_center(), current_values[closest_arrow_idx[1]][2]),
            buff=0,
        ).set_color(color_speed_plastic)

        # Move closest vector to dot
        self.play(
            FadeOut(closest_point_circle_2),
            FadeOut(closest_point_text_2),
            Transform(arrows_currents[1][closest_arrow_idx[1]], arrow_plastic_speed_2),
        )
        self.wait()

        # Move plastic
        self.play(
            dot_plastic.animate.shift(current_values[closest_arrow_idx[1]][2]),
            FadeOut(arrows_currents[1][closest_arrow_idx[1]]),
        )
        self.wait()

        # Fade out the numberplane and the arrows
        self.play(
            FadeOut(numberplane),
            *[FadeOut(arrows_currents[0][i]) for i in range(len(current_values))],
        )
        self.wait()