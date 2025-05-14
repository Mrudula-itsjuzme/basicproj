import turtle
import random

screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Flower Pattern")

t = turtle.Turtle()
t.speed(1000)
t.width(2)

colors = ["red", "orange", "yellow", "green", "blue", "purple"]

def draw_flower():
    for _ in range(36):
        t.color(random.choice(colors))
        for _ in range(4):
            t.forward(100)
            t.right(90)
        t.right(10)

draw_flower()

turtle.done()
