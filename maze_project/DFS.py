import tkinter as tk  # Import the Tkinter library for GUI
from tkinter import filedialog  # Import the filedialog module for file selection
from enum import Enum  # Import the Enum class for representing directions

# Section 1: Enums and Helper Classes
# ------------------------------------

# Enum to represent directions
class Direction(Enum):
    EAST = 'E'
    WEST = 'W'
    NORTH = 'N'
    SOUTH = 'S'

# Class representing a cell in the maze
class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Class representing the maze
class Maze:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.maze_map = [[False] * cols for _ in range(rows)]  # 2D array representing the maze
        self.start = None  # Start point in the maze
        self.finish = None  # Finish point in the maze

    # Method to load maze from a text file
    def load_maze_from_file(self, filename):
        with open(filename, 'r') as file:
            maze_lines = file.readlines()
        maze_lines = [line.strip() for line in maze_lines]

        for i in range(len(maze_lines)):
            for j in range(len(maze_lines[i])):
                if maze_lines[i][j] == '#':
                    self.maze_map[i][j] = True  # Wall
                elif maze_lines[i][j] == '.':
                    self.maze_map[i][j] = False  # Open space
                elif maze_lines[i][j] == 'O':
                    self.start = (i, j)  # Set start point
                elif maze_lines[i][j] == 'B':
                    self.finish = (i, j)  # Set finish point

    # Method to check if a move is valid in a given direction
    def is_valid_move(self, cell, direction):
        x, y = cell
        if direction == 'E' and y + 1 < self.cols and not self.maze_map[x][y + 1]:
            return True
        elif direction == 'W' and y - 1 >= 0 and not self.maze_map[x][y - 1]:
            return True
        elif direction == 'N' and x - 1 >= 0 and not self.maze_map[x - 1][y]:
            return True
        elif direction == 'S' and x + 1 < self.rows and not self.maze_map[x + 1][y]:
            return True
        return False

    # Method to get the child cell in a given direction
    def get_child_cell(self, cell, direction):
        x, y = cell
        if direction == 'E':
            return x, y + 1
        elif direction == 'W':
            return x, y - 1
        elif direction == 'N':
            return x - 1, y
        elif direction == 'S':
            return x + 1, y

# Section 2: Maze Solving Algorithms
# -----------------------------------

# Function for Depth-First Search (DFS) algorithm
def dfs(maze):
    # Initialization
    start = maze.start  # The starting point of the maze.
    explored = [start]  # A list to keep track of cells that have been explored.
    frontier = [start]  # A list that acts as a stack to store cells to be explored.
    dfsPath = {}  # A dictionary to store the parent-child relationship for each explored cell.

    # Explore the maze using Depth-First Search (DFS)
    while len(frontier) > 0:
        currCell = frontier.pop()  # Get the current cell from the top of the stack.

        # Check if the current cell is the finish point of the maze.
        if currCell == maze.finish:
            break

        # Explore adjacent cells in all possible directions (East, South, North, West).
        for d in 'ESNW':
            if maze.is_valid_move(currCell, d):
                childCell = maze.get_child_cell(currCell, d)

                # Skip already explored cells.
                if childCell in explored:
                    continue

                # Mark the child cell as explored and record its parent (current cell).
                explored.append(childCell)
                frontier.append(childCell)
                dfsPath[childCell] = currCell

    # Reconstruct the forward path from the finish point to the start point.
    fwdPath = {}
    cell = maze.finish
    while cell != start:
        fwdPath[dfsPath[cell]] = cell
        cell = dfsPath[cell]

    return fwdPath

# Section 3: GUI Implementation
# ------------------------------

# Class for the maze solver GUI
class MazeSolverGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Maze Solver (DFS)")

        self.maze = Maze(5, 7)  # Create an instance of the Maze class

        # Create a canvas for drawing the maze
        self.canvas = tk.Canvas(self.master, width=500, height=350, borderwidth=0, highlightthickness=0)
        self.canvas.grid(row=0, column=0, columnspan=3)

        # Buttons and labels for the GUI
        self.load_button = tk.Button(self.master, text="Load Maze", command=self.load_maze)
        self.load_button.grid(row=1, column=0, pady=10)

        self.solve_button = tk.Button(self.master, text="Solve Maze", command=self.solve_maze)
        self.solve_button.grid(row=1, column=1, pady=10)

        self.clear_button = tk.Button(self.master, text="Clear Path", command=self.clear_path)
        self.clear_button.grid(row=1, column=2, pady=10)

        self.start_label = tk.Label(self.master, text="Start Point:")
        self.start_label.grid(row=2, column=0, pady=10)

        self.end_label = tk.Label(self.master, text="End Point:")
        self.end_label.grid(row=2, column=2, pady=10)

    # Method to load maze from a file
    def load_maze(self):
        file_path = filedialog.askopenfilename(initialdir="/", title="Select Maze File",
                                               filetypes=[("Text files", "*.txt")])
        if file_path:
            self.maze.load_maze_from_file(file_path)
            self.draw_maze()

    # Method to draw the maze on the canvas
    def draw_maze(self):
        self.canvas.delete("all")  # Clear canvas
        cell_width = 500 // self.maze.cols
        cell_height = 350 // self.maze.rows

        # Draw each cell in the maze
        for i in range(self.maze.rows):
            for j in range(self.maze.cols):
                x1, y1 = j * cell_width, i * cell_height
                x2, y2 = (j + 1) * cell_width, (i + 1) * cell_height

                if self.maze.maze_map[i][j]:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="black")
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="white")

        self.start_label.config(text=f"Start Point: {self.maze.start}")
        self.end_label.config(text=f"End Point: {self.maze.finish}")

    # Method to solve the maze using DFS and highlight the path
    def solve_maze(self):
        solution_path = dfs(self.maze)
        self.highlight_path(solution_path)

    # Method to clear the highlighted path on the canvas
    def clear_path(self):
        self.canvas.delete("path")

    # Method to highlight the path on the canvas
    def highlight_path(self, path):
        cell_width = 500 // self.maze.cols
        cell_height = 350 // self.maze.rows

        # Draw rectangles to represent the path
        for cell in path.keys():
            i, j = cell
            x1, y1 = j * cell_width, i * cell_height
            x2, y2 = (j + 1) * cell_width, (i + 1) * cell_height

            self.canvas.create_rectangle(x1, y1, x2, y2, fill="green", tags="path")

        # Highlight Start and End Points
        i, j = self.maze.start
        start_x1, start_y1 = j * cell_width, i * cell_height
        start_x2, start_y2 = (j + 1) * cell_width, (i + 1) * cell_height
        self.canvas.create_rectangle(start_x1, start_y1, start_x2, start_y2, fill="red", tags="path")

        i, j = self.maze.finish
        finish_x1, finish_y1 = j * cell_width, i * cell_height
        finish_x2, finish_y2 = (j + 1) * cell_width, (i + 1) * cell_height
        self.canvas.create_rectangle(finish_x1, finish_y1, finish_x2, finish_y2, fill="yellow", tags="path")

# Section 4: Main Application Entry Point
# ----------------------------------------

# Main application entry point
if __name__ == "__main__":
    root = tk.Tk()  # Create the main window
    app = MazeSolverGUI(root)  # Create an instance of the MazeSolverGUI class
    root.mainloop()  # Run the Tkinter event loop
