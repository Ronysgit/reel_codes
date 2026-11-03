import pygame, math, random, colorsys

pygame.init()
W, H = 800, 800
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("RGB ENERGY PORTAL")
clock = pygame.time.Clock()

particles = []
t = 0

def rgb(h):
    return tuple(int(c * 255) for c in colorsys.hsv_to_rgb(h % 1, 1, 1))

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    t += 0.025
    screen.fill((3, 2, 12))
    cx, cy = W // 2, H // 2

    # Rotating neon portal rings
    for i in range(12):
        r = 65 + i * 19
        col = rgb(t + i / 12)
        rect = pygame.Rect(cx-r, cy-r, r*2, r*2)
        pygame.draw.arc(screen, col, rect, t*2+i, t*2+i+4.5, 3)

    # Energy particles shooting outward
    if random.random() < 0.8:
        a = random.random() * math.tau
        particles.append([cx, cy, math.cos(a)*random.uniform(2, 7),
                          math.sin(a)*random.uniform(2, 7), 0])

    for p in particles[:]:
        p[0] += p[2]
        p[1] += p[3]
        p[4] += 1
        col = rgb(t + p[4] * 0.01)

        if p[4] < 70:
            pygame.draw.circle(screen, col,
                               (int(p[0]), int(p[1])),
                               max(1, 4 - p[4] // 20))
        else:
            particles.remove(p)

    # Glowing core
    for r in range(35, 0, -5):
        pygame.draw.circle(screen, rgb(t + r/80), (cx, cy), r)

    pygame.display.flip()
    clock.tick(60)