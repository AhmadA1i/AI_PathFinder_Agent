import pygame


class Toolbar:
    def __init__(self, height, bg_color, text_color, secondary_color, title_font, info_font):
        self.height = height
        self.bg_color = bg_color
        self.text_color = text_color
        self.secondary_color = secondary_color
        self.title_font = title_font
        self.info_font = info_font

    def draw(self, surface, width, title, algorithm_label, speed_multiplier):
        rect = pygame.Rect(0, 0, width, self.height)
        pygame.draw.rect(surface, self.bg_color, rect)

        title_surface = self.title_font.render(title, True, self.text_color)
        surface.blit(title_surface, (16, (self.height - title_surface.get_height()) // 2))

        right_text = f"Algorithm: {algorithm_label.upper()}   Speed: {speed_multiplier:.2f}x"
        info_surface = self.info_font.render(right_text, True, self.secondary_color)
        surface.blit(info_surface, (width - info_surface.get_width() - 16, (self.height - info_surface.get_height()) // 2))
