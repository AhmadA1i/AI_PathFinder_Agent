# AI Pathfinder - Uninformed Search Visualization

AI Pathfinder is a Python + Pygame visualization for classic uninformed search
algorithms on a grid world. It highlights frontier, visited, current node,
and the final path to help you compare behavior and performance.

## Features
- Real-time grid visualization with step-by-step animation
- Clear color coding for frontier, visited, current node, path, start, and goal
- Random weighted grids for UCS
- Deterministic neighbor ordering for reproducible paths
- Multiple uninformed search strategies in one interface

## Algorithms Implemented
- Breadth-First Search (BFS)
- Depth-First Search (DFS)
- Uniform Cost Search (UCS)
- Depth-Limited Search (DLS)
- Iterative Deepening DFS (IDDFS)
- Bidirectional Search

## Project Structure
- `main.py` - Entry point and Pygame visualization loop
- `algorithms.py` - Search algorithm implementations
- `grid.py` - Grid representation and neighbor logic
- `requirements.txt` - Python dependencies

## Requirements
- Python 3.8+
- Pygame

Install dependencies:
```bash
pip install -r requirements.txt
```

## Run
```bash
python main.py
```

When prompted, choose an algorithm:
```
bfs, dfs, ucs, dls, iddfs, bidirectional
```

## Controls
- Close the window or press `Esc` to exit

## Visualization Legend
- Green: Start
- Red: Goal
- Yellow: Final path
- Light Blue: Visited nodes
- Purple: Frontier
- Orange: Current node
- Black: Walls

## Notes
- UCS assigns random weights to all non-wall cells at runtime.
- DLS requires a depth limit; IDDFS increases the limit until a path is found.
- Neighbor expansion order is fixed to ensure consistent results.

## Troubleshooting
- If Pygame fails to initialize, update your graphics drivers and ensure
	you are using a supported Python version.
- On Windows, run from a terminal that has access to the Python environment
	where `pygame` is installed.

