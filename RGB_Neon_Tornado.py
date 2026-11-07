import pygame, math

pygame.init()
s = pygame.display.set_mode((900, 700))
clock = pygame.time.Clock()

t = 0
run = True

while run:
    t += 0.035

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False

    s.fill((3, 3, 12))
    glow = pygame.Surface((900, 700), pygame.SRCALPHA)

    for i in range(900):
        y = i * 0.65 - 250
        radius = 25 + (y + 250) * 0.38
        a = i * 0.19 + t * 4

        x = 450 + math.cos(a) * radius
        yy = 350 + y

        c = (
            int(127 + 128 * math.sin(a + t)),
            int(127 + 128 * math.sin(a + t + 2)),
            int(127 + 128 * math.sin(a + t + 4)),
        )

        pygame.draw.circle(glow, (*c, 35),
                            (int(x), int(yy)), 7)
        pygame.draw.circle(s, c,
                           (int(x), int(yy)), 2)

    s.blit(glow, (0, 0), special_flags=pygame.BLEND_ADD)
    pygame.display.flip()
    clock.tick(60)


