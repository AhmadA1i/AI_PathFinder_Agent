import pygame


class Button:
    def __init__(
        self,
        rect,
        text,
        font,
        bg_color,
        text_color,
        border_color=None,
        hover_color=None,
        radius=10,
    ):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color
        self.border_color = border_color
        self.hover_color = hover_color or bg_color
        self.radius = radius
        self.is_hovered = False

    def update_rect(self, rect):
        self.rect = pygame.Rect(rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.bg_color
        pygame.draw.rect(surface, color, self.rect, border_radius=self.radius)
        if self.border_color:
            pygame.draw.rect(surface, self.border_color, self.rect, width=1, border_radius=self.radius)

        label = self.font.render(self.text, True, self.text_color)
        label_rect = label.get_rect(center=self.rect.center)
        surface.blit(label, label_rect)


class ToggleButton(Button):
    def __init__(
        self,
        rect,
        text,
        font,
        bg_color,
        text_color,
        selected_bg,
        selected_text,
        border_color=None,
        hover_color=None,
        radius=12,
    ):
        super().__init__(
            rect,
            text,
            font,
            bg_color,
            text_color,
            border_color=border_color,
            hover_color=hover_color,
            radius=radius,
        )
        self.selected_bg = selected_bg
        self.selected_text = selected_text
        self.selected = False

    def draw(self, surface):
        if self.selected:
            bg = self.selected_bg
            text_color = self.selected_text
        else:
            bg = self.hover_color if self.is_hovered else self.bg_color
            text_color = self.text_color

        pygame.draw.rect(surface, bg, self.rect, border_radius=self.radius)
        if self.border_color and not self.selected:
            pygame.draw.rect(surface, self.border_color, self.rect, width=1, border_radius=self.radius)

        label = self.font.render(self.text, True, text_color)
        label_rect = label.get_rect(center=self.rect.center)
        surface.blit(label, label_rect)
