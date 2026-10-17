import pygame
import os
import random

pygame.init()

# =============== WINDOW ===============
W, H = 900, 700
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("MOTORBIKE RUSH")
clock = pygame.time.Clock()

BASE = os.path.dirname(os.path.abspath(__file__))

# =============== COLORS ===============
GRASS = (28, 105, 58)
GRASS_DARK = (22, 88, 48)
ROAD = (43, 45, 53)
WHITE = (245, 245, 245)
YELLOW = (255, 205, 55)
CYAN = (0, 235, 255)
RED = (255, 65, 90)
BLACK = (7, 11, 22)

font = pygame.font.SysFont("Arial", 25, bold=True)
small = pygame.font.SysFont("Arial", 17, bold=True)
big = pygame.font.SysFont("Arial", 56, bold=True)

# =============== LOAD IMAGES ===============
def load_png(filename):
    path = os.path.join(BASE, filename)

    if not os.path.isfile(path):
        raise FileNotFoundError(
            f"{filename} nahi mili! "
            "Saari PNG files Python file ke same folder mein rakho."
        )

    return pygame.image.load(path).convert_alpha()


def resize_image(image, height):
    width = max(
        1,
        int(image.get_width() * height / image.get_height())
    )
    return pygame.transform.smoothscale(image, (width, height))


bike_original = load_png("bike.png")
car1_original = load_png("car1.png")
car2_original = load_png("car2.png")

bike_image = resize_image(bike_original, 155)
car_images = [car1_original, car2_original]

# =============== ROAD SETTINGS ===============
HORIZON = 145
ROAD_CENTER = W // 2
TOP_WIDTH = 145
BOTTOM_WIDTH = 770
PLAYER_Y = H - 125

# =============== GAME SETTINGS ===============
INITIAL_SPEED = 170.0
SPEED_INCREASE = 22.0
ACCELERATION = 12.0

bike_x = W / 2
bike_speed = INITIAL_SPEED

score = 0.0
road_scroll = 0.0
spawn_timer = 0.0

cars = []
game_over = False
steer = 0
bike_lean = 0.0
speed_level = 0


# =============== ROAD GEOMETRY ===============
def road_width(y):
    t = (y - HORIZON) / (H - HORIZON)
    t = max(0.0, min(1.0, t))
    t = t * t * (3 - 2 * t)

    return TOP_WIDTH + (BOTTOM_WIDTH - TOP_WIDTH) * t


def road_edges(y):
    width = road_width(y)

    return (
        ROAD_CENTER - width / 2,
        ROAD_CENTER + width / 2
    )


def lane_x(lane, y):
    left, right = road_edges(y)
    return left + (right - left) * (lane + 0.5) / 3


# =============== DRAW ROAD ===============
def draw_road():
    screen.fill(GRASS)

    # Grass texture
    stripe_gap = 32
    offset = int(road_scroll * 0.55) % stripe_gap

    for y in range(HORIZON, H, stripe_gap):
        yy = y + offset

        if yy < H:
            pygame.draw.line(
                screen, GRASS_DARK,
                (0, yy), (W, yy), 2
            )

    # Road surface
    left_top = ROAD_CENTER - TOP_WIDTH / 2
    right_top = ROAD_CENTER + TOP_WIDTH / 2
    left_bottom = ROAD_CENTER - BOTTOM_WIDTH / 2
    right_bottom = ROAD_CENTER + BOTTOM_WIDTH / 2

    pygame.draw.polygon(
        screen, ROAD,
        [
            (left_top, HORIZON),
            (right_top, HORIZON),
            (right_bottom, H),
            (left_bottom, H)
        ]
    )

    # No white borders on road sides.
    # Only yellow centre lane markings remain.
    dash_count = 17

    for divider in (1, 2):
        for i in range(dash_count):
            p1 = (
                i / dash_count + road_scroll * 0.0015
            ) % 1.0

            p2 = min(1.0, p1 + 0.025)

            y1 = HORIZON + p1 * p1 * (H - HORIZON)
            y2 = HORIZON + p2 * p2 * (H - HORIZON)

            left1, right1 = road_edges(y1)
            left2, right2 = road_edges(y2)

            x1 = left1 + (right1 - left1) * divider / 3
            x2 = left2 + (right2 - left2) * divider / 3

            thickness = max(1, int(1 + p1 * 4))

            pygame.draw.line(
                screen, YELLOW,
                (int(x1), int(y1)),
                (int(x2), int(y2)),
                thickness
            )


