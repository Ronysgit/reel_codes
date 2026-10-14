import pygame, math, random

pygame.init()
W, H = 900, 900
s = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
dots = [[random.random()*6.28,random.uniform(1,5),random.random()*6.28] for _ in range(450)]
t = 0

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: pygame.quit(); quit()

    s.fill((2,2,12))

    for a,r,z in dots:
        a += t*(1/r)
        x = math.cos(a)*r
        y = math.sin(a)*r
        depth = math.sin(a*2+z)*1.5
        scale = 100/(r+1)
        px = int(W/2 +x*scale*2)
        py = int(H/2 +y*scale*2+depth*30)

        h = (math.degrees(a*3)+t*100)%360
        c = tuple(int(127+127*math.sin(math.radians(h+k*120))) for k in (0,1,2))

        if 0<= px<W and 0<=py<H:
            pygame.draw.circle(s,c, (px,py),max(1,int(4/r)))

    t += .025
    pygame.display.flip()
    clock.tick(60)