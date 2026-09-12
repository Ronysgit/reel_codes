import pygame, random, math, colorsys

pygame.init()

s=pygame.display.set_mode((900,600)); clock=pygame.time.Clock()

P=[]; t=0

def rgb(h):

    return tuple(int(x*255) for x in colorsys.hsv_to_rgb(h%1,1,1))

while 1:

    for e in pygame.event.get():

        if e.type==pygame.QUIT: quit()

    s.fill((2,2,8))

    mx,my=pygame.mouse.get_pos()

    # Ink droplets

    for _ in range(7):

        a=random.random()*math.tau

        v=random.uniform(2,9)

        P.append([mx,my,math.cos(a)*v,math.sin(a)*v,

                  random.randint(25,55),random.random()])

    for p in P[:]:

        p[0]+=p[2]; p[1]+=p[3]

        p[2]*=.97; p[3]*=.97

        p[4]-=1

        if p[4]<=0:

            P.remove(p)

            continue

        r=max(2,p[4]//7)

        pygame.draw.circle(

            s,rgb(t*.01+p[5]),

            (int(p[0]),int(p[1])),r

        )

    # Splash core

    for r in range(32,5,-5):

        pygame.draw.circle(

            s,rgb(t*.02+r*.01),

            (mx,my),r,2

        )

    pygame.draw.circle(s,(255,255,255),(mx,my),4)

    pygame.display.flip()

    t+=1

    clock.tick(60)