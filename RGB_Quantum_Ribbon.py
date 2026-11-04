import pygame, math

pygame.init()
screen = pygame.display.set_mode((900, 700))
clock = pygame.time.Clock()

t = 0
running = True

while running:
    t += 0.025

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    screen.fill((3, 4, 14))
    glow = pygame.Surface((900, 700), pygame.SRCALPHA)

    for layer in range(9):
        points = []

        for i in range(500):
            u = i * 0.025
            wave = u + t + layer * 0.18

            x = 450 + (u - 6) * 48
            y = 350 + math.sin(wave * 1.5) * 120
            y += math.sin(wave * 0.7) * 65
            y += math.sin(u * 2 + t) * 35

            points.append((int(x), int(y)))

        color = (
            int(127 + 128 * math.sin(t + layer)),
            int(127 + 128 * math.sin(t + layer + 2)),
            int(127 + 128 * math.sin(t + layer + 4))
        )

        pygame.draw.lines(glow, (*color, 35), False, points, 12)
        pygame.draw.lines(screen, color, False, points, 2)

    screen.blit(glow, (0, 0), special_flags=pygame.BLEND_ADD)
    pygame.display.flip()
    clock.tick(60)
