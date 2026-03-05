import pygame
import random
from grid import Grid
from algorithms import bfs_search, dfs_search, ucs_search, dls_search, bidirectional_search
from ui.layout import UIManager
from ui.button import Button
from ui.slider import Slider
from ui.toolbar import Toolbar
from ui.legend import Legend

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

# Modern dark visualization palette
APP_BG = (15, 23, 42)
TOP_BAR_BG = (17, 24, 39)
GRID_CELL_BG = (30, 41, 59)
GRID_LINE = (51, 65, 85)
TEXT_PRIMARY = (229, 231, 235)
TEXT_SECONDARY = (156, 163, 175)
BUTTON_BG = (59, 130, 246)
BUTTON_HOVER = (37, 99, 235)
SLIDER_TRACK = (55, 65, 81)
SLIDER_FILL = (59, 130, 246)
SLIDER_KNOB = (255, 255, 255)


def add_demo_walls(grid, start, goal):
    """Create a deterministic obstacle pattern that adapts to grid size."""
    walls = set()

    # Central cross
    cx = grid.width // 2
    cy = grid.height // 2
    for x in range(max(1, cx - max(2, grid.width // 6)), min(grid.width - 1, cx + max(2, grid.width // 6))):
        walls.add((x, cy))
    for y in range(max(1, cy - max(2, grid.height // 6)), min(grid.height - 1, cy + max(2, grid.height // 6))):
        walls.add((cx, y))

    # Upper-left pocket
    ul_x = max(1, grid.width // 8)
    ul_y = max(1, grid.height // 6)
    for x in range(ul_x, min(grid.width - 2, ul_x + max(2, grid.width // 5))):
        walls.add((x, ul_y))
    for y in range(ul_y, min(grid.height - 2, ul_y + max(2, grid.height // 6))):
        walls.add((ul_x, y))

    # Bottom-right corridor
    br_x = max(2, grid.width - max(3, grid.width // 5))
    br_y = max(2, grid.height - max(3, grid.height // 5))
    for y in range(br_y, grid.height - 1):
        walls.add((br_x, y))
    for x in range(max(1, br_x - max(2, grid.width // 8)), br_x + 1):
        walls.add((x, grid.height - 2))

    # Keep start and goal open
    if start in walls:
        walls.remove(start)
    if goal in walls:
        walls.remove(goal)

    grid.walls = walls


def run_iddfs(grid, start, goal, visualizer=None, delay=50):
    """Run iterative deepening DFS and return path/visited/depth_found."""
    path, visited = dls_search(grid, start, goal, 0, visualizer, delay=delay)
    visited_total = set(visited)

    if path:
        return path, visited_total, 0

    for depth_limit in range(1, grid.width + grid.height):
        path, visited = dls_search(grid, start, goal, depth_limit, visualizer, delay=delay)
        visited_total.update(visited)
        if path:
            return path, visited_total, depth_limit

    return [], visited_total, None


def build_info_lines(choice, grid, start, goal, status=None, path=None, visited=None, depth_limit=None, iddfs_depth_found=None, post_run=False):
    """Build side-panel lines with only details relevant to the chosen algorithm."""
    lines = [
        f"Algorithm: {choice.upper()}",
        f"Grid: {grid.width} x {grid.height}",
        f"Start: {start}",
        f"Goal: {goal}",
    ]

    if choice == "dls":
        lines.append(f"Depth Limit: {depth_limit}")
    elif choice == "iddfs" and iddfs_depth_found is not None:
        lines.append(f"IDDFS Found At: {iddfs_depth_found}")

    if status is not None:
        lines.append(f"Status: {status}")

    if path is not None and visited is not None:
        lines.extend([
            f"Path Steps: {len(path)}",
            f"Visited Nodes: {len(visited)}",
        ])

    lines.extend([
        "Esc = Exit",
        "Window = Resizable",
    ])

    if post_run:
        lines.extend([
            "R = Reset / Rerun",
            "N = New Setup",
        ])
    return lines


class VisualizerInterrupt(Exception):
    """Raised when user requests reset/new setup/exit during algorithm animation."""

    def __init__(self, action):
        super().__init__(action)
        self.action = action


class GridVisualizer:
    def __init__(self, grid, cell_size=40, window_width=1200, window_height=750):
        self.grid = grid
        self.base_cell_size = cell_size
        self.padding = 14
        self.cell_padding = 2
        self.min_window_width = 920
        self.min_window_height = 620
        self.width = max(window_width, self.min_window_width)
        self.height = max(window_height, self.min_window_height)
        self.info_lines = []
        self.speed_min = 0.5
        self.speed_max = 5.0
        self.speed_multiplier = 1.0
        self.algorithm_label = "-"
        self.status_label = "Ready"
        self.post_run_mode = False
        self.paused = False
        self.step_once = False
        self.pending_action = None
        self.top_bar_height = 52
        self.control_height = 64
        self.legend_height = 52
        self.buttons = {}
        self.last_frame = {
            "path": None,
            "start": None,
            "goal": None,
            "visited": None,
            "current": None,
            "frontier": None,
        }

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption("AI PathFinder")
        self.clock = pygame.time.Clock()
        self.title_font = pygame.font.SysFont("Segoe UI", 24, bold=True)
        self.info_font = pygame.font.SysFont("Segoe UI", 20)
        self.small_font = pygame.font.SysFont("Segoe UI", 18)

        self.toolbar = Toolbar(
            self.top_bar_height,
            TOP_BAR_BG,
            TEXT_PRIMARY,
            TEXT_SECONDARY,
            self.title_font,
            self.info_font,
        )
        self.legend = Legend(
            [
                ("Start", GREEN),
                ("Goal", RED),
                ("Path", YELLOW),
                ("Visited", LIGHT_BLUE),
                ("Frontier", PURPLE),
                ("Wall", TOP_BAR_BG),
            ],
            self.small_font,
            TEXT_PRIMARY,
            TOP_BAR_BG,
        )

        self.buttons["run"] = Button((0, 0, 120, 40), "Run", self.small_font, BUTTON_BG, WHITE, hover_color=BUTTON_HOVER, radius=10)
        self.buttons["reset"] = Button((0, 0, 120, 40), "Reset", self.small_font, BUTTON_BG, WHITE, hover_color=BUTTON_HOVER, radius=10)
        self.buttons["setup"] = Button((0, 0, 140, 40), "New Setup", self.small_font, BUTTON_BG, WHITE, hover_color=BUTTON_HOVER, radius=10)
        self.speed_slider = Slider((0, 0, 220, 20), self.speed_min, self.speed_max, self.speed_multiplier, SLIDER_TRACK, SLIDER_FILL, SLIDER_KNOB)

    def set_info_lines(self, lines):
        self.info_lines = lines or []

        self.post_run_mode = any(line.startswith("Path Steps:") for line in self.info_lines)
        for line in self.info_lines:
            if line.startswith("Algorithm:"):
                self.algorithm_label = line.split(":", 1)[1].strip()
            if line.startswith("Status:"):
                self.status_label = line.split(":", 1)[1].strip()

    def _update_layout(self):
        top_h = self.top_bar_height
        control_h = self.control_height
        legend_h = self.legend_height

        self.grid_area = pygame.Rect(
            self.padding,
            top_h + self.padding,
            self.width - self.padding * 2,
            self.height - top_h - control_h - legend_h - self.padding * 3,
        )
        self.control_area = pygame.Rect(0, self.grid_area.bottom + self.padding, self.width, control_h)
        self.legend_area = pygame.Rect(0, self.control_area.bottom, self.width, legend_h)

        btn_w = 108
        btn_h = 40
        btn_y = self.control_area.y + (control_h - btn_h) // 2
        x = 16
        self.buttons["run"].update_rect((x, btn_y, btn_w, btn_h))
        x += btn_w + 12
        self.buttons["reset"].update_rect((x, btn_y, btn_w, btn_h))
        x += btn_w + 12
        self.buttons["setup"].update_rect((x, btn_y, 140, btn_h))

        slider_w = min(260, max(140, self.width // 4))
        slider_x = self.width - slider_w - 24
        slider_y = self.control_area.y + (control_h // 2) + 8
        self.speed_slider.update_rect((slider_x, slider_y, slider_w, 18))

    def _handle_visual_event(self, event):
        """Handle common visualizer interactions for both animation and post-run phases."""
        if event.type == pygame.QUIT:
            self.pending_action = "exit"
            return self.pending_action

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.pending_action = "exit"
                return self.pending_action
            if event.key == pygame.K_SPACE:
                self.paused = not self.paused
            if event.key == pygame.K_RIGHT and self.paused:
                self.step_once = True
            if event.key in (pygame.K_PLUS, pygame.K_EQUALS):
                self.speed_multiplier = min(self.speed_multiplier + 0.25, self.speed_max)
            if event.key == pygame.K_MINUS:
                self.speed_multiplier = max(self.speed_multiplier - 0.25, self.speed_min)
            if event.key == pygame.K_r:
                self.pending_action = "rerun"
            if event.key == pygame.K_n:
                self.pending_action = "reconfigure"

        if event.type == pygame.VIDEORESIZE:
            self.width = max(event.w, self.min_window_width)
            self.height = max(event.h, self.min_window_height)
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)

        if self.speed_slider.handle_event(event):
            self.speed_multiplier = self.speed_slider.value

        if self.buttons["run"].handle_event(event):
            if self.post_run_mode:
                self.pending_action = "rerun"
            else:
                self.paused = not self.paused

        if self.buttons["reset"].handle_event(event):
            self.pending_action = "rerun"

        if self.buttons["setup"].handle_event(event):
            self.pending_action = "reconfigure"

        return self.pending_action

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
        # Reuse the most recent frame values when arguments are omitted.
        if path is None and self.last_frame["path"] is not None:
            path = self.last_frame["path"]
        if start is None and self.last_frame["start"] is not None:
            start = self.last_frame["start"]
        if goal is None and self.last_frame["goal"] is not None:
            goal = self.last_frame["goal"]
        if visited is None and self.last_frame["visited"] is not None:
            visited = self.last_frame["visited"]
        if current is None and self.last_frame["current"] is not None:
            current = self.last_frame["current"]
        if frontier is None and self.last_frame["frontier"] is not None:
            frontier = self.last_frame["frontier"]

        self.last_frame = {
            "path": path,
            "start": start,
            "goal": goal,
            "visited": visited,
            "current": current,
            "frontier": frontier,
        }

        self._update_layout()
        self.screen.fill(APP_BG)

        self.toolbar.draw(self.screen, self.width, "AI PathFinder", self.algorithm_label, self.speed_multiplier)

        # Center grid within available grid area.
        self.cell_size = max(
            8,
            min(
                self.grid_area.width // self.grid.width,
                self.grid_area.height // self.grid.height,
            ),
        )
        grid_w = self.grid.width * self.cell_size
        grid_h = self.grid.height * self.cell_size
        offset_x = self.grid_area.x + (self.grid_area.width - grid_w) // 2
        offset_y = self.grid_area.y + (self.grid_area.height - grid_h) // 2

        def cell_rect(x, y):
            return pygame.Rect(offset_x + x * self.cell_size, offset_y + y * self.cell_size, self.cell_size, self.cell_size)

        # Draw base cells first.
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                rect = cell_rect(x, y)
                inner = rect.inflate(-self.cell_padding * 2, -self.cell_padding * 2)
                pygame.draw.rect(self.screen, GRID_CELL_BG, inner, border_radius=4)

        def draw_cells(cells, color):
            if not cells:
                return
            for x, y in cells:
                rect = cell_rect(x, y)
                inner = rect.inflate(-self.cell_padding * 2, -self.cell_padding * 2)
                pygame.draw.rect(self.screen, color, inner, border_radius=4)

        draw_cells(visited, LIGHT_BLUE)
        draw_cells(frontier, PURPLE)
        draw_cells(path, YELLOW)
        draw_cells(self.grid.walls, TOP_BAR_BG)

        if current:
            draw_cells([current], ORANGE)
        if start:
            draw_cells([start], GREEN)
        if goal:
            draw_cells([goal], RED)

        # Subtle grid lines.
        for x in range(self.grid.width + 1):
            px = offset_x + x * self.cell_size
            pygame.draw.line(self.screen, GRID_LINE, (px, offset_y), (px, offset_y + grid_h), 1)
        for y in range(self.grid.height + 1):
            py = offset_y + y * self.cell_size
            pygame.draw.line(self.screen, GRID_LINE, (offset_x, py), (offset_x + grid_w, py), 1)

        # Control panel.
        pygame.draw.rect(self.screen, TOP_BAR_BG, self.control_area)
        for button in self.buttons.values():
            button.draw(self.screen)

        speed_text = self.small_font.render(f"Speed: {self.speed_multiplier:.2f}x", True, TEXT_PRIMARY)
        self.screen.blit(speed_text, (self.speed_slider.rect.x, self.control_area.y + 6))
        self.speed_slider.draw(self.screen)

        status = "Paused" if self.paused else self.status_label
        status_text = self.small_font.render(status, True, TEXT_SECONDARY)
        self.screen.blit(status_text, (self.buttons["setup"].rect.right + 18, self.control_area.y + (self.control_area.height - status_text.get_height()) // 2))

        # Legend.
        self.legend.draw(self.screen, self.legend_area)
        
        pygame.display.flip()
    
    def delay(self, milliseconds):
        """Delay for visualization"""
        adjusted_delay = int(milliseconds / max(self.speed_multiplier, 0.01))
        elapsed = 0
        step = 10

        # Keep visualizer responsive during algorithm animation.
        while elapsed < adjusted_delay:
            for event in pygame.event.get():
                action = self._handle_visual_event(event)
                if action in ("exit", "rerun", "reconfigure"):
                    raise VisualizerInterrupt(action)

            while self.paused and not self.step_once:
                self.draw_grid()
                for event in pygame.event.get():
                    action = self._handle_visual_event(event)
                    if action in ("exit", "rerun", "reconfigure"):
                        raise VisualizerInterrupt(action)
                self.clock.tick(60)

            if self.step_once:
                self.step_once = False
                self.paused = True
                break

            chunk = min(step, adjusted_delay - elapsed)
            pygame.time.delay(chunk)
            elapsed += chunk
    
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
            for event in pygame.event.get():
                action = self._handle_visual_event(event)
                if action == "exit":
                    return "exit"
                if action == "rerun":
                    self.pending_action = None
                    return "rerun"
                if action == "reconfigure":
                    self.pending_action = None
                    return "reconfigure"

            self.draw_grid(path, start, goal, visited)
            self.clock.tick(fps)

        return "exit"


def get_user_config_via_pygame(initial_width=980, initial_height=600, initial_config=None):
    """Collect configuration from user via the modular Pygame dashboard UI."""
    ui = UIManager(initial_width, initial_height)
    return ui.run(initial_config=initial_config)


def run_search_with_config(config):
    """Run one search session using a config and return visualizer + result context."""
    grid = Grid(config["grid_width"], config["grid_height"])
    start = config["start"]
    goal = config["goal"]
    add_demo_walls(grid, start, goal)

    choice = config["algorithm"]
    depth_limit = config["depth_limit"]

    if choice == "ucs":
        for x in range(grid.width):
            for y in range(grid.height):
                if (x, y) not in grid.walls:
                    grid.weights[(x, y)] = random.randint(1, 10)
    else:
        grid.weights = {}

    visualizer = GridVisualizer(grid, cell_size=42, window_width=1120, window_height=720)
    visualizer.set_info_lines(
        build_info_lines(
            choice,
            grid,
            start,
            goal,
            status="Running...",
            depth_limit=depth_limit,
            iddfs_depth_found=None,
            post_run=False,
        )
    )

    iddfs_depth_found = None
    interrupt_action = None
    try:
        if choice == "bfs":
            path, visited = bfs_search(grid, start, goal, visualizer, delay=80)
        elif choice == "dfs":
            path, visited = dfs_search(grid, start, goal, visualizer, delay=80)
        elif choice == "ucs":
            path, visited = ucs_search(grid, start, goal, visualizer, delay=80)
        elif choice == "dls":
            path, visited = dls_search(grid, start, goal, depth_limit, visualizer, delay=80)
        elif choice == "iddfs":
            path, visited, iddfs_depth_found = run_iddfs(grid, start, goal, visualizer, delay=45)
        elif choice == "bidirectional":
            path, visited = bidirectional_search(grid, start, goal, visualizer, delay=70)
        else:
            path, visited = [], set()
    except VisualizerInterrupt as interrupt:
        interrupt_action = interrupt.action
        path, visited = [], set()

    status = "Path Found" if path else "No Path Found"
    visualizer.set_info_lines(
        build_info_lines(
            choice,
            grid,
            start,
            goal,
            status=status,
            path=path,
            visited=visited,
            depth_limit=depth_limit,
            iddfs_depth_found=iddfs_depth_found,
            post_run=True,
        )
    )

    if interrupt_action is None:
        print(f"Algorithm: {choice.upper()}")
        print(f"Grid: {grid.width} x {grid.height}")
        print(f"Path steps: {len(path)}")
        print(f"Visited nodes: {len(visited)}")

    return visualizer, path, visited, start, goal, interrupt_action


def main():
    config = get_user_config_via_pygame()
    if config is None:
        pygame.quit()
        return

    while True:
        visualizer, path, visited, start, goal, interrupt_action = run_search_with_config(config)

        if interrupt_action == "exit":
            pygame.quit()
            return
        if interrupt_action == "rerun":
            continue
        if interrupt_action == "reconfigure":
            new_config = get_user_config_via_pygame(initial_config=config)
            if new_config is None:
                pygame.quit()
                return
            config = new_config
            continue

        # Keep result visible and allow in-app next action
        action = visualizer.run(path=path, start=start, goal=goal, visited=visited)

        if action == "exit":
            pygame.quit()
            return
        if action == "rerun":
            continue
        if action == "reconfigure":
            new_config = get_user_config_via_pygame(initial_config=config)
            if new_config is None:
                pygame.quit()
                return
            config = new_config
            continue


if __name__ == "__main__":
    main()
