import arcade, math, colorsys

W, H = 900, 600
t = 0

def rgb(h):
    return tuple(int(x * 255) for x in colorsys.hsv_to_rgb(h % 1, 1, 1))

class RGBWave(arcade.Window):
    def __init__(self):
        super().__init__(W, H, "RGB Wave Field")
        arcade.set_background_color((2, 2, 8))

    def on_draw(self):
        global t
        self.clear()

        for i in range(16):
            pts = []

            for x in range(0, W + 10, 10):
                y = 300 + math.sin(x*.018 + t*.05 + i*.35) * 55
                y += math.sin(x*.035 - t*.03) * 25
                pts.append((x, y, i*7 - 55))

            arcade.draw_line_strip(
                pts, rgb(t*.01 + i/16), 3
            )

    def on_update(self, dt):
        global t
        t += 1

RGBWave()
arcade.run()