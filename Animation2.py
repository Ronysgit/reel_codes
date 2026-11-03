import turtle

# Screen setup
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Centered Beautiful Animation")

# Turtle setup
t = turtle.Turtle()
t.speed(0)  # Maximum speed
turtle.colormode(255)

# Colors list for vibrant look
colors = ["#FF5733", "#33FF57", "#3357FF", "#F3FF33", "#FF33F3", "#33FFF3"]

# Ensure turtle starts right at the center (0, 0)
t.penup()
t.goto(0, 0)
t.pendown()

# Drawing a perfectly centered symmetrical pattern
for i in range(150):
    t.color(colors[i % len(colors)])
    t.circle(i, 90)
    t.left(90)
    t.circle(i, 90)
    t.right(30)

# Keep window open until clicked
screen.exitonclick()