# grid.py

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = set()

    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def is_passable(self, id):
        return id not in self.walls

    def get_neighbors(self, id):
        (x, y) = id
        # Strict Clockwise Order: Up, Right, Bottom, Bottom-Right, Left, Top-Left
        # Note: Directions adjusted based on your updated instructions
        results = [
            (x, y - 1),  # Up
            (x + 1, y),  # Right
            (x + 1, y + 1), # Bottom-Right
            (x, y + 1),  # Bottom
            (x - 1, y),  # Left
            (x - 1, y - 1)  # Top-Left
        ]
        
        # Filter results that are within grid and not blocked
        results = filter(self.in_bounds, results)
        results = filter(self.is_passable, results)
        return results