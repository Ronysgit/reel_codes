import pygame, math, colorsys

pygame.init()
s=pygame.display.set_mode((900,600)); c=pygame.time.Clock()
t=0

def rgb(h):
    return tuple(int(x*255) for x in colorsys.hsv_to_rgb(h%1,1,1))

while 1:
    for e in pygame.event.get():
        if e.type==pygame.QUIT: quit()

    s.fill((2,2,8))

    for j in range(7):
        pts=[]
        for x in range(0,901,8):
            y=300+math.sin(x*.012+t*.045+j)*70
            y+=math.sin(x*.025-t*.03+j*1.7)*35
            y+=j*9-27
            pts.append((x,y))

        pygame.draw.lines(s,rgb(t*.008+j*.08),False,pts,3)

    pygame.display.flip()
    t+=1
    c.tick(60)