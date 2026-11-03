import pygame
import math
import random

pygame.init()

W, H = 900, 900
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("RGB Mechanical Iris")

clock = pygame.time.Clock()

CX, CY = W // 2, H // 2
BLACK = (3, 4, 12)

BLADE_COUNT = 10
particles = []

for _ in range(100):
    particles.append([
        random.uniform(0, math.tau),
        random.uniform(180, 430),
        random.uniform(0.5, 2.5)
    ])

def rgb(t):
    return (
        int(127 + 128 * math.sin(t)),
        int(127 + 128 * math.sin(t + 2.1)),
        int(127 + 128 * math.sin(t + 4.2))
    )

def point(angle, radius):
    return (
        CX + math.cos(angle) * radius,
        CY + math.sin(angle) * radius
    )

def draw_ring(surface, radius, color, width=2):
    pygame.draw.circle(surface, color, (CX, CY), int(radius), width)

running = True
time = 0

while running:
    dt = clock.tick(60) / 1000
    time += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    glow = pygame.Surface((W, H), pygame.SRCALPHA)

    # Opening and closing iris
    opening = 105 + 65 * (0.5 + 0.5 * math.sin(time * 1.4))
    rotation = time * 0.35

    outer_radius = 285

    # Mechanical blades
    for i in range(BLADE_COUNT):
        angle = rotation + i * math.tau / BLADE_COUNT

        spread = math.tau / BLADE_COUNT

        points = []

        for j in range(9):
            a = angle + j * spread / 8
            points.append(point(a, outer_radius))

        for j in range(8, -1, -1):
            a = angle + j * spread / 8
            points.append(point(a, opening))

        color = rgb(time * 0.7 + i * 0.35)

        pygame.draw.polygon(glow, (*color, 35), points)
        pygame.draw.polygon(screen, color, points, 2)

        # Blade highlights
        pygame.draw.line(
            screen,
            color,
            point(angle, opening),
            point(angle + spread, outer_radius),
            2
        )

    # Rotating mechanical rings
    for i in range(5):
        radius = 310 + i * 16
        color = rgb(time + i * 0.5)

        draw_ring(screen, radius, color, 2)

    # Inner aperture rings
    draw_ring(screen, opening, rgb(time * 1.5), 3)
    draw_ring(screen, opening + 12, rgb(time * 1.5 + 1), 1)

    # Rotating ticks
    for i in range(72):
        angle = i * math.tau / 72 + rotation

        r1 = 390
        r2 = 405 if i % 6 == 0 else 397

        pygame.draw.line(
            screen,
            rgb(time + i * 0.08),
            point(angle, r1),
            point(angle, r2),
            2
        )

    # Floating particles
    for p in particles:
        p[0] += p[2] * dt * 0.25

        x, y = point(p[0], p[1])

        color = rgb(time + p[0])

        pygame.draw.circle(
            screen, color,
            (int(x), int(y)), 2
        )

    # Central energy core
    core_color = rgb(time * 2)

    pygame.draw.circle(screen, core_color, (CX, CY), 16)
    pygame.draw.circle(screen, (255, 255, 255), (CX, CY), 5)

    # Glow layers
    screen.blit(glow, (0, 0), special_flags=pygame.BLEND_ADD)

    pygame.display.flip()

pygame.quit()