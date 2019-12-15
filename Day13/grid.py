#!/usr/bin/env python

BLOCK = u"\u2588"
SPACE = u" "
LINE_COLOR = (50, 50, 50)
BACKGROUND_COLOR = (0, 0, 0)
DEFAULT_COLOR_MAP = {
    0: (0, 0, 0),
    ' ': (0, 0, 0),
    '.': (0, 0, 0),
    1: (255, 255, 255),
    '#': (255, 255, 255),
    'Star': (255, 255, 0),
    'star': (255, 255, 0),
    'Target': (192, 192, 255),
    'target': (192, 192, 255),
}
DEFAULT_DISP_MAP = {
    ' ': SPACE,
    0: SPACE,
    '.': SPACE,
    '#': BLOCK,
    1: BLOCK,
}

class Grid:
    def __init__(self, default=0):
        self.grid = {}
        self.default = default
        self.min_x = 0
        self.min_y = 0
        self.max_x = 0
        self.max_y = 0
        self.frame = 0
        self.frames = []

    @staticmethod
    def make_animation(frame_rate=30):
        import os
        import subprocess

        if os.path.isfile("animation.gif"):
            os.unlink("animation.gif")

        subprocess.check_call([
            "ffmpeg", 
            "-hide_banner",
            "-framerate", str(frame_rate), 
            "-i", "frame_%04d.png", 
            "animation.gif",
        ])

    def get(self, x, y):
        return self.grid.get((x, y), self.default)

    def width(self):
        return self.max_x - self.min_x + 1

    def height(self):
        return self.max_y - self.min_y + 1

    def set(self, x, y, value):
        self.min_x = min(self.min_x, x)
        self.min_y = min(self.min_y, y)
        self.max_x = max(self.max_x, x)
        self.max_y = max(self.max_y, y)
        self.grid[(x, y)] = value

    def value_set(self, x, y):
        return (x, y) in self.grid

    def enum_grid(self, callback, include_missing=True):
        for y in range(self.min_y, self.max_y + 1):
            for x in range(self.min_x, self.max_x + 1):
                if include_missing:
                    callback(x, y, self.grid.get((x, y), self.default))
                else:
                    if (x, y) in self.grid:
                        callback(x, y, self.grid[(x, y)])

    def show_grid(self, log, disp_map=DEFAULT_DISP_MAP):
        for y in range(self.min_y, self.max_y + 1):
            line = ""
            for x in range(self.min_x, self.max_x + 1):
                line += disp_map[self.grid.get((x, y), self.default)]
            log.show(line)

    def save_frame(self):
        self.frames.append(self.grid.copy())

    def draw_frames(self, color_map=DEFAULT_COLOR_MAP, cell_size=10, repeat_final=0):
        temp = self.grid
        for cur in self.frames:
            self.grid = cur
            self.draw_grid(color_map=color_map, cell_size=cell_size)
        for _ in range(repeat_final):
            self.draw_grid(color_map=color_map, cell_size=cell_size)
        self.grid = temp

    def draw_grid(self, color_map=DEFAULT_COLOR_MAP, cell_size=10):
        from PIL import Image, ImageDraw
        width = self.max_x - self.min_x + 1
        height = self.max_y - self.min_y + 1

        border = 5
        cell_size = 10

        im = Image.new('RGB', (
            width * (cell_size + 1) + 1 + (border * 2), 
            height * (cell_size + 1) + 1 + (border * 2),
        ), color=BACKGROUND_COLOR)

        d = ImageDraw.Draw(im)
        d.rectangle(
            (
                (border, border), 
                (border + width * (cell_size + 1), border + height * (cell_size + 1))
            ), 
            LINE_COLOR, 
            LINE_COLOR,
        )

        for x in range(width):
            for y in range(height):
                color = self.grid.get((x + self.min_x, y + self.min_y), self.default)
                color = color_map[color]
                d.rectangle(
                    (
                        (border + x * (cell_size + 1) + 1, border + y * (cell_size + 1) + 1), 
                        (border + x * (cell_size + 1) + cell_size, border + y * (cell_size + 1) + cell_size)
                    ),
                    color, color
                )

        del d
        im.save("frame_%04d.png" % (self.frame,))
        self.frame += 1