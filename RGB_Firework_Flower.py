import turtle, math, colorsys

s = turtle.Screen()
s.bgcolor("black")
s.setup(900, 700)
s.colormode(255)

t = turtle.Turtle()
t.speed(0)
t.hideturtle()
t.width(2)

for i in range(180):
    hue = i / 180
    t.pencolor(tuple(int(x*255) for x in colorsys.hsv_to_rgb(hue, 1, 1)))

    for j in range(2):
        t.forward(180)
        t.backward(180)
        t.right(1)

    t.right(2)

turtle.done()