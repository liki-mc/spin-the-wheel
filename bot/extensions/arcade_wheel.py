import os
os.environ["ARCADE_HEADLESS"] = "True"


import arcade
from colorsys import hls_to_rgb
import emoji
import imageio
from io import BytesIO
import numpy as np
from PIL import Image, ImageDraw
import random
import requests
import time
random.seed(time.time())

SIZE = 350
TEXT_SIZE = SIZE - 50
WIDTH = 2 * (SIZE + 50)
HEIGHT = 2 * (SIZE + 50)

EMOJIS = "".join(emoji.EMOJI_DATA.keys())

def get_emoji(emoji_char: str) -> Image:
    code_point = '-'.join(f'{ord(c):x}' for c in emoji_char)
    url = f"https://cdnjs.cloudflare.com/ajax/libs/twemoji/14.0.2/72x72/{code_point}.png"
    response = requests.get(url)
    if response.status_code != 200:
        return Image.new("RGBA", (31, 31))
    img = Image.open(BytesIO(response.content)).convert("RGBA")
    img = img.resize((31, 31), Image.ANTIALIAS)
    return img

def create_circular_image(image_path: str) -> Image:
    # Open the input image
    img = Image.open(image_path).convert("RGBA")
    
    # Resize the image to fit within a 150x150 pixel box
    img = img.resize((150, 150), Image.ANTIALIAS)
    
    # Create a mask to make the image circular
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + img.size, fill = 255)
    
    # Apply the mask to the image
    img.putalpha(mask)
    
    return img

class Text(arcade.Text):
    def __init__(self, text: str, rotation: float, **kwargs):
        kwargs["start_x"] = np.cos(np.radians(rotation)) * TEXT_SIZE + WIDTH / 2
        kwargs["start_y"] = np.sin(np.radians(rotation)) * TEXT_SIZE + HEIGHT / 2
        kwargs["color"] = arcade.color.BLACK
        kwargs["font_size"] = 20
        kwargs["width"] = TEXT_SIZE - 100
        kwargs["anchor_y"] = "center"
        kwargs["rotation"] = rotation + 180
        text, self.sprites = self.get_emojis(text)
        super().__init__(text, **kwargs)
        self.current_angle = rotation
    
    def get_emojis(self, text: str) -> tuple[str, list[tuple[float, arcade.Sprite]]]:
        if len(text) == 1:
            if text in EMOJIS:
                image = get_emoji(text)
                texture = arcade.Texture(f"Emoji{text}", image.resize((72, 72), Image.ANTIALIAS))
                sprite = arcade.Sprite(texture = texture)
                return "    ", [(10, sprite)]
            
        sprites = []
        for i, letter in enumerate(text):
            if letter in EMOJIS:
                image = get_emoji(letter)
                texture = arcade.Texture(f"Emoji{letter}", image)
                sprite = arcade.Sprite(texture = texture)
                sprites.append((i * 20, sprite))
                text = text.replace(letter, f"    ")
        
        return text, sprites
    
    def rotate_text(self, angle: float):
        self.current_angle += angle
        self.rotation = self.current_angle + 180
        self.position = (
            np.cos(np.radians(self.current_angle)) * TEXT_SIZE + WIDTH / 2,
            np.sin(np.radians(self.current_angle)) * TEXT_SIZE + HEIGHT / 2
        )
        for offset, sprite in self.sprites:
            sprite.angle = self.current_angle + 180
            sprite.position = (
                np.cos(np.radians(self.current_angle)) * (TEXT_SIZE - offset) + WIDTH / 2,
                np.sin(np.radians(self.current_angle)) * (TEXT_SIZE - offset) + HEIGHT / 2
            )
    
    def draw(self):
        super().draw()
        for _, sprite in self.sprites:
            sprite.draw()

class SpinTheWheel(arcade.Window):
    def __init__(self, options: list[str]):
        super().__init__(WIDTH, HEIGHT, "Spin the Wheel")
        arcade.set_background_color((49, 51, 56))
        self.wheel_angle = 0.5
        self.frames = []
        self.options = options
        self.shape_element_list = arcade.ShapeElementList()
        self.sprite_list = arcade.SpriteList()
        self.text_list : list[Text] = []
        self.triangle = arcade.ShapeElementList()
        self.setup(options)
        self.setup_triangle()
        image = create_circular_image("data/avatar.png")
        texture = arcade.Texture("Avatar", image)
        self.avatar_sprite = arcade.Sprite(center_x = WIDTH / 2, center_y = HEIGHT / 2, texture = texture)
    
    @staticmethod
    def get_arc_filled(x, y, radius, color, start_angle, angle):
        angles = np.linspace(start_angle, angle + start_angle, 100)
        x_points = x + radius * np.cos(np.radians(angles))
        y_points = y + radius * np.sin(np.radians(angles))
        x_points = np.append(x_points, x)
        y_points = np.append(y_points, y)
        points = list(zip(x_points, y_points))
        return arcade.create_polygon(points, color), arcade.create_line_strip((points[0], (x, y), points[-2]), arcade.color.WHITE, line_width = 3)

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
                i * alpha + alpha / 2 + self.wheel_angle
            )
            self.text_list.append(text_object)
        
        self.shape_element_list.center_x = WIDTH / 2
        self.shape_element_list.center_y = HEIGHT / 2
    
    def on_update(self, angle: float = 4):
        self.wheel_angle += angle
        self.shape_element_list.angle = self.wheel_angle
        for text in self.text_list:
            text.rotate_text(angle)

        self.avatar_sprite.angle = self.wheel_angle

    def draw_frame(self):
        arcade.start_render()
        self.shape_element_list.draw()
        self.avatar_sprite.draw()
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
    
    def run(self, filename: str = "output.mp4"):
        for _ in range(random.randint(20, 200)):
            self.on_update(14)
            self.draw_frame()
        
        self.slow()
        
        self.save_video(filename)
        self.close()
    

def spin(options: list[str], filename: str = "output.mp4") -> str:
    window = SpinTheWheel(options)
    window.run(filename)

def quickspin(options: list[str], filename: str = "output.png") -> str:
    window = SpinTheWheel(options)
    window.on_update(random.randint(0, 359))
    window.draw_frame()
    window.save_video(filename)

if __name__ == "__main__":
    quickspin(["Herspinnen", "Niet herspinnen", "dsf😭abc😭bla😭", "😭"])

async def setup(*args):
    pass