import pygame, math

pygame.init()
S = pygame.display.set_mode((800,700))
clock = pygame.time.Clock()
rings = []

def color(h):
    return tuple(127+127*math.sin(h+i*2.094) for i in range(3))

while 1:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: quit()
        if e.type == pygame.MOUSEBUTTONDOWN:
            rings.append([*e.pos,0])

    S.fill((2,2,8))

    for r in rings[:]:
        x,y,n = r
        n += 5

        for k in range(3):
            pygame.draw.circle(
                S, color(n*.04+k),
                (x,y), n+k*12, 2
            )

        r[2] = n
        if n > 350: rings.remove(r)

    pygame.display.flip()
    clock.tick(60)