import turtle

screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Neon Mandala Animation")

t = turtle.Turtle()
t.speed(0)
t.width(2)

colors = ["#FF0055", "#00FFCC", "#9900FF", "#FFFF00", "#00FF00", "#FF6600"]

t.penup()
t.goto(0, 0)
t.pendown()

for i in range(150):
    t.color(colors[i % len(colors)])
    t.circle(i, 90)
    t.left(90)
    t.circle(i, 90)
    t.right(30)

screen.exitonclick()
