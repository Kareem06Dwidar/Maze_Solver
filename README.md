# Maze Solver Visualization

This repository contains Python implementations of maze-solving algorithms—A*, Breadth-First Search (BFS), and Depth-First Search (DFS)—along with a GUI for visualizing their operations. The algorithms are applied to solve mazes represented in text files.

## Features
- **A star Search Algorithm**: Uses a heuristic to find the shortest path efficiently.
- **BFS Algorithm**: Explores the maze layer by layer.
- **DFS Algorithm**: Explores paths deeply before backtracking.
- **GUI Integration**: A user-friendly interface to load mazes, solve them, and visualize paths.

## Files
- **A_Star.py**: Contains the A* algorithm implementation with GUI support.
- **BFS.py**: Implements the BFS algorithm with GUI.
- **DFS.py**: Implements the DFS algorithm with GUI.
- **maze1.txt, maze2.txt, maze3.txt**: Sample maze files for testing.

## Maze Format
The mazes are represented as `.txt` files with the following symbols:
- `#`: Wall
- `.`: Open path
- `O`: Start point
- `B`: End point

Example maze:
```
#######
#O....#
#.#.#.#
#..B#.#
#######
```

## Requirements
- Python 3.6 or above
- `tkinter` library (comes pre-installed with Python)

## Usage
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/maze-solver-visualization.git
   ```
2. Navigate to the project directory:
   ```bash
   cd maze-solver-visualization
   ```
3. Run any of the scripts:
   ```bash
   python A_Star.py
   ```
4. Use the GUI to:
   - Load a maze file.
   - Solve it using the respective algorithm.
   - Visualize the solution path.



