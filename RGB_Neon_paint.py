import pygame, math

pygame.init()
s = pygame.display.set_mode((900,700))
clock = pygame.time.Clock()

trail = []
h = 0

while 1:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: quit()
        if e.type == pygame.MOUSEMOTION:
            trail.append([*e.pos, h])
            h += 4

    s.fill((2,2,8))

    for i in range(1, len(trail)):
        x1,y1,c = trail[i-1]
        x2,y2,_ = trail[i]

        rgb = (
            int(127+127*math.sin(c*.05)),
            int(127+127*math.sin(c*.05+2)),
            int(127+127*math.sin(c*.05+4))
        )

        pygame.draw.line(s, rgb, (x1,y1), (x2,y2), 5)

    trail = trail[-120:]

    pygame.display.flip()
    clock.tick(60)