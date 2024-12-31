import os
os.environ["ARCADE_HEADLESS"] = "True"


import arcade
from colorsys import hls_to_rgb
import imageio
import numpy as np
import pyglet



class WheelGame(arcade.Window):
    def __init__(self, options: list[str]):
        super().__init__(800, 800, "Spin the Wheel")
        arcade.set_background_color(arcade.color.WHITE)
        self.wheel_angle = 0
        self.frames = []
        self.options = options
        self.shape_element_list = arcade.ShapeElementList()
        self.sprite_list = arcade.SpriteList()
        self.setup(options)
    
    @staticmethod
    def get_arc_filled(x, y, radius, color, start_angle, angle):
        angles = np.linspace(start_angle, angle + start_angle, 100)
        x_points = x + radius * np.cos(np.radians(angles))
        y_points = y + radius * np.sin(np.radians(angles))
        x_points = np.append(x_points, x)
        y_points = np.append(y_points, y)
        points = list(zip(x_points, y_points))
        return arcade.create_polygon(points, color), arcade.create_line_loop(points, arcade.color.WHITE, line_width = 3)
    
    def setup(self, options: list[str]) -> None:
        N = len(options)
        alpha = 360 / N
        for i, option in enumerate(options):
            color = hls_to_rgb(i * alpha / 360, 0.75, 0.35)
            rgb_color = [int(i * 255) for i in color]
            arc, outline = self.get_arc_filled(0, 0, 350, rgb_color, i * alpha, alpha)
            self.shape_element_list.append(arc)
            self.shape_element_list.append(outline)
        
        self.shape_element_list.center_x = 400
        self.shape_element_list.center_y = 400
    
    def on_update(self):
        self.wheel_angle += 4
        self.shape_element_list.angle = self.wheel_angle

    def draw_frame(self):
        arcade.start_render()
        self.shape_element_list.draw()
        self.capture_frame()

    def capture_frame(self):
        image = arcade.get_image()
        image_data = np.asarray(image)
        self.frames.append(image_data)

    def save_video(self, filename):
        imageio.mimsave(filename, self.frames, fps = 60)

def main():
    window = WheelGame(["heyoehyo", "12", "&&&"])
    for _ in range(100):  # Generate 100 frames
        window.on_update()
        window.draw_frame()
    window.save_video('output_video.mp4')
    window.close()

if __name__ == "__main__":
    main()


















































async def setup(*args):
    pass