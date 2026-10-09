import pygame, random, math

pygame.init()
S = pygame.display.set_mode((800, 700))
clock = pygame.time.Clock()

p = [400, 600]
balls = []
score = 0

while 1:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: quit()

    p = list(pygame.mouse.get_pos())

    if random.random()<.06:
        balls.append([
            random.randint(20,780),-20,
            random.randint(3,7),
            random.randint(0,360)
        ])

    S.fill((3,3,12))

    pygame.draw.circle(S,(255,255,255),p,18)
    pygame.draw.circle(S,(0,220,255),p,13)

    for b in balls[:]:
        b[1]+=b[2]
        b[3]+=4

        c = (
            int(127+127*math.sin(math.radians(b[3]))),
            int(127+127*math.sin(math.radians(b[3]+120))),
            int(127+127*math.sin(math.radians(b[3]+240)))
        )

        pygame.draw.circle(S,c,(b[0],int(b[1])),9)

        if math.hypot(b[0]-p[0],b[1]-p[1])<27:
            balls.remove(b)
            score+=1

        elif b[1]>720:
            balls.remove(b)

    font = pygame.font.Font(None, 35)
    S.blit(font.render(f"SCORE {score}",1,"white"),(25,25))

    pygame.display.flip()
    clock.tick(60)