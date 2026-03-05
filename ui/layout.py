import pygame

from config import COLORS, MIN_HEIGHT, MIN_WIDTH, SPACING, WINDOW_HEIGHT, WINDOW_WIDTH
from ui.button import Button, ToggleButton
from ui.card import CardPanel
from ui.input_box import InputBox


class UIManager:
    def __init__(self, width=WINDOW_WIDTH, height=WINDOW_HEIGHT):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption("AI PathFinder")
        self.clock = pygame.time.Clock()

        self.title_font = pygame.font.SysFont("Segoe UI", 36, bold=True)
        self.subtitle_font = pygame.font.SysFont("Segoe UI", 20)
        self.section_font = pygame.font.SysFont("Segoe UI", 22, bold=True)
        self.label_font = pygame.font.SysFont("Segoe UI", 17)
        self.button_font = pygame.font.SysFont("Segoe UI", 18, bold=True)

        self.algorithms = ["bfs", "dfs", "ucs", "dls", "iddfs", "bidirectional"]
        self.selected_algo_idx = 0
        self.error_text = ""

        self.fields = {}
        self.algo_buttons = []
        self.start_button = None
        self.exit_button = None
        self.grid_card = None
        self.algo_card = None

    def _build_default_values(self, initial_config=None):
        defaults = {
            "width": "20",
            "height": "15",
            "start_x": "1",
            "start_y": "1",
            "goal_x": "19",
            "goal_y": "14",
            "depth": "10",
        }

        if not initial_config:
            return defaults

        defaults["width"] = str(initial_config.get("grid_width", defaults["width"]))
        defaults["height"] = str(initial_config.get("grid_height", defaults["height"]))

        start = initial_config.get("start", (1, 1))
        goal = initial_config.get("goal", (19, 14))
        defaults["start_x"] = str(start[0])
        defaults["start_y"] = str(start[1])
        defaults["goal_x"] = str(goal[0])
        defaults["goal_y"] = str(goal[1])

        if initial_config.get("depth_limit") is not None:
            defaults["depth"] = str(initial_config.get("depth_limit"))

        if initial_config.get("algorithm") in self.algorithms:
            self.selected_algo_idx = self.algorithms.index(initial_config.get("algorithm"))

        return defaults

    def _build_layout(self):
        self.width = max(self.screen.get_width(), MIN_WIDTH)
        self.height = max(self.screen.get_height(), MIN_HEIGHT)
        if (self.width, self.height) != self.screen.get_size():
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)

        container_w = min(980, self.width - 40)
        container_h = min(640, self.height - 36)
        container_x = (self.width - container_w) // 2
        container_y = (self.height - container_h) // 2

        content_top = container_y + 108
        cards_h = container_h - 220
        card_gap = SPACING["card_gap"]
        card_w = (container_w - card_gap) // 2

        grid_rect = pygame.Rect(container_x, content_top, card_w, cards_h)
        algo_rect = pygame.Rect(container_x + card_w + card_gap, content_top, card_w, cards_h)

        self.grid_card = CardPanel(
            grid_rect,
            "Grid Settings",
            self.section_font,
            self.label_font,
            COLORS["card_bg"],
            COLORS["card_border"],
            radius=12,
            padding=SPACING["card_padding"],
        )
        self.algo_card = CardPanel(
            algo_rect,
            "Algorithm Selection",
            self.section_font,
            self.label_font,
            COLORS["card_bg"],
            COLORS["card_border"],
            radius=12,
            padding=SPACING["card_padding"],
        )

        start_rect = pygame.Rect(container_x + container_w // 2 - 180, container_y + container_h - 64, 170, 46)
        exit_rect = pygame.Rect(container_x + container_w // 2 + 10, container_y + container_h - 64, 170, 46)

        if self.start_button is None:
            self.start_button = Button(
                start_rect,
                "Start Search",
                self.button_font,
                COLORS["start_bg"],
                (255, 255, 255),
                hover_color=COLORS["start_hover"],
                radius=10,
            )
            self.exit_button = Button(
                exit_rect,
                "Exit",
                self.button_font,
                COLORS["exit_bg"],
                (255, 255, 255),
                hover_color=COLORS["exit_hover"],
                radius=10,
            )
        else:
            self.start_button.update_rect(start_rect)
            self.exit_button.update_rect(exit_rect)

        self._layout_grid_fields()
        self._layout_algo_buttons()

        return {
            "container": pygame.Rect(container_x, container_y, container_w, container_h),
        }

    def _ensure_input(self, key, rect, text):
        if key not in self.fields:
            self.fields[key] = InputBox(
                rect,
                text,
                self.label_font,
                COLORS["text_primary"],
                COLORS["input_bg"],
                COLORS["input_border"],
                COLORS["input_focus"],
                radius=8,
                numeric_only=True,
            )
        else:
            self.fields[key].update_rect(rect)

    def _layout_grid_fields(self):
        inner = self.grid_card.inner_rect()
        left = inner.x
        top = inner.y + 42
        field_h = 40
        gap = SPACING["field"]

        label_col_w = 145
        full_w = inner.width - label_col_w - 10
        half_w = (full_w - 10) // 2

        y = top
        self._ensure_input("width", pygame.Rect(left + label_col_w, y, full_w, field_h), self.fields["width"].text if "width" in self.fields else "20")
        y += field_h + gap
        self._ensure_input("height", pygame.Rect(left + label_col_w, y, full_w, field_h), self.fields["height"].text if "height" in self.fields else "15")

        y += field_h + gap + 6
        self._ensure_input("start_x", pygame.Rect(left + label_col_w, y, half_w, field_h), self.fields["start_x"].text if "start_x" in self.fields else "1")
        self._ensure_input("start_y", pygame.Rect(left + label_col_w + half_w + 10, y, half_w, field_h), self.fields["start_y"].text if "start_y" in self.fields else "1")

        y += field_h + gap
        self._ensure_input("goal_x", pygame.Rect(left + label_col_w, y, half_w, field_h), self.fields["goal_x"].text if "goal_x" in self.fields else "19")
        self._ensure_input("goal_y", pygame.Rect(left + label_col_w + half_w + 10, y, half_w, field_h), self.fields["goal_y"].text if "goal_y" in self.fields else "14")

        y += field_h + gap
        self._ensure_input("depth", pygame.Rect(left + label_col_w, y, full_w, field_h), self.fields["depth"].text if "depth" in self.fields else "10")

    def _layout_algo_buttons(self):
        inner = self.algo_card.inner_rect()
        top = inner.y + 52
        btn_w = (inner.width - 14) // 2
        btn_h = 44
        col_gap = 14
        row_gap = 12

        new_buttons = []
        for i, algo in enumerate(self.algorithms):
            row = i // 2
            col = i % 2
            rect = pygame.Rect(
                inner.x + col * (btn_w + col_gap),
                top + row * (btn_h + row_gap),
                btn_w,
                btn_h,
            )
            if i < len(self.algo_buttons):
                btn = self.algo_buttons[i]
                btn.update_rect(rect)
            else:
                btn = ToggleButton(
                    rect,
                    algo.upper(),
                    self.button_font,
                    COLORS["button_bg"],
                    COLORS["text_primary"],
                    COLORS["button_selected"],
                    COLORS["button_selected_text"],
                    border_color=COLORS["button_border"],
                    hover_color=COLORS["button_hover"],
                    radius=12,
                )
            btn.selected = (i == self.selected_algo_idx)
            new_buttons.append(btn)
        self.algo_buttons = new_buttons

    def _validate(self):
        try:
            grid_w = int(self.fields["width"].text)
            grid_h = int(self.fields["height"].text)
            sx = int(self.fields["start_x"].text)
            sy = int(self.fields["start_y"].text)
            gx = int(self.fields["goal_x"].text)
            gy = int(self.fields["goal_y"].text)
            depth_text = self.fields["depth"].text or "0"
            depth = int(depth_text)

            if grid_w < 8 or grid_w > 80 or grid_h < 8 or grid_h > 60:
                self.error_text = "Grid width: 8-80, height: 8-60"
                return None

            if not (0 <= sx < grid_w and 0 <= sy < grid_h):
                self.error_text = "Start must be within grid bounds"
                return None

            if not (0 <= gx < grid_w and 0 <= gy < grid_h):
                self.error_text = "Goal must be within grid bounds"
                return None

            if (sx, sy) == (gx, gy):
                self.error_text = "Start and goal cannot be the same"
                return None

            if depth < 0:
                self.error_text = "Depth limit must be >= 0"
                return None

            algo = self.algorithms[self.selected_algo_idx]
            self.error_text = ""
            return {
                "grid_width": grid_w,
                "grid_height": grid_h,
                "start": (sx, sy),
                "goal": (gx, gy),
                "algorithm": algo,
                "depth_limit": depth if algo == "dls" else None,
            }
        except ValueError:
            self.error_text = "Please enter valid numeric values"
            return None

    def _draw_title_block(self, container):
        title = self.title_font.render("AI PathFinder", True, COLORS["text_primary"])
        subtitle = self.subtitle_font.render("Configure grid and search algorithm", True, COLORS["text_secondary"])

        title_rect = title.get_rect(centerx=container.centerx, top=container.y + 8)
        subtitle_rect = subtitle.get_rect(centerx=container.centerx, top=title_rect.bottom + 8)

        self.screen.blit(title, title_rect)
        self.screen.blit(subtitle, subtitle_rect)

    def _draw_grid_content(self):
        inner = self.grid_card.inner_rect()
        x = inner.x
        y = inner.y + 54
        gap = SPACING["field"]
        label_color = COLORS["text_secondary"]

        self.screen.blit(self.label_font.render("Width", True, label_color), (x, y + 10))
        y += 40 + gap
        self.screen.blit(self.label_font.render("Height", True, label_color), (x, y + 10))

        y += 40 + gap + 6
        self.screen.blit(self.label_font.render("Start (X, Y)", True, label_color), (x, y + 10))
        y += 40 + gap
        self.screen.blit(self.label_font.render("Goal (X, Y)", True, label_color), (x, y + 10))
        y += 40 + gap

        depth_label = "DLS Depth" if self.algorithms[self.selected_algo_idx] == "dls" else "DLS Depth (optional)"
        self.screen.blit(self.label_font.render(depth_label, True, label_color), (x, y + 10))

        for field in self.fields.values():
            field.draw(self.screen)

    def _draw_algo_content(self):
        for button in self.algo_buttons:
            button.draw(self.screen)

        inner = self.algo_card.inner_rect()
        preview = pygame.Rect(inner.x, inner.y + 210, inner.width, inner.height - 220)
        pygame.draw.rect(self.screen, (34, 34, 34), preview, border_radius=10)
        pygame.draw.rect(self.screen, (58, 58, 58), preview, width=1, border_radius=10)

        title = self.label_font.render("Live Preview", True, COLORS["text_secondary"])
        self.screen.blit(title, (preview.x + 12, preview.y + 10))

        try:
            gw = max(1, int(self.fields["width"].text or "1"))
            gh = max(1, int(self.fields["height"].text or "1"))
            sx = int(self.fields["start_x"].text or "0")
            sy = int(self.fields["start_y"].text or "0")
            gx = int(self.fields["goal_x"].text or "0")
            gy = int(self.fields["goal_y"].text or "0")
        except ValueError:
            return

        grid_area = pygame.Rect(preview.x + 12, preview.y + 36, preview.width - 24, preview.height - 48)
        if grid_area.width <= 0 or grid_area.height <= 0:
            return

        cell = max(3, min(grid_area.width // gw, grid_area.height // gh))
        px = grid_area.x + (grid_area.width - gw * cell) // 2
        py = grid_area.y + (grid_area.height - gh * cell) // 2

        for ix in range(gw):
            for iy in range(gh):
                rect = pygame.Rect(px + ix * cell, py + iy * cell, cell, cell)
                pygame.draw.rect(self.screen, (58, 58, 58), rect, width=1)

        if 0 <= sx < gw and 0 <= sy < gh:
            pygame.draw.rect(self.screen, (34, 197, 94), pygame.Rect(px + sx * cell, py + sy * cell, cell, cell))
        if 0 <= gx < gw and 0 <= gy < gh:
            pygame.draw.rect(self.screen, (239, 68, 68), pygame.Rect(px + gx * cell, py + gy * cell, cell, cell))

    def run(self, initial_config=None):
        defaults = self._build_default_values(initial_config)
        self.fields = {
            "width": InputBox((0, 0, 0, 0), defaults["width"], self.label_font, COLORS["text_primary"], COLORS["input_bg"], COLORS["input_border"], COLORS["input_focus"]),
            "height": InputBox((0, 0, 0, 0), defaults["height"], self.label_font, COLORS["text_primary"], COLORS["input_bg"], COLORS["input_border"], COLORS["input_focus"]),
            "start_x": InputBox((0, 0, 0, 0), defaults["start_x"], self.label_font, COLORS["text_primary"], COLORS["input_bg"], COLORS["input_border"], COLORS["input_focus"]),
            "start_y": InputBox((0, 0, 0, 0), defaults["start_y"], self.label_font, COLORS["text_primary"], COLORS["input_bg"], COLORS["input_border"], COLORS["input_focus"]),
            "goal_x": InputBox((0, 0, 0, 0), defaults["goal_x"], self.label_font, COLORS["text_primary"], COLORS["input_bg"], COLORS["input_border"], COLORS["input_focus"]),
            "goal_y": InputBox((0, 0, 0, 0), defaults["goal_y"], self.label_font, COLORS["text_primary"], COLORS["input_bg"], COLORS["input_border"], COLORS["input_focus"]),
            "depth": InputBox((0, 0, 0, 0), defaults["depth"], self.label_font, COLORS["text_primary"], COLORS["input_bg"], COLORS["input_border"], COLORS["input_focus"]),
        }

        while True:
            dt = self.clock.tick(60)
            layout = self._build_layout()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return None
                    if event.key == pygame.K_LEFT:
                        self.selected_algo_idx = (self.selected_algo_idx - 1) % len(self.algorithms)
                    elif event.key == pygame.K_RIGHT:
                        self.selected_algo_idx = (self.selected_algo_idx + 1) % len(self.algorithms)
                    elif event.key == pygame.K_RETURN:
                        result = self._validate()
                        if result:
                            return result

                for idx, btn in enumerate(self.algo_buttons):
                    if btn.handle_event(event):
                        self.selected_algo_idx = idx

                if self.start_button and self.start_button.handle_event(event):
                    result = self._validate()
                    if result:
                        return result

                if self.exit_button and self.exit_button.handle_event(event):
                    return None

                for field in self.fields.values():
                    field.handle_event(event)

                if event.type == pygame.VIDEORESIZE:
                    w = max(event.w, MIN_WIDTH)
                    h = max(event.h, MIN_HEIGHT)
                    self.screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)

            for field in self.fields.values():
                field.update(dt)

            self.screen.fill(COLORS["bg"])
            self._draw_title_block(layout["container"])
            self.grid_card.draw(self.screen)
            self.algo_card.draw(self.screen)
            self._draw_grid_content()
            self._draw_algo_content()

            self.start_button.draw(self.screen)
            self.exit_button.draw(self.screen)

            if self.error_text:
                error = self.label_font.render(self.error_text, True, COLORS["error"])
                self.screen.blit(error, (layout["container"].x, layout["container"].bottom - 88))

            pygame.display.flip()
