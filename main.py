import pygame
import sys, random
from grid import Grid
from algorithms import bfs_search, dfs_search, ucs_search, dls_search, bidirectional_search

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (173, 216, 230)
ORANGE = (255, 165, 0)
PURPLE = (147, 112, 219)

class GridVisualizer:
    def __init__(self, grid, cell_size=40):
        self.grid = grid
        self.cell_size = cell_size
        self.width = grid.width * cell_size
        self.height = grid.height * cell_size
        
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("AI PathFinder")
        self.clock = pygame.time.Clock()
        
    def draw_grid(self, path=None, start=None, goal=None, visited=None, current=None, frontier=None):
        """
        Generic function to draw the grid with optional path, start, goal, and visited nodes
        
        Args:
            path: List of tuples representing the path
            start: Tuple (x, y) representing start position
            goal: Tuple (x, y) representing goal position
            visited: Set of tuples representing visited nodes
            current: Tuple (x, y) representing currently exploring node
            frontier: List of tuples representing nodes in frontier
        """
        self.screen.fill(WHITE)
        
        # Draw visited nodes first (if any)
        if visited:
            for (x, y) in visited:
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, 
                                   self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, LIGHT_BLUE, rect)  # Light blue
        
        # Draw frontier nodes (if any)
        if frontier:
            for (x, y) in frontier:
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, 
                                   self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, PURPLE, rect)  # Purple for frontier
        
        # Draw path (if any)
        if path:
            for (x, y) in path:
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, 
                                   self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, YELLOW, rect)
        
        # Draw walls
        for (x, y) in self.grid.walls:
            rect = pygame.Rect(x * self.cell_size, y * self.cell_size, 
                               self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, BLACK, rect)
        
        
        # Draw current node being explored (if any)
        if current:
            x, y = current
            rect = pygame.Rect(x * self.cell_size, y * self.cell_size, 
                               self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, ORANGE, rect)  # Orange for current
        
        # Draw start position
        if start:
            x, y = start
            rect = pygame.Rect(x * self.cell_size, y * self.cell_size, 
                               self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, GREEN, rect)
        
        # Draw goal position
        if goal:
            x, y = goal
            rect = pygame.Rect(x * self.cell_size, y * self.cell_size, 
                               self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, RED, rect)
        
        # Draw grid lines
        for x in range(self.grid.width + 1):
            pygame.draw.line(self.screen, GRAY, 
                           (x * self.cell_size, 0), 
                           (x * self.cell_size, self.height), 1)
        
        for y in range(self.grid.height + 1):
            pygame.draw.line(self.screen, GRAY, 
                           (0, y * self.cell_size), 
                           (self.width, y * self.cell_size), 1)
        
        pygame.display.flip()
    
    def delay(self, milliseconds):
        """Delay for visualization"""
        pygame.time.delay(milliseconds)
        # Process events during delay to keep window responsive
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
        return True
    
    def run(self, path=None, start=None, goal=None, visited=None, fps=60):
        """
        Main loop to display the grid
        
        Args:
            path: List of tuples representing the path
            start: Tuple (x, y) representing start position
            goal: Tuple (x, y) representing goal position
            visited: Set of tuples representing visited nodes
            fps: Frames per second
        """
        running = True
        while running:
            running = self.handle_events()
            self.draw_grid(path, start, goal, visited)
            self.clock.tick(fps)
        
        pygame.quit()
        sys.exit()


def main():
    # Create a sample grid
    grid = Grid(20, 15)
    
    # Add some walls
    for x in range(5, 15):
        grid.walls.add((x, 7))
    
    for y in range(3, 10):
        grid.walls.add((10, y))
    
    # Define start and goal
    start = (2, 2)
    goal = (19, 14)

    choice = input("Enter algorithm (bfs, dfs, ucs, dls, iddfs, bidirectional): ").lower()
    
    # Validate choice
    valid_choices = ['bfs', 'dfs', 'ucs', 'dls', 'iddfs', 'bidirectional']
    if choice not in valid_choices:
        print("Invalid choice! Please enter one of: bfs, dfs, ucs, dls, iddfs, bidirectional")
        return
    
    # Add random weights ONLY if UCS is chosen
    if choice == "ucs":
        print("Generating random weights for UCS...")
        for x in range(grid.width):
            for y in range(grid.height):
                if (x, y) not in grid.walls:
                    grid.weights[(x, y)] = random.randint(1, 10)
    else:
        # For other algorithms, ensure all weights are 1 (default)
        grid.weights = {}
    
    # Create visualizer
    visualizer = GridVisualizer(grid, cell_size=40)
    
    # Run selected algorithm
    print(f"Running {choice.upper()} algorithm...")
    
    if choice == "bfs":
        path, visited = bfs_search(grid, start, goal, visualizer, delay=100)
    elif choice == "dfs":
        path, visited = dfs_search(grid, start, goal, visualizer, delay=100)
    elif choice == "ucs":
        path, visited = ucs_search(grid, start, goal, visualizer, delay=100)
    elif choice == "dls":
        depth_limit = int(input("Enter depth limit (default 10): ") or "10")
        path, visited = dls_search(grid, start, goal, depth_limit, visualizer, delay=100)
    elif choice == "iddfs":
        path, visited = dls_search(grid, start, goal, 0, visualizer, delay=50)
        visited_total = set(visited)
        for depth_limit in range(1, grid.width + grid.height):
            path, visited = dls_search(grid, start, goal, depth_limit, visualizer, delay=50)
            visited_total.update(visited)
            if path:
                print(f"Path found at depth limit {depth_limit}")
                visited = visited_total
                break
    elif choice == "bidirectional":
        path, visited = bidirectional_search(grid, start, goal, visualizer, delay=100)
    
    # Display final result
    print(f"Path found with {len(path)} steps")
    print(f"Visited {len(visited)} nodes")
    if path:
        print(f"Path: {path[:5]}{'...' if len(path) > 5 else ''}")
    
    # Show final path
    visualizer.run(path=path, start=start, goal=goal, visited=visited)


if __name__ == "__main__":
    main()
