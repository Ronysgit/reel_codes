import pygame
import math
import random

pygame.init()

W, H = 900, 900
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("RGB Quantum Hourglass")

clock = pygame.time.Clock()
CX, CY = W // 2, H // 2

BLACK = (3, 4, 13)
PARTICLE_COUNT = 650

particles = []
timer = 0
rotation = 0
flipping = False

def rgb(t):
    return (
        int(127 + 128 * math.sin(t)),
        int(127 + 128 * math.sin(t + 2.1)),
        int(127 + 128 * math.sin(t + 4.2))
    )

def chamber_width(y):
    return 18 + abs(y - CY) * 0.55

def create_particle():
    y = random.uniform(100, 420)
    width = chamber_width(y) - 12

    return {
        "x": random.uniform(-width, width),
        "y": y,
        "vx": random.uniform(-25, 25),
        "vy": random.uniform(20, 150),
        "size": random.uniform(1.5, 3.5),
        "phase": random.random() * 6
    }

for _ in range(PARTICLE_COUNT):
    particles.append(create_particle())

def draw_glass():
    points = [
        (CX - 220, CY - 350),
        (CX - 15, CY),
        (CX - 220, CY + 350),
        (CX + 220, CY + 350),
        (CX + 15, CY),
        (CX + 220, CY - 350)
    ]

    for i in range(len(points)):
        a = points[i]
        b = points[(i + 1) % len(points)]

        pygame.draw.line(screen, (30, 100, 145), a, b, 3)

    pygame.draw.line(
        screen, (90, 220, 255),
        (CX - 220, CY - 350),
        (CX + 220, CY - 350), 4
    )

    pygame.draw.line(
        screen, (90, 220, 255),
        (CX - 220, CY + 350),
        (CX + 220, CY + 350), 4
    )

def update_particles(dt, t):
    for p in particles:
        p["vy"] += 190 * dt
        p["x"] += p["vx"] * dt
        p["y"] += p["vy"] * dt

        p["vx"] += math.sin(t * 2 + p["phase"]) * 12 * dt

        width = chamber_width(p["y"])

        if abs(p["x"]) > width:
            p["x"] = math.copysign(width, p["x"])
            p["vx"] *= -0.45

        # Particles leaving the bottom return to the top
        if p["y"] > CY + 345:
            p["y"] = CY - 340
            p["x"] = random.uniform(-160, 160)
            p["vy"] = random.uniform(20, 100)
            p["vx"] = random.uniform(-20, 20)

        # Prevent particles escaping the top
        if p["y"] < CY - 345:
            p["y"] = CY - 345
            p["vy"] = abs(p["vy"]) * 0.4

def draw_particles(t):
    glow = pygame.Surface((W, H), pygame.SRCALPHA)

    for p in particles:
        x = int(CX + p["x"])
        y = int(p["y"])

        color = rgb(t * 0.8 + p["phase"])

        pygame.draw.circle(
            glow, (*color, 45),
            (x, y), int(p["size"] * 4)
        )

        pygame.draw.circle(
            screen, color,
            (x, y), max(1, int(p["size"]))
        )

    screen.blit(glow, (0, 0), special_flags=pygame.BLEND_ADD)

def draw_energy_stream(t):
    for i in range(5):
        offset = math.sin(t * 3 + i) * 9

        pygame.draw.line(
            screen,
            rgb(t + i),
            (CX + offset, CY - 45),
            (CX - offset, CY + 45),
            2
        )

    pygame.draw.circle(
        screen, rgb(t * 2),
        (CX, CY), 9
    )

    pygame.draw.circle(
        screen, (255, 255, 255),
        (CX, CY), 3
    )

running = True

while running:
    dt = min(clock.tick(60) / 1000, 0.03)
    timer += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    # Background atmosphere
    for i in range(4):
        radius = 300 + i * 45
        pygame.draw.circle(
            screen,
            (8, 24, 48),
            (CX, CY), radius, 1
        )

    update_particles(dt, timer)

    draw_glass()
    draw_particles(timer)
    draw_energy_stream(timer)

    # Glass frame highlights
    pygame.draw.circle(
        screen, rgb(timer),
        (CX, CY), 18, 1
    )

    pygame.display.flip()

pygame.quit()