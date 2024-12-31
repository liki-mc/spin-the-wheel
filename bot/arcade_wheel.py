import os
os.environ["ARCADE_HEADLESS"] = "True"


import arcade
from colorsys import hls_to_rgb
import imageio
import numpy as np

SIZE = 450
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

class WheelGame(arcade.Window):
    def __init__(self, options: list[str]):
        super().__init__(WIDTH, HEIGHT, "Spin the Wheel")
        arcade.set_background_color(arcade.color.WHITE)
        self.wheel_angle = 0
        self.frames = []
        self.options = options
        self.shape_element_list = arcade.ShapeElementList()
        self.sprite_list = arcade.SpriteList()
        self.text_list : list[Text] = []
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
    
    def on_update(self):
        self.wheel_angle += 4
        self.shape_element_list.angle = self.wheel_angle
        for text in self.text_list:
            text.rotate_text(4)

    def draw_frame(self):
        arcade.start_render()
        self.shape_element_list.draw()
        for text in self.text_list:
            text.draw()
        self.capture_frame()

    def capture_frame(self):
        image = arcade.get_image()
        image_data = np.asarray(image)
        self.frames.append(image_data)

    def save_video(self, filename):
        imageio.mimsave(filename, self.frames, fps = 60)

def main():
    window = WheelGame(["heyodjiazejoisdijfiejzaoifjeziaojfoeiazjejehyo", "12", "&&&"])
    for _ in range(100):  # Generate 100 frames
        window.on_update()
        window.draw_frame()
    window.save_video('output_video.mp4')
    window.close()

if __name__ == "__main__":
    main()


















































async def setup(*args):
    pass