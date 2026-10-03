import pygame, math

pygame.init()
screen = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()

A = B = 0

def rot(x,y,z):
    x,z = x*math.cos(A)-z*math.sin(A), x*math.sin(A)+z*math.cos(A)
    y,z = y*math.cos(B)-z*math.sin(B), y*math.sin(B)+z*math.cos(B)
    return x,y,z

def project(x,y,z):
    z += 6
    s = 430/z
    return 400+x*s, 400+y*s

run = True
while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False

    screen.fill((2,3,12))

    for i in range(80):
        u = i * math.pi*2/80
        pts = []

        for j in range(-5,6):
            v = j/5
            r = 2 + .65*v*math.cos(u/2)

            x = r*math.cos(u)
            y = .65*v*math.sin(u/2)
            z = r*math.sin(u)

            x,y,z = rot(x,y,z)
            pts.append(project(x,y,z))

        for k in range(10):
            pygame.draw.line(
                screen,
                (0,120+12*k,255),
                pts[k], pts[k+1], 2
            )

    pygame.draw.circle(screen,(255,0,200),(400,400),5)

    A += .018
    B += .012

    pygame.display.flip()
    clock.tick(60)

pygame.quit()