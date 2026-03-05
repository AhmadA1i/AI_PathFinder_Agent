import pygame


class Legend:
    def __init__(self, items, text_font, text_color, background_color):
        self.items = items
        self.text_font = text_font
        self.text_color = text_color
        self.background_color = background_color

    def draw(self, surface, rect):
        pygame.draw.rect(surface, self.background_color, rect)

        x = rect.x + 16
        y = rect.y + (rect.height - 18) // 2

        for label, color in self.items:
            swatch = pygame.Rect(x, y, 18, 18)
            pygame.draw.rect(surface, color, swatch, border_radius=4)
            pygame.draw.rect(surface, (71, 85, 105), swatch, width=1, border_radius=4)
            x += 24

            text = self.text_font.render(label, True, self.text_color)
            surface.blit(text, (x, rect.y + (rect.height - text.get_height()) // 2))
            x += text.get_width() + 18
