import turtle
import random

# Constants
CELL_SIZE = 20
ROWS = 20
COLS = 20

# Maze grid
maze = [[1 for _ in range(COLS)] for _ in range(ROWS)]  # 1 represents walls, 0 represents paths

# Initialize Turtle screen
screen = turtle.Screen()
screen.title("Maze Generator and Solver")
screen.bgcolor("white")
screen.setup(width=CELL_SIZE * COLS + 1, height=CELL_SIZE * ROWS + 1)

# Turtle for drawing maze
drawer = turtle.Turtle()
drawer.speed(0)
drawer.hideturtle()
drawer.penup()
drawer.goto(-COLS * CELL_SIZE / 2, ROWS * CELL_SIZE / 2)
drawer.pendown()
drawer.pensize(2)

# Function to draw a rectangle at given position
def draw_rectangle(x, y, color):
    drawer.penup()
    drawer.goto(x, y)
    drawer.pendown()
    drawer.fillcolor(color)
    drawer.begin_fill()
    for _ in range(4):
        drawer.forward(CELL_SIZE)
        drawer.right(90)
    drawer.end_fill()

# Maze generation using Recursive Backtracking
def generate_maze():
    def inside(x, y):
        return 0 <= x < COLS and 0 <= y < ROWS
    
    def get_neighbors(x, y):
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if inside(nx, ny) and maze[ny][nx] == 1:
                neighbors.append((nx, ny))
        return neighbors
    
    def remove_wall(x1, y1, x2, y2):
        drawer.penup()
        drawer.goto(x1 * CELL_SIZE, -y1 * CELL_SIZE)
        drawer.pendown()
        drawer.goto(x2 * CELL_SIZE, -y2 * CELL_SIZE)
        maze[y1][x1] = 0
        maze[y2][x2] = 0
    
    stack = [(random.randint(0, COLS - 1), random.randint(0, ROWS - 1))]
    while stack:
        x, y = stack[-1]
        maze[y][x] = 0
        neighbors = get_neighbors(x, y)
        if neighbors:
            nx, ny = random.choice(neighbors)
            remove_wall(x, y, nx, ny)
            stack.append((nx, ny))
        else:
            stack.pop()

# Maze solving using Depth-First Search
def solve_maze(x, y):
    def inside(x, y):
        return 0 <= x < COLS and 0 <= y < ROWS
    
    def dfs(x, y):
        if not inside(x, y) or maze[y][x] == 1 or visited[y][x]:
            return False
        visited[y][x] = True
        if (x, y) == (COLS - 1, ROWS - 1):
            return True
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if dfs(x + dx, y + dy):
                return True
        return False
    
    visited = [[False for _ in range(COLS)] for _ in range(ROWS)]
    dfs(x, y)

# Main function
def main():
    generate_maze()
    solve_maze(0, 0)

# Run the main function
if __name__ == "__main__":
    main()

# Keep the window open
screen.mainloop()
