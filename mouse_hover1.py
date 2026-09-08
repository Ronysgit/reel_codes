import pygame, math, colorsys

pygame.init()
s = pygame.display.set_mode((900, 600))
clock = pygame.time.Clock()
t = 0

def rgb(h):
    return tuple(int(x*255) for x in colorsys.hsv_to_rgb(h%1, 1, 1))

pts = [(x,y) for x in range(100,801,70) for y in range(70,531,70)]

while 1:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: quit()

    s.fill((2,2,8))
    mx,my = pygame.mouse.get_pos()

    for i,(x,y) in enumerate(pts):
        d = math.hypot(mx-x,my-y)
        pull = max(0, 1-d/180)

        x += (mx-x)*pull*0.45
        y += (my-y)*pull*0.45

        r = 3 + pull*8
        col = rgb(t*.015+i*.008)

        pygame.draw.circle(s, col, (int(x),int(y)), int(r))

        if pull > .15:
            pygame.draw.line(s, col, (int(x), int(y)), (mx, my), 1)

    pygame.draw.circle(s, (255,255,255), (mx,my),5)
    pygame.display.flip()

    t += 1
    clock.tick(60) 