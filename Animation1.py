import turtle

screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Spiral Animation")

t = turtle.Turtle()
t.speed(0)
turtle.colormode(255)

colors = ["red", "orange", "yellow", "green", "blue", "purple"]

lenght = 100
angle = 59

for i in range(300):
    t.color(colors[i % len(colors)])

    t.forward(lenght)
    t.left(angle)

    lenght += 1

screen.exitonclick()