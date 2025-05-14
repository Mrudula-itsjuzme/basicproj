import turtle
import random

screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Dense Starry Night Sky")

t = turtle.Turtle()
t.speed(10000)
t.width(2)

colors = ["white", "yellow", "lightblue", "lightyellow"]

def draw_stars():
    for _ in range(2000):
        size = random.randint(1, 5)
        x = random.randint(-screen.window_width()//2, screen.window_width()//2)
        y = random.randint(-screen.window_height()//2, screen.window_height()//2)
        t.penup()
        t.setpos(x, y)
        t.pendown()
        t.color(random.choice(colors))
        t.begin_fill()
        for _ in range(5):
            t.forward(size * 2)
            t.right(144)
        t.end_fill()

def draw_shooting_stars():
    t.penup()
    t.setpos(-screen.window_width()//2, screen.window_height()//2)
    t.pendown()
    t.speed(5)
    t.pencolor("white")
    for _ in range(10):
        t.forward(150)
        t.penup()
        t.backward(150)
        t.pendown()
        t.right(36)

draw_stars()
draw_shooting_stars()

turtle.done()
