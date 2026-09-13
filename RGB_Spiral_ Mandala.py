import turtle, colorsys

s = turtle.Screen()
s.bgcolor("black")
s.setup(900,700)
s.colormode(255)

t = turtle.Turtle()
t.speed(0)
t.hideturtle()
t.width(2)

for i in range(360):
    c = colorsys.hsv_to_rgb(i/360, 1, 1)
    t.pencolor(*(int(x*255) for x in c))

    for j in range(3):
        t.forward(i * .8)
        t.left(121)

    t.right(7)
    t.forward(2)

turtle.done()