import arcade, math, colorsys

W, H = 900, 600
t = 0

def rgb(h):
    return tuple(int(x * 255) for x in colorsys.hsv_to_rgb(h % 1, 1, 1))

class RGBEffect(arcade.Window):

    def __init__(self):
        super().__init__(W, H, "RGB Neon Burst")
        arcade.set_background_color((2, 2, 8))

    def on_draw(self):
        global t

        self.clear()

        cx, cy = W // 2, H // 2

        for i in range(180):
            a = i * 0.35 + t * 0.04
            r = (i * 2.2 + t * 2) % 280

            x = cx + math.cos(a) * r
            y = cy + math.sin(a) * r * 0.55

            arcade.draw_circle_filled(
                x, y, 3,
                rgb(t * 0.01 + i / 180)
            )

    def on_update(self, delta_time):
        global t
        t += 1

RGBEffect()
arcade.run()