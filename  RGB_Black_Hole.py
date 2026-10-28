import pygame, math, colorsys
pygame.init()
s = pygame.display.set_mode((700, 700))
clock = pygame.time.Clock()
t = 0
stars = [(i*37%700, i*91%700, i%3+1) for i in range(180)]

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    s.fill((2, 2, 8))
    for i, (x, y, r) in enumerate(stars):
        pygame.draw.circle(s, (90, 100, 150), (x, y), r)

    for i in range(220):
        a = i*0.19 + t*(1+i%5*.08)
        r = 35 + (i*17 % 260)
        x = 350 + math.cos(a)*r
        y = 350 + math.sin(a)*r*.48
        c = colorsys.hsv_to_rgb((t*.08+i/220)%1, 1, 1)
        c = tuple(int(v*255) for v in c)
        pygame.draw.circle(s, c, (int(x), int(y)), max(1, 4-r//90))

    pygame.draw.circle(s, (0, 0, 0), (350, 350), 42)
    pygame.draw.circle(s, (255, 255, 255), (350, 350), 43, 2)

    pygame.display.flip()
    clock.tick(60)
    t += .035