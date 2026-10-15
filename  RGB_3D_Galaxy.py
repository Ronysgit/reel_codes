import pygame, math, random

pygame.init()
s = pygame.display.set_mode((900, 800))
clock = pygame.time.Clock()

stars = [[random.random()*6.28, random.uniform(.3, 3.5),
          random.uniform(-1, 1)] for _ in range(700)]
t = 0

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            quit()

    s.fill((2, 2, 12))
    mx, my = pygame.mouse.get_pos()
    angle = t + (mx-450)*.001

    for a, r, z in stars:
        a += angle / (r+.3)
        x = math.cos(a)*r*100
        y = math.sin(a)*r*45 + z*30
        depth = 500/(r+2)

        px = int(450+x*depth/100)
        py = int(400+y*depth/100)

        h = (math.degrees(a*4)+t*100)%360
        c = tuple(int(127+127*math.sin(math.radians(h+k*120)))
                  for k in (0,1,2))

        if 0 <= px < 900 and 0 <= py < 800:
            pygame.draw.circle(s,c,(px,py),max(1,int(4/(r+.5))))

    t += .015
    pygame.display.flip()
    clock.tick(60)