# =============== SPAWN TRAFFIC ===============
def spawn_car():
    lane = random.randint(0, 2)

    cars.append({
        "lane": lane,
        "y": HORIZON + 15,
        "image": random.choice(car_images),
        "lane_offset": random.uniform(-0.02, 0.02)
    })


# =============== DRAW CAR ===============
def draw_car(car):
    y = car["y"]

    depth = (y - HORIZON) / (H - HORIZON)
    depth = max(0.0, min(1.0, depth))

    target_h = max(1, int(24 + depth * 75))
    original = car["image"]

    target_w = max(
        1,
        int(original.get_width() * target_h / original.get_height())
    )

    image = pygame.transform.smoothscale(
        original, (target_w, target_h)
    )

    x = lane_x(car["lane"], y)
    x += car["lane_offset"] * road_width(y)

    rect = image.get_rect(center=(int(x), int(y)))

    # Shadow
    shadow_w = max(4, int(target_w * 0.78))
    shadow_h = max(2, int(target_h * 0.15))

    shadow = pygame.Surface(
        (shadow_w, shadow_h), pygame.SRCALPHA
    )

    pygame.draw.ellipse(
        shadow, (0, 0, 0, 90), shadow.get_rect()
    )

    screen.blit(
        shadow,
        shadow.get_rect(
            center=(int(x), int(y + target_h * 0.42))
        )
    )

    screen.blit(image, rect)

    # Collision box
    hitbox = pygame.Rect(
        int(x - target_w * 0.32),
        int(y - target_h * 0.36),
        max(1, int(target_w * 0.64)),
        max(1, int(target_h * 0.72))
    )

    return hitbox


# =============== SCOREBOARD ===============
def draw_hud():
    pygame.draw.rect(
        screen, BLACK,
        (20, 20, 280, 145),
        border_radius=14
    )

    pygame.draw.rect(
        screen, CYAN,
        (20, 20, 280, 145),
        2, border_radius=14
    )

    screen.blit(
        font.render("MOTORBIKE RUSH", True, CYAN),
        (35, 30)
    )

    screen.blit(
        font.render(
            f"SPEED: {int(bike_speed)} KM/H",
            True, WHITE
        ),
        (35, 70)
    )

    screen.blit(
        font.render(
            f"SCORE: {int(score)}",
            True, RED
        ),
        (35, 110)
    )

    next_score = (speed_level + 1) * 200
    remaining = max(0, next_score - int(score))

    screen.blit(
        small.render(
            f"NEXT SPEED UP: {remaining}",
            True, YELLOW
        ),
        (W - 230, 25)
    )

    pygame.draw.rect(
        screen, (45, 50, 65),
        (W - 230, 55, 195, 16),
        border_radius=8
    )

    bar_value = min(1.0, bike_speed / 400)

    pygame.draw.rect(
        screen, CYAN,
        (W - 230, 55, int(195 * bar_value), 16),
        border_radius=8
    )

    screen.blit(
        small.render("LEFT / RIGHT: STEER", True, WHITE),
        (20, H - 58)
    )

    screen.blit(
        small.render("R: RESTART     ESC: EXIT", True, WHITE),
        (20, H - 32)
    )


# =============== RESET GAME ===============
def reset_game():
    global bike_x, bike_speed, score, road_scroll
    global spawn_timer, game_over, cars, steer
    global bike_lean, speed_level

    bike_x = W / 2
    bike_speed = INITIAL_SPEED

    score = 0.0
    road_scroll = 0.0
    spawn_timer = 0.0

    cars = []
    game_over = False
    steer = 0
    bike_lean = 0.0
    speed_level = 0


