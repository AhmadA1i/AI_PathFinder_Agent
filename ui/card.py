import pygame


class CardPanel:
    def __init__(self, rect, title, title_font, subtitle_font, bg_color, border_color, radius=12, padding=20):
        self.rect = pygame.Rect(rect)
        self.title = title
        self.title_font = title_font
        self.subtitle_font = subtitle_font
        self.bg_color = bg_color
        self.border_color = border_color
        self.radius = radius
        self.padding = padding

    def update_rect(self, rect):
        self.rect = pygame.Rect(rect)

    def inner_rect(self):
        return pygame.Rect(
            self.rect.x + self.padding,
            self.rect.y + self.padding,
            self.rect.width - self.padding * 2,
            self.rect.height - self.padding * 2,
        )

    def draw(self, surface):
        pygame.draw.rect(surface, self.bg_color, self.rect, border_radius=self.radius)
        pygame.draw.rect(surface, self.border_color, self.rect, width=1, border_radius=self.radius)

        title_surf = self.title_font.render(self.title, True, (229, 231, 235))
        surface.blit(title_surf, (self.rect.x + self.padding, self.rect.y + 12))
