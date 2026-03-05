import pygame


class Slider:
    def __init__(
        self,
        rect,
        min_value,
        max_value,
        value,
        track_color,
        fill_color,
        knob_color,
    ):
        self.rect = pygame.Rect(rect)
        self.min_value = float(min_value)
        self.max_value = float(max_value)
        self.value = float(value)
        self.track_color = track_color
        self.fill_color = fill_color
        self.knob_color = knob_color
        self.dragging = False

    def update_rect(self, rect):
        self.rect = pygame.Rect(rect)

    def _value_from_x(self, x):
        if self.rect.width <= 0:
            return self.value
        clamped_x = max(self.rect.left, min(x, self.rect.right))
        ratio = (clamped_x - self.rect.left) / self.rect.width
        return self.min_value + ratio * (self.max_value - self.min_value)

    def _x_from_value(self):
        if self.max_value == self.min_value:
            return self.rect.left
        ratio = (self.value - self.min_value) / (self.max_value - self.min_value)
        return int(self.rect.left + ratio * self.rect.width)

    def handle_event(self, event):
        changed = False

        knob_x = self._x_from_value()
        knob_rect = pygame.Rect(knob_x - 8, self.rect.centery - 8, 16, 16)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if knob_rect.collidepoint(event.pos) or self.rect.collidepoint(event.pos):
                self.dragging = True
                self.value = self._value_from_x(event.pos[0])
                changed = True

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False

        if event.type == pygame.MOUSEMOTION and self.dragging:
            self.value = self._value_from_x(event.pos[0])
            changed = True

        return changed

    def draw(self, surface):
        track_rect = pygame.Rect(self.rect.x, self.rect.centery - 3, self.rect.width, 6)
        pygame.draw.rect(surface, self.track_color, track_rect, border_radius=3)

        if self.max_value != self.min_value:
            ratio = (self.value - self.min_value) / (self.max_value - self.min_value)
        else:
            ratio = 0
        fill_w = int(track_rect.width * ratio)
        fill_rect = pygame.Rect(track_rect.x, track_rect.y, fill_w, track_rect.height)
        pygame.draw.rect(surface, self.fill_color, fill_rect, border_radius=3)

        knob_x = self._x_from_value()
        pygame.draw.circle(surface, self.knob_color, (knob_x, track_rect.centery), 8)
