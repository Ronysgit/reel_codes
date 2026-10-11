import turtle
import random
import math

# ==============================
# 3D INTERACTIVE GALAXY
# Python + Turtle
# ==============================

screen = turtle.Screen()
screen.setup(1000, 700)
screen.bgcolor("black")
screen.title("3D Interactive Galaxy - Python Turtle")
screen.tracer(0)

# ------------------------------
# Settings
# ------------------------------

WIDTH = 1000
HEIGHT = 700

STAR_COUNT = 500
GALAXY_RADIUS = 430

# Galaxy rotation
rot_x = 0.35
rot_y = 0.0

# Mouse interaction
dragging = False
last_x = 0
last_y = 0

# ------------------------------
# Star data
# ------------------------------

stars = []

colors = [
    "#ffffff",
    "#bde9ff",
    "#7fd8ff",
    "#fff2a8",
    "#ffd166",
    "#ff9de2",
    "#c9b6ff"
]

for _ in range(STAR_COUNT):

    # Spiral galaxy distribution
    radius = random.uniform(20, GALAXY_RADIUS)

    arm = random.randint(0, 4)

    angle = (
        radius * 0.018
        + arm * (2 * math.pi / 4)
        + random.gauss(0, 0.25)
    )

    # Flat galaxy with some depth
    z = random.gauss(0, 55) * (1 - radius / GALAXY_RADIUS)

    x = math.cos(angle) * radius
    y = math.sin(angle) * radius

    size = random.choice([1, 1, 1, 2, 2, 3])

    stars.append({
        "x": x,
        "y": y,
        "z": z,
        "size": size,
        "color": random.choice(colors),
        "phase": random.random() * math.pi * 2
    })


# ------------------------------
# Turtle drawing object
# ------------------------------

pen = turtle.Turtle()
pen.hideturtle()
pen.penup()
pen.speed(0)


# ------------------------------
# 3D Rotation
# ------------------------------

def rotate_3d(x, y, z):

    # Rotation around X
    cos_x = math.cos(rot_x)
    sin_x = math.sin(rot_x)

    y1 = y * cos_x - z * sin_x
    z1 = y * sin_x + z * cos_x

    # Rotation around Y
    cos_y = math.cos(rot_y)
    sin_y = math.sin(rot_y)

    x2 = x * cos_y + z1 * sin_y
    z2 = -x * sin_y + z1 * cos_y

    return x2, y1, z2


# ------------------------------
# Perspective projection
# ------------------------------

def project(x, y, z):

    camera = 700

    scale = camera / (camera + z)

    screen_x = x * scale
    screen_y = y * scale

    return screen_x, screen_y, scale


# ------------------------------
# Draw galaxy
# ------------------------------

def draw_galaxy():

    pen.clear()

    # Sort stars by depth
    visible_stars = []

    for star in stars:

        x, y, z = rotate_3d(
            star["x"],
            star["y"],
            star["z"]
        )

        sx, sy, scale = project(x, y, z)

        if -500 < sx < 500 and -350 < sy < 350:

            visible_stars.append(
                (z, sx, sy, scale, star)
            )

    # Far stars first
    visible_stars.sort(key=lambda s: s[0])

    for z, sx, sy, scale, star in visible_stars:

        size = max(1, star["size"] * scale)

        pen.goto(sx, sy)

        pen.dot(
            size,
            star["color"]
        )

    # Galaxy core
    pen.goto(0, 0)

    for size in range(50, 5, -5):

        brightness = size / 50

        if brightness > 0.7:
            color = "#fff4c2"
        elif brightness > 0.4:
            color = "#ffd27d"
        else:
            color = "#ff9de2"

        pen.dot(size, color)

    screen.update()


# ------------------------------
# Automatic rotation
# ------------------------------

auto_rotate = True


def animate():

    global rot_y

    if auto_rotate:
        rot_y += 0.008

    draw_galaxy()

    screen.ontimer(animate, 20)


# ------------------------------
# Mouse controls
# ------------------------------

def mouse_down(x, y):

    global dragging, last_x, last_y

    dragging = True
    last_x = x
    last_y = y


def mouse_drag(x, y):

    global rot_x, rot_y
    global last_x, last_y

    if dragging:

        dx = x - last_x
        dy = y - last_y

        rot_y += dx * 0.008
        rot_x += dy * 0.008

        last_x = x
        last_y = y


def mouse_up(x, y):

    global dragging

    dragging = False


# Turtle mouse events
screen.cv.bind(
    "<ButtonPress-1>",
    lambda e: mouse_down(
        e.x - WIDTH / 2,
        HEIGHT / 2 - e.y
    )
)

screen.cv.bind(
    "<B1-Motion>",
    lambda e: mouse_drag(
        e.x - WIDTH / 2,
        HEIGHT / 2 - e.y
    )
)

screen.cv.bind(
    "<ButtonRelease-1>",
    lambda e: mouse_up(
        e.x - WIDTH / 2,
        HEIGHT / 2 - e.y
    )
)


# ------------------------------
# Keyboard controls
# ------------------------------

def toggle_rotation():

    global auto_rotate

    auto_rotate = not auto_rotate


def reset():

    global rot_x, rot_y

    rot_x = 0.35
    rot_y = 0.0


screen.listen()

screen.onkey(
    toggle_rotation,
    "space"
)

screen.onkey(
    reset,
    "r"
)


# ------------------------------
# Start
# ------------------------------

draw_galaxy()
animate()

screen.mainloop()