import tkinter as tk
from tkinter import messagebox, simpledialog, colorchooser
import turtle
import random

class TurtleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Turtle Drawing")

        # Set up the Turtle canvas within the tkinter window
        self.canvas = tk.Canvas(root, width=800, height=300)
        self.canvas.pack()

        # Create a Turtle screen object using the canvas
        self.screen = turtle.TurtleScreen(self.canvas)
        self.screen.bgcolor("white")

        # Create the initial Turtle object
        self.t = turtle.RawTurtle(self.screen)
        self.t.shape("turtle")
        self.t.color("blue")
        self.t.speed(1)  # Initial speed

        self.turtles = [self.t]
        self.pen_size = 1
        self.color = "blue"
        self.speed = 1
        self.move_randomly_running = False
        self.move_randomly_id = None

        self.undo_stack = []
        self.redo_stack = []

        # Create control buttons and options
        self.create_controls()

        # Bind keys to turtle movement
        self.root.bind('<w>', lambda e: self.move_up())
        self.root.bind('<s>', lambda e: self.move_down())
        self.root.bind('<a>', lambda e: self.move_left())
        self.root.bind('<d>', lambda e: self.move_right())

        # Show welcome screen
        self.show_welcome_screen()

    def show_welcome_screen(self):
        messagebox.showinfo("Welcome!", "Welcome to Interactive Turtle Drawing!\n\n"
                                        "Use the arrow keys (WASD) to move the turtle.\n"
                                        "Explore various drawing options and have fun!")

    def create_controls(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack()

        # Buttons
        tk.Button(control_frame, text="Change Pen Color", command=self.change_color).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(control_frame, text="Increase Pen Size", command=self.increase_size).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(control_frame, text="Decrease Pen Size", command=self.decrease_size).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(control_frame, text="Undo", command=self.undo).grid(row=0, column=3, padx=5, pady=5)
        tk.Button(control_frame, text="Redo", command=self.redo).grid(row=0, column=4, padx=5, pady=5)
        tk.Button(control_frame, text="Clear", command=self.clear).grid(row=0, column=5, padx=5, pady=5)
        tk.Button(control_frame, text="Change Background Color", command=self.change_bg_color).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(control_frame, text="Add Turtle", command=self.add_turtle).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(control_frame, text="Delete Turtle", command=self.delete_turtle).grid(row=1, column=2, padx=5, pady=5)
        tk.Button(control_frame, text="Replicate Drawing", command=self.replicate_drawing).grid(row=1, column=3, padx=5, pady=5)
        tk.Button(control_frame, text="Move Randomly", command=self.start_random_move).grid(row=1, column=4, padx=5, pady=5)
        tk.Button(control_frame, text="Stop Moving", command=self.stop_movement).grid(row=1, column=5, padx=5, pady=5)
        tk.Button(control_frame, text="Text Input", command=self.text_input).grid(row=2, column=0, padx=5, pady=5)
        tk.Button(control_frame, text="Stamp", command=self.stamp).grid(row=2, column=1, padx=5, pady=5)
        tk.Button(control_frame, text="Interactive Help", command=self.show_help).grid(row=2, column=2, columnspan=2, padx=5, pady=5)

        # Additional Options
        tk.Label(control_frame, text="Additional Options", font=("Arial", 12, "bold")).grid(row=3, column=0, columnspan=6, pady=(10, 5))

        tk.Button(control_frame, text="Draw Circle", command=self.draw_circle).grid(row=4, column=0, padx=5, pady=5)
        tk.Button(control_frame, text="Draw Square", command=self.draw_square).grid(row=4, column=1, padx=5, pady=5)
        tk.Button(control_frame, text="Draw Triangle", command=self.draw_triangle).grid(row=4, column=2, padx=5, pady=5)
        tk.Button(control_frame, text="Draw Spiral", command=self.draw_spiral).grid(row=4, column=3, padx=5, pady=5)
        tk.Button(control_frame, text="Draw Star", command=self.draw_star).grid(row=4, column=4, padx=5, pady=5)
        tk.Button(control_frame, text="Random Colors", command=self.random_colors).grid(row=4, column=5, padx=5, pady=5)
        tk.Button(control_frame, text="Draw Hexagon", command=self.draw_hexagon).grid(row=5, column=0, padx=5, pady=5)
        tk.Button(control_frame, text="Draw Pentagon", command=self.draw_pentagon).grid(row=5, column=1, padx=5, pady=5)
        tk.Button(control_frame, text="Draw Octagon", command=self.draw_octagon).grid(row=5, column=2, padx=5, pady=5)
        tk.Button(control_frame, text="Draw Cross", command=self.draw_cross).grid(row=5, column=3, padx=5, pady=5)
        tk.Button(control_frame, text="Draw Heart", command=self.draw_heart).grid(row=5, column=4, padx=5, pady=5)
        tk.Button(control_frame, text="Draw Flower", command=self.draw_flower).grid(row=5, column=5, padx=5, pady=5)
        tk.Button(control_frame, text="Draw Mandelbrot Set", command=self.draw_mandelbrot).grid(row=6, column=0, padx=5, pady=5)
        tk.Button(control_frame, text="Draw Koch Curve", command=self.draw_koch_curve).grid(row=6, column=1, padx=5, pady=5)
        tk.Button(control_frame, text="Fill Color", command=self.fill_color).grid(row=6, column=2, padx=5, pady=5)

        # Speed Control
        tk.Label(control_frame, text="Turtle Speed", font=("Arial", 12, "bold")).grid(row=7, column=0, columnspan=6, pady=(10, 5))

        tk.Button(control_frame, text="Increase Speed", command=self.increase_speed).grid(row=8, column=0, padx=5, pady=5)
        tk.Button(control_frame, text="Decrease Speed", command=self.decrease_speed).grid(row=8, column=1, padx=5, pady=5)

        # Stamp Shape Selection
        tk.Label(control_frame, text="Stamp Shape", font=("Arial", 12, "bold")).grid(row=9, column=0, columnspan=6, pady=(10, 5))
        shapes = ["turtle", "classic", "square", "triangle", "circle"]
        self.stamp_shape_var = tk.StringVar()
        self.stamp_shape_var.set("turtle")
        for i, shape in enumerate(shapes):
            tk.Radiobutton(control_frame, text=shape.capitalize(), variable=self.stamp_shape_var, value=shape, command=self.update_stamp_shape).grid(row=10, column=i, padx=5, pady=5)

    def update_stamp_shape(self):
        shape = self.stamp_shape_var.get()
        for t in self.turtles:
            t.shape(shape)

    def change_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.color = color
            for t in self.turtles:
                t.color(self.color)
    
    def increase_size(self):
        self.pen_size += 1
        for t in self.turtles:
            t.pensize(self.pen_size)
    
    def decrease_size(self):
        if self.pen_size > 1:
            self.pen_size -= 1
            for t in self.turtles:
                t.pensize(self.pen_size)
    
    def undo(self):
        if self.undo_stack:
            action = self.undo_stack.pop()
            action.undo()
            self.redo_stack.append(action)
    
    def redo(self):
        if self.redo_stack:
            action = self.redo_stack.pop()
            action.redo()
            self.undo_stack.append(action)
    
    def clear(self):
        for t in self.turtles:
            t.clear()
        self.undo_stack.clear()
        self.redo_stack.clear()
    
    def change_bg_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.screen.bgcolor(color)
    
    def add_turtle(self):
        new_turtle = turtle.RawTurtle(self.screen)
        new_turtle.shape("turtle")
        new_turtle.color(self.color)
        new_turtle.speed(self.speed)
        self.turtles.append(new_turtle)
    
    def delete_turtle(self):
        if len(self.turtles) > 1:
            turtle_to_delete = self.turtles.pop()
            turtle_to_delete.clear()
            turtle_to_delete.hideturtle()
    
    def replicate_drawing(self):
        for _ in range(10):
            self.draw_square()
            self.move_up()
    
    def start_random_move(self):
        self.move_randomly_running = True
        self.move_randomly()
    
    def move_randomly(self):
        if self.move_randomly_running:
            for t in self.turtles:
                t.setheading(random.choice([0, 90, 180, 270]))
                t.forward(random.randint(10, 50))
            self.move_randomly_id = self.root.after(1000, self.move_randomly)
    
    def stop_movement(self):
        self.move_randomly_running = False
        if self.move_randomly_id:
            self.root.after_cancel(self.move_randomly_id)
        for t in self.turtles:
            t.clear()

    def text_input(self):
        text = simpledialog.askstring("Text Input", "Enter text for turtle to write:")
        if text:
            for t in self.turtles:
                t.write(text, font=("Arial", 12, "normal"))
    
    def stamp(self):
        shape = self.stamp_shape_var.get()
        for t in self.turtles:
            t.shape(shape)
            t.stamp()
    
    def show_help(self):
        messagebox.showinfo("Interactive Turtle Drawing Help", "Click on buttons to draw shapes, change colors, and perform various actions. Use keyboard keys W, A, S, D to move the turtle.Change Pen Color: Opens a color picker to change the turtle's pen color.\n"
            "Increase Pen Size: Increases the pen size used by the turtle.\n"
            "Decrease Pen Size: Decreases the pen size used by the turtle.\n"
            "Undo: Reverts the last action performed by the turtle.\n"
            "Redo: Reapplies the last action that was undone.\n"
            "Clear: Clears the entire drawing canvas.\n"
            "Change Background Color: Opens a color picker to change the background color of the canvas.\n"
            "Add Turtle: Adds a new turtle to the canvas.\n"
            "Delete Turtle: Removes the last added turtle from the canvas.\n"
            "Replicate Drawing: Replicates the drawing of the first turtle onto all other turtles.\n"
            "Move Randomly: Moves all turtles randomly around the canvas.\n"
            "Stop Moving Randomly: Stops the random movement of all turtles.\n"
            "Text Input: Prompts for user input to be written by the turtle.\n"
            "Stamp: Leaves an imprint of the turtle's shape on the canvas.\n"
            "Interactive Help: Opens this help window describing each option.")

    def draw_circle(self):
        for t in self.turtles:
            t.circle(50)
    
    def draw_square(self):
        for t in self.turtles:
            for _ in range(4):
                t.forward(100)
                t.right(90)
    
    def draw_triangle(self):
        for t in self.turtles:
            for _ in range(3):
                t.forward(100)
                t.left(120)
    
    def draw_spiral(self):
        for t in self.turtles:
            for i in range(36):
                t.forward(i * 10)
                t.right(144)
    
    def draw_star(self):
        for t in self.turtles:
            for _ in range(5):
                t.forward(100)
                t.right(144)
    
    def random_colors(self):
        colors = ["red", "orange", "yellow", "green", "blue", "purple"]
        for t in self.turtles:
            t.color(random.choice(colors))
    
    def draw_hexagon(self):
        for t in self.turtles:
            for _ in range(6):
                t.forward(100)
                t.right(60)
    
    def draw_pentagon(self):
        for t in self.turtles:
            for _ in range(5):
                t.forward(100)
                t.right(72)
    
    def draw_octagon(self):
        for t in self.turtles:
            for _ in range(8):
                t.forward(100)
                t.right(45)
    
    def draw_cross(self):
        for t in self.turtles:
            t.forward(100)
            t.backward(50)
            t.right(90)
            t.forward(50)
            t.backward(100)
            t.forward(50)
            t.left(90)
            t.forward(50)
            t.backward(100)
    
    def draw_heart(self):
        for t in self.turtles:
            t.begin_fill()
            t.left(140)
            t.forward(224)
            t.circle(-112, 200)
            t.left(120)
            t.circle(-112, 200)
            t.forward(224)
            t.color('red')
            t.end_fill()
    
    def draw_flower(self):
        for t in self.turtles:
            for _ in range(18):
                t.forward(100)
                t.left(150)
                t.forward(50)
                t.left(180)
                t.forward(50)
                t.left(150)
                t.forward(100)
                t.right(20)
    
    def draw_mandelbrot(self):
        messagebox.showinfo("Mandelbrot Set", "Mandelbrot set drawing feature is not yet implemented.")

    def draw_koch_curve(self):
        def koch_curve(turtle, order, size):
            if order == 0:
                turtle.forward(size)
            else:
                for angle in [60, -120, 60, 0]:
                    koch_curve(turtle, order - 1, size / 3)
                    turtle.left(angle)

        for t in self.turtles:
            koch_curve(t, 3, 300)
    
    def fill_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            for t in self.turtles:
                t.fillcolor(color)
                t.begin_fill()
                # Replace with your shape drawing function
                t.circle(50)
                t.end_fill()

    def move_up(self):
        for t in self.turtles:
            t.setheading(90)
            t.forward(10)
    
    def move_down(self):
        for t in self.turtles:
            t.setheading(270)
            t.forward(10)
    
    def move_left(self):
        for t in self.turtles:
            t.setheading(180)
            t.forward(10)
    
    def move_right(self):
        for t in self.turtles:
            t.setheading(0)
            t.forward(10)
    
    def increase_speed(self):
        self.speed += 1
        for t in self.turtles:
            t.speed(self.speed)
    
    def decrease_speed(self):
        if self.speed > 1:
            self.speed -= 1
            for t in self.turtles:
                t.speed(self.speed)

# Main application entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = TurtleApp(root)
    root.mainloop()
