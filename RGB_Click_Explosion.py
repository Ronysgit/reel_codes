import turtle, math, colorsys

s = turtle.Screen()
s.bgcolor("black")
s.setup(900, 700)
s.colormode(255)

t = turtle.Turtle()
t.hideturtle()
t.speed(0)
t.width(2)

def rgb(h):
    return tuple(int(x*255) for x in colorsys.hsv_to_rgb(h % 1, 1, 1))

def click(x, y):
    t.penup()
    t.goto(x, y)
    t.pendown()

    for r in range(10, 170, 12):
        t.pencolor(rgb(r / 170))
        t.circle(r)

    for i in range(36):
        a = i * 10
        r = 180 + math.sin(i * 3) * 35

        t.penup()
        t.goto(x, y)
        t.setheading(a)
        t.pendown()

        t.forward(r)
        t.backward(r)

    t.penup()
    t.goto(x, y)
    t.dot(18, "white")

s.onclick(click)

turtle.mainloop()