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


def dls_search(grid, start, goal, depth_limit, visualizer=None, delay=100):
    """
    Depth-Limited Search algorithm that finds a path within a depth limit.
    
    Args:
        grid: Grid object containing the environment
        start: Tuple (x, y) representing start position
        goal: Tuple (x, y) representing goal position
        depth_limit: Maximum depth to search
        visualizer: GridVisualizer object for visualization (optional)
        delay: Delay in milliseconds between visualization steps
    
    Returns:
        path: List of tuples representing the path from start to goal
        visited: Set of tuples representing all visited nodes
    """
    # Initialize the frontier with (start, depth=0)
    frontier = deque()
    frontier.append((start, 0))
    
    # Dictionary to track where each node came from
    came_from = {start: None}
    
    # Set to track visited nodes for visualization
    visited = set()
    visited.add(start)
    
    # DLS main loop
    while frontier:
        current, depth = frontier.pop()  # Pop from the end to simulate DFS behavior
        
        # Visualize current state
        if visualizer:
            visualizer.draw_grid(
                path=None,
                start=start,
                goal=goal,
                visited=visited,
                current=current,
                frontier=[node for (node, _) in frontier]
            )
            visualizer.delay(delay)
        
        # Check if we reached the goal
        if current == goal:
            break
        
        # Explore neighbors only if within depth limit
        if depth < depth_limit:
            for next_node in grid.get_neighbors(current):
                if next_node not in came_from:
                    frontier.append((next_node, depth + 1))
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


def reconstruct_bidirectional(came_f, came_b, meeting_point):
    """
    Helper function to reconstruct the path found by bidirectional search.
    
    Args:
        came_f: Dictionary of parents from forward search
        came_b: Dictionary of parents from backward search
        meeting_point: The node where forward and backward searches met
    
    Returns:
        path: List of tuples representing the complete path from start to goal
    """
    # Build path from start to meeting point
    path_f = []
    current = meeting_point
    while current is not None:
        path_f.append(current)
        current = came_f[current]
    path_f.reverse()
    
    # Build path from meeting point to goal
    path_b = []
    current = came_b[meeting_point]  # Start from parent of meeting point in backward search
    while current is not None:
        path_b.append(current)
        current = came_b[current]
    
    # Combine paths
    return path_f + path_b


def bidirectional_search(grid, start, goal, visualizer=None, delay=50):
    """
    Bidirectional Search algorithm that searches from both start and goal simultaneously.
    
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
    # Two frontiers
    frontier_f = deque([start])  # Forward
    frontier_b = deque([goal])   # Backward
    
    # Two "came_from" dictionaries
    came_f = {start: None}
    came_b = {goal: None}
    
    while frontier_f and frontier_b:
        # 1. Expand Forward
        if frontier_f:
            current_f = frontier_f.popleft()
            
            # Check if forward search meets backward search
            if current_f in came_b:
                path = reconstruct_bidirectional(came_f, came_b, current_f)
                visited = set(came_f.keys()) | set(came_b.keys())
                return path, visited
            
            # Explore neighbors in forward direction
            for next_node in grid.get_neighbors(current_f):
                if next_node not in came_f:
                    came_f[next_node] = current_f
                    frontier_f.append(next_node)
        
        # 2. Expand Backward
        if frontier_b:
            current_b = frontier_b.popleft()
            
            # Check if backward search meets forward search
            if current_b in came_f:
                path = reconstruct_bidirectional(came_f, came_b, current_b)
                visited = set(came_f.keys()) | set(came_b.keys())
                return path, visited
            
            # Explore neighbors in backward direction
            for next_node in grid.get_neighbors(current_b):
                if next_node not in came_b:
                    came_b[next_node] = current_b
                    frontier_b.append(next_node)
        
        # 3. Visualization
        if visualizer:
            visualizer.draw_grid(
                path=None,
                start=start,
                goal=goal,
                visited=set(came_f.keys()) | set(came_b.keys()),
                current=current_f if frontier_f else current_b,
                frontier=list(frontier_f) + list(frontier_b)
            )
            visualizer.delay(delay)
    
    return [], set()