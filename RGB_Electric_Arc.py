import pygame, random, colorsys, math

pygame.init()
s = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
t = 0

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    s.fill((4, 3, 12))
    t += 0.04
    points = [(100, 300)]

    for i in range(1, 22):
        x = 100 + i * 28
        y = 300 + random.randint(-45, 45)
        points.append((x, y))
    points.append((700, 300))

    for w, bright in [(12, 50), (6, 130), (2, 255)]:
        for i in range(len(points)-1):
            hue = (t + i/len(points)) % 1
            c = tuple(int(v*bright) for v in
                      colorsys.hsv_to_rgb(hue, 1, 1))
            pygame.draw.line(s, c, points[i], points[i+1], w)

    for x, y in [points[0], points[-1]]:
        pygame.draw.circle(s, (255, 255, 255), (x, y), 9)

    pygame.display.flip()
    clock.tick(30)