import turtle
import random

screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Swirling Rainbow Circles")

t = turtle.Turtle()
t.speed(0)
t.width(2)

colors = ["red", "orange", "yellow", "green", "blue", "purple"]

def draw_rainbow_circles():
    for _ in range(100):
        t.color(random.choice(colors))
        radius = random.randint(10, 100)
        t.penup()
        t.setpos(random.randint(-300, 300), random.randint(-300, 300))
        t.pendown()
        t.circle(radius)

draw_rainbow_circles()

turtle.done()
