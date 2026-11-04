import pygame, math, random

pygame.init()
s = pygame.display.set_mode((900, 600))
clock = pygame.time.Clock()
particles = []

t = 0
run = True

while run:
    dt = clock.tick(60) / 1000
    t += dt

    for e in pygame.event.get():
        if e.type == pygame.QUIT: run = False

    s.fill((3, 4, 15))

    x = 450 + math.sin(t * 1.5) * 230
    y = 300 + math.cos(t * 2) * 150

    for _ in range(7):
        particles.append([x, y, random.uniform(-4, 4),
                          random.uniform(-4, 4), 255])

    for p in particles:
        p[0] += p[2]
        p[1] += p[3]
        p[4] -= 3

        c = (max(0, p[4]), 80, 255)
        pygame.draw.circle(s, c, (int(p[0]), int(p[1])), 3)

        if p[4] <= 0: particles.remove(p)

    color = (100 + int(100 * math.sin(t)),
             150, 255)

    pygame.draw.circle(s, color, (int(x), int(y)), 13)
    pygame.draw.circle(s, (255, 255, 255), (int(x), int(y)), 5)

    pygame.display.flip()

pygame.quit()