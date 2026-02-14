from collections import deque

def bfs_search(grid, start, goal, visualizer=None, delay=100):
    """
    Breadth-First Search algorithm that finds the optimal path from start to goal.
    
    Args:
        grid: Grid object containing the environment
        start: Tuple (x, y) representing start position
        goal: Tuple (x, y) representing goal position
        visualizer: GridVisualizer object for visualization (optional)
        delay: Delay in milliseconds between visualization steps
    
    Returns:
        path: List of tuples representing the path from start to goal
        visited: Set of tuples representing all visited nodes
    """
    # Initialize the frontier with the start position
    frontier = deque()
    frontier.append(start)
    
    # Dictionary to track where each node came from
    came_from = {start: None}
    
    # Set to track visited nodes for visualization
    visited = set()
    visited.add(start)
    
    # BFS main loop
    while frontier:
        current = frontier.popleft()
        
        # Visualize current state
        if visualizer:
            visualizer.draw_grid(
                path=None,
                start=start,
                goal=goal,
                visited=visited,
                current=current,
                frontier=list(frontier)
            )
            visualizer.delay(delay)
        
        # Check if we reached the goal
        if current == goal:
            break
        
        # Explore neighbors
        for next_node in grid.get_neighbors(current):
            if next_node not in came_from:
                frontier.append(next_node)
                came_from[next_node] = current
                visited.add(next_node)
    
    # Reconstruct path
    path = []
    if goal in came_from:
        current = goal
        while current is not None:
            path.append(current)
            current = came_from[current]
        path.reverse()
    
    return path, visited
