import turtle
import random

screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Dynamic Spiral Pattern")

t = turtle.Turtle()
t.speed(0)
t.width(2)

colors = ["red", "orange", "yellow", "green", "blue", "purple"]

def draw_spiral_pattern():
    for i in range(100):
        t.color(random.choice(colors))
        size = 20 + i * 5
        for _ in range(4):
            t.forward(size)
            t.right(90)
        t.right(15)

draw_spiral_pattern()

turtle.done()