# =============== MAIN GAME LOOP ===============
running = True

while running:
    dt = min(clock.tick(60) / 1000.0, 0.035)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_r:
                reset_game()

    keys = pygame.key.get_pressed()

    if not game_over:

        # ---------------------------------
        # AUTOMATIC, GRADUAL ACCELERATION
        # ---------------------------------
        speed_level = int(score // 200)

        target_speed = (
            INITIAL_SPEED + speed_level * SPEED_INCREASE
        )

        # Speed can only increase, never decrease automatically.
        if bike_speed < target_speed:
            bike_speed = min(
                target_speed,
                bike_speed + ACCELERATION * dt
            )

        # ---------------------------------
        # PLAYER CONTROLS: STEERING ONLY
        # ---------------------------------
        steer = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            steer = -1

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            steer = 1

        bike_x += steer * (260 + bike_speed * 0.32) * dt

        # Smooth bike lean
        target_lean = -steer * 10

        bike_lean += (
            target_lean - bike_lean
        ) * min(1.0, dt * 9)

        # Keep bike on road
        left, right = road_edges(PLAYER_Y)

        bike_x = max(
            left + bike_image.get_width() * 0.40,
            min(
                right - bike_image.get_width() * 0.40,
                bike_x
            )
        )

        # ---------------------------------
        # ROAD MOVEMENT AND SCORE
        # ---------------------------------
        road_scroll += bike_speed * dt * 1.55
        score += bike_speed * dt * 0.045

        # ---------------------------------
        # TRAFFIC SPAWNING
        # ---------------------------------
        spawn_timer += dt

        spawn_interval = max(
            0.55,
            1.25 - speed_level * 0.045
        )

        if spawn_timer >= spawn_interval:
            spawn_car()
            spawn_timer = 0.0

        # ---------------------------------
        # CARS APPROACH PLAYER
        # ---------------------------------
        for car in cars:
            depth = max(
                0.0,
                min(
                    1.0,
                    (car["y"] - HORIZON) / (H - HORIZON)
                )
            )

            approach_speed = (
                95 + bike_speed * 0.95
            ) * (0.55 + depth * 0.85)

            car["y"] += approach_speed * dt

        cars = [
            car for car in cars
            if car["y"] < H + 100
        ]

    # =============== DRAW FRAME ===============
    draw_road()

    cars.sort(key=lambda car: car["y"])

    bike_rect = bike_image.get_rect(
        center=(int(bike_x), int(PLAYER_Y))
    )

    bike_hitbox = bike_rect.inflate(
        -int(bike_rect.width * 0.45),
        -int(bike_rect.height * 0.30)
    )

    for car in cars:
        car_hitbox = draw_car(car)

        if (
            not game_over
            and bike_hitbox.colliderect(car_hitbox)
        ):
            game_over = True
            bike_speed = 0

    # Draw player bike
    rotated_bike = pygame.transform.rotate(
        bike_image, bike_lean
    )

    rotated_rect = rotated_bike.get_rect(
        center=(int(bike_x), int(PLAYER_Y))
    )

    screen.blit(rotated_bike, rotated_rect)

    draw_hud()

    # =============== CRASH SCREEN ===============
    if game_over:
        overlay = pygame.Surface(
            (W, H), pygame.SRCALPHA
        )

        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        title = big.render(
            "BIKE CRASHED!", True, RED
        )

        screen.blit(
            title,
            title.get_rect(
                center=(W // 2, H // 2 - 45)
            )
        )

        final_score = font.render(
            f"FINAL SCORE: {int(score)}",
            True, WHITE
        )

        screen.blit(
            final_score,
            final_score.get_rect(
                center=(W // 2, H // 2 + 5)
            )
        )

        restart = font.render(
            "PRESS R TO RESTART", True, CYAN
        )

        screen.blit(
            restart,
            restart.get_rect(
                center=(W // 2, H // 2 + 55)
            )
        )

    pygame.display.flip()

pygame.quit()