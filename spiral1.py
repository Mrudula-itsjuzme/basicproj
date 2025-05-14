import turtle
import random

screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Geometric Pattern")

t = turtle.Turtle()
t.speed(0)
t.width(2)

colors = ["red", "orange", "yellow", "green", "blue", "purple"]

def draw_pattern():
    for _ in range(36):
        t.color(random.choice(colors))
        t.circle(100)
        t.right(10)
        
        t.color(random.choice(colors))
        for _ in range(4):
            t.forward(100)
            t.right(90)

draw_pattern()

turtle.done()
