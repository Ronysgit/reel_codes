import pygame, math, colorsys
pygame.init()
s = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
t = 0

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    s.fill((3, 3, 15))
    t += 0.04

    for side in [-1, 1]:
        for i in range(5):
            a = t + i * 0.18
            x = 400 + side * (70 + i*13) * abs(math.sin(a))
            y = 300 + math.sin(a*2+i) * (90+i*12)
            hue = (t/5 + i/5 + side*.3) % 1
            c = tuple(int(v*255) for v in colorsys.hsv_to_rgb(hue,1,1))
            pygame.draw.ellipse(s,c,(int(x)-35,int(y)-55,70,110),3)

    pygame.draw.line(s,(255,255,255),(400,230),(400,370),5)
    pygame.draw.circle(s,(255,255,255),(400,300),9)

    pygame.display.flip()
    clock.tick(60) 