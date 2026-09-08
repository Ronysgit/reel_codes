import pygame, math, colorsys

pygame.init()
s=pygame.display.set_mode((900,600)); clock=pygame.time.Clock()
t=0

def rgb(h):
    return tuple(int(x*255) for x in colorsys.hsv_to_rgb(h%1,1,1))

while 1:
    for e in pygame.event.get():
        if e.type==pygame.QUIT: quit()

    s.fill((3,3,8))
    mx,my=pygame.mouse.get_pos()

    for i in range(9):
        x=450+math.cos(t*.025+i*.7)*220
        y=300+math.sin(t*.03+i*.7)*150
        d=math.hypot(mx-x,my-y)
        r=12+max(0,70-d*.15)

        pygame.draw.circle(s,rgb(t*.01+i*.08),(int(x),int(y)),int(r),2)

        if d<100:
            pygame.draw.circle(s,(255,255,255),(int(x),int(y)),int(r+8),2)

    pygame.display.flip()
    t+=1
    clock.tick(60)