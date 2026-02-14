from collections import deque
import heapq

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


def dfs_search(grid, start, goal, visualizer=None, delay=100):
    """
    Depth-First Search algorithm that finds a path from start to goal.
    
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
    
    # DFS main loop
    while frontier:
        current = frontier.pop()  # Pop from the end to simulate DFS behavior
        
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


def ucs_search(grid, start, goal, visualizer=None, delay=100):
    """
    Uniform Cost Search algorithm that finds the optimal path from start to goal.
    
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
    frontier = []
    heapq.heappush(frontier, (0, start))  # (cost, node)
    
    # Dictionary to track where each node came from
    came_from = {start: None}
    
    # Dictionary to track the cost to reach each node
    cost_so_far = {start: 0}
    
    # Set to track visited nodes for visualization
    visited = set()
    
    # UCS main loop
    while frontier:
        current_cost, current = heapq.heappop(frontier)  # Pop the node with the lowest cost
        
        # Skip if we've already visited this node
        if current in visited:
            continue
        
        visited.add(current)
        
        # Visualize current state
        if visualizer:
            visualizer.draw_grid(
                path=None,
                start=start,
                goal=goal,
                visited=visited,
                current=current,
                frontier=[node for _, node in frontier]
            )
            visualizer.delay(delay)
        
        # Check if we reached the goal
        if current == goal:
            break
        
        # Explore neighbors
        for next_node in grid.get_neighbors(current):
            new_cost = cost_so_far[current] + grid.cost(next_node)
            
            # Only add neighbor if not visited or if we found a cheaper path
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                came_from[next_node] = current
                heapq.heappush(frontier, (new_cost, next_node))
    
    # Reconstruct path
    path = []
    if goal in came_from:
        current = goal
        while current is not None:
            path.append(current)
            current = came_from[current]
        path.reverse()
    
    return path, visited