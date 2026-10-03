import pygame, math

pygame.init()
S = pygame.display.set_mode((900, 700))
clock = pygame.time.Clock()

A = B = hue = 0

def rgb(h):
    h %= 360
    x = int(255 * (1 - abs((h / 60) % 2 - 1)))
    if h < 60: return 255, x, 0
    if h < 120: return x, 255, 0
    if h < 180: return 0, 255, x
    if h < 240: return 0, x, 255
    if h < 300: return x, 0, 255
    return 255, 0, x

def rotate(x,y,z):
    x,z = x*math.cos(A)-z*math.sin(A), x*math.sin(A)+z*math.cos(A)
    y,z = y*math.cos(B)-z*math.sin(B), y*math.sin(B)+z*math.cos(B)
    return x,y,z

def project(x,y,z):
    z += 7
    s = 500 / z
    return int(450+x*s), int(350+y*s)

run = True

while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False

    S.fill((2,2,10))
    left, right =[], []

    for i in range(100):
        t = i * .14
        y = 4.5 - i * .09

        x = 2.0 * math.cos(t)
        z = 2.0 * math.sin(t)

        a = project(*rotate(x,y,z))
        b = project(*rotate(-x,y,-z))

        left.append(a)
        right.append(b)

        c1 = rgb(hue + i*3)
        c2 = rgb(hue + i*3 + 120)

        pygame.draw.circle(S, c1, a, 6)
        pygame.draw.circle(S, c2, b, 6)

        if i % 2 == 0:
            pygame.draw.line(S, c1, a, b, 3)

    for strand in (left, right):
        for a,b in zip(strand,strand[1:]):
            pygame.draw.line(S, rgb(hue), a, b, 5)

    A += .018
    B += .025
    hue += 2

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

