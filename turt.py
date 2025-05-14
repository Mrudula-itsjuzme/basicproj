import tkinter as tk
from tkinter import messagebox, simpledialog, colorchooser
import turtle
import random
from PIL import ImageGrab

class TurtleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Turtle Drawing")

        # Set up the Turtle canvas within the tkinter window
        self.canvas = tk.Canvas(root, width=1000, height=350)
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

        # Save Button
        tk.Button(control_frame, text="Save Drawing", command=self.save).grid(row=11, column=0, columnspan=6, pady=(10, 5))

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
            turtle_to_delete.hideturtle()
            turtle_to_delete.clear()
    
    def replicate_drawing(self):
        self.screen.update()
        x, y, w, h = self.screen.window_geometry()
        image = ImageGrab.grab((x, y, x + w, y + h))
        image.show()
    
    def start_random_move(self):
        if not self.move_randomly_running:
            self.move_randomly_running = True
            self.move_randomly_id = self.root.after(100, self.random_move)
    
    def stop_movement(self):
        if self.move_randomly_running:
            self.move_randomly_running = False
            self.root.after_cancel(self.move_randomly_id)
    
    def random_move(self):
        for t in self.turtles:
            move = random.choice([self.move_up, self.move_down, self.move_left, self.move_right])
            move()
        if self.move_randomly_running:
            self.move_randomly_id = self.root.after(100, self.random_move)
    
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
    
    def text_input(self):
        text = simpledialog.askstring("Text Input", "Enter text:")
        if text:
            for t in self.turtles:
                t.write(text, font=("Arial", 12, "normal"))
    
    def stamp(self):
        for t in self.turtles:
            t.stamp()
    
    def show_help(self):
        help_text = "Welcome to Interactive Turtle Drawing!\n\n" \
                    "Use the arrow keys (WASD) to move the turtle.\n" \
                    "Explore various drawing options and have fun!\n\n" \
                    "For any queries or assistance, please reach out to our support team."
        messagebox.showinfo("Help", help_text)
    
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
        self.color = random.choice(colors)
        for t in self.turtles:
            t.color(self.color)
    
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
            for _ in range(4):
                t.forward(100)
                t.backward(50)
                t.right(90)
    
    def draw_heart(self):
        for t in self.turtles:
            t.begin_fill()
            t.left(50)
            t.forward(133)
            t.circle(50, 200)
            t.right(140)
            t.circle(50, 200)
            t.forward(133)
            t.end_fill()
    
    def draw_flower(self):
        for t in self.turtles:
            for _ in range(6):
                t.forward(100)
                t.right(60)
            t.right(60)
    
    def draw_mandelbrot(self):
        for t in self.turtles:
            # Your Mandelbrot set drawing code here
            pass
    
    def draw_koch_curve(self):
        for t in self.turtles:
            # Your Koch curve drawing code here
            pass
    
    def fill_color(self):
        for t in self.turtles:
            t.begin_fill()
            # Your fill color logic here
            t.end_fill()
    
    def increase_speed(self):
        self.speed += 1
        for t in self.turtles:
            t.speed(self.speed)
    
    def decrease_speed(self):
        if self.speed > 1:
            self.speed -= 1
            for t in self.turtles:
                t.speed(self.speed)
    
    def save(self):
        x, y, w, h = self.screen.window_geometry()
        x_root, y_root = self.root.winfo_rootx(), self.root.winfo_rooty()
        x_cap, y_cap = x_root + x, y_root + y
        ImageGrab.grab().crop((x_root, y_root, x_cap, y_cap)).save("drawing.png")

# Initialize the tkinter window and TurtleApp
root = tk.Tk()
app = TurtleApp(root)
root.mainloop()
