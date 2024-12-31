import os
os.environ["ARCADE_HEADLESS"] = "True"


import arcade
from colorsys import hls_to_rgb
import imageio
import numpy as np
import random
import time
random.seed(time.time())

SIZE = 350
TEXT_SIZE = SIZE - 50
WIDTH = 2 * (SIZE + 50)
HEIGHT = 2 * (SIZE + 50)

class Text(arcade.Text):
    def __init__(self, text: str, rotation: float, **kwargs):
        kwargs["start_x"] = np.cos(np.radians(rotation)) * TEXT_SIZE + WIDTH / 2
        kwargs["start_y"] = np.sin(np.radians(rotation)) * TEXT_SIZE + HEIGHT / 2
        kwargs["color"] = arcade.color.BLACK
        kwargs["font_size"] = 20
        kwargs["width"] = TEXT_SIZE - 100
        kwargs["anchor_y"] = "center"
        kwargs["rotation"] = rotation + 180
        super().__init__(text, **kwargs)
        self.current_angle = rotation
    
    def rotate_text(self, angle: float):
        self.current_angle += angle
        self.rotation = self.current_angle + 180
        self.position = (
            np.cos(np.radians(self.current_angle)) * TEXT_SIZE + WIDTH / 2,
            np.sin(np.radians(self.current_angle)) * TEXT_SIZE + HEIGHT / 2
        )

class SpinTheWheel(arcade.Window):
    def __init__(self, options: list[str]):
        super().__init__(WIDTH, HEIGHT, "Spin the Wheel")
        self.wheel_angle = 0
        self.frames = []
        self.options = options
        self.shape_element_list = arcade.ShapeElementList()
        self.sprite_list = arcade.SpriteList()
        self.text_list : list[Text] = []
        self.triangle = arcade.ShapeElementList()
        self.setup(options)
        self.setup_triangle()
    
    @staticmethod
    def get_arc_filled(x, y, radius, color, start_angle, angle):
        angles = np.linspace(start_angle, angle + start_angle, 100)
        x_points = x + radius * np.cos(np.radians(angles))
        y_points = y + radius * np.sin(np.radians(angles))
        x_points = np.append(x_points, x)
        y_points = np.append(y_points, y)
        points = list(zip(x_points, y_points))
        return arcade.create_polygon(points, color), arcade.create_line_strip((points[0], (x, y), points[-1]), arcade.color.WHITE, line_width = 3)

    def setup_triangle(self):
        angles = np.linspace(0, 360, 4)[:3] + 180
        dx, dy = np.cos(np.radians(angles)) * 30, np.sin(np.radians(angles)) * 30
        base_x, base_y = WIDTH / 2 + SIZE + 15, HEIGHT / 2
        points = list(zip(base_x + dx, base_y + dy))
        triangle = arcade.create_polygon(points, (204, 204, 204))
        trangle_outline = arcade.create_line_loop(points, arcade.color.GRAY, 6)

        self.triangle.append(triangle)
        self.triangle.append(trangle_outline)
        
    
    def setup(self, options: list[str]) -> None:
        N = len(options)
        alpha = 360 / N
        for i, option in enumerate(options):
            color = hls_to_rgb(i * alpha / 360, 0.75, 0.35)
            rgb_color = [int(i * 255) for i in color]
            arc, outline = self.get_arc_filled(0, 0, SIZE, rgb_color, i * alpha, alpha)
            self.shape_element_list.append(arc)
            self.shape_element_list.append(outline)

            text = option[:17] + "..." if len(option) > 20 else option
            text_object = Text(
                text, 
                i * alpha + alpha / 2
            )
            self.text_list.append(text_object)
        
        self.shape_element_list.center_x = WIDTH / 2
        self.shape_element_list.center_y = HEIGHT / 2
    
    def on_update(self, angle: float = 4):
        self.wheel_angle += angle
        self.shape_element_list.angle = self.wheel_angle
        for text in self.text_list:
            text.rotate_text(angle)

    def draw_frame(self):
        arcade.start_render()
        self.shape_element_list.draw()
        for text in self.text_list:
            text.draw()
        
        self.triangle.draw()
        self.capture_frame()

    def capture_frame(self):
        image = arcade.get_image()
        image_data = np.asarray(image)
        self.frames.append(image_data)

    def save_video(self, filename):
        imageio.mimsave(filename, self.frames, fps = 60)
    
    def slow(self):
        for i in range(13, 0, -1):
            for _ in range(20 - i):
                self.on_update(i)
                self.draw_frame()
        
        for i in [2, 3, 4, 5]:
            for _ in range(20):

                self.on_update(1/i)
                self.draw_frame()
        
        for i in range(20):
            self.draw_frame()
    
    def run(self):
        for _ in range(random.randint(20, 200)):
            self.on_update(14)
            self.draw_frame()
        
        self.slow()
        
        self.save_video("output.mp4")
        self.close()

def main():
    window = SpinTheWheel(["heyodjiazejoisdijfiejzaoifjeziaojfoeiazjejehyo", "12", "&&&"])
    window.run()

if __name__ == "__main__":
    main()


















































async def setup(*args):
    pass