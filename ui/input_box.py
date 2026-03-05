import pygame


class InputBox:
    def __init__(
        self,
        rect,
        text,
        font,
        text_color,
        bg_color,
        border_color,
        focus_border,
        radius=8,
        numeric_only=True,
    ):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.border_color = border_color
        self.focus_border = focus_border
        self.radius = radius
        self.numeric_only = numeric_only
        self.active = False
        self.cursor_visible = True
        self.cursor_timer = 0
        self.cursor_interval_ms = 450

    def update_rect(self, rect):
        self.rect = pygame.Rect(rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.rect.collidepoint(event.pos)

        if not self.active or event.type != pygame.KEYDOWN:
            return False

        if event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
            return True

        if event.key in (pygame.K_RETURN, pygame.K_TAB):
            return False

        char = event.unicode
        if not char:
            return False

        if self.numeric_only and not char.isdigit():
            return False

        self.text += char
        return True

    def update(self, dt_ms):
        if not self.active:
            self.cursor_visible = False
            self.cursor_timer = 0
            return

        self.cursor_timer += dt_ms
        if self.cursor_timer >= self.cursor_interval_ms:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0

    def draw(self, surface):
        border = self.focus_border if self.active else self.border_color
        pygame.draw.rect(surface, self.bg_color, self.rect, border_radius=self.radius)
        pygame.draw.rect(surface, border, self.rect, width=2 if self.active else 1, border_radius=self.radius)

        display_text = self.text if self.text else ""
        rendered = self.font.render(display_text, True, self.text_color)
        text_x = self.rect.x + 10
        text_y = self.rect.centery - rendered.get_height() // 2
        surface.blit(rendered, (text_x, text_y))

        if self.active and self.cursor_visible:
            cursor_x = text_x + rendered.get_width() + 2
            top = self.rect.y + 9
            bottom = self.rect.bottom - 9
            pygame.draw.line(surface, self.text_color, (cursor_x, top), (cursor_x, bottom), 2)
