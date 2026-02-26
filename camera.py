import pygame
#camera.py



class Camera:
    def __init__(self, screen_size, world_size):
        self.offset = pygame.Vector2(0, 0)
        self.screen_width, self.screen_height = screen_size
        self.world_width, self.world_height = world_size

    def follow(self, target_rect, mouse_bias=True, bias_strength=0.04):
        # Base target is player center
        target_x = target_rect.centerx
        target_y = target_rect.centery

        if mouse_bias:
            mx, my = pygame.mouse.get_pos()
            screen_center = pygame.Vector2(self.screen_width // 2, self.screen_height // 2)
            mouse_pos = pygame.Vector2(mx, my)
            bias = (mouse_pos - screen_center) * bias_strength

            # Apply mouse bias to target position
            target_x += bias.x
            target_y += bias.y

        # Calculate offset to center camera on biased target
        self.offset.x = target_x - self.screen_width // 2
        self.offset.y = target_y - self.screen_height // 2

        # Clamp offset to world bounds
        self.offset.x = max(0, min(self.offset.x, self.world_width - self.screen_width))
        self.offset.y = max(0, min(self.offset.y, self.world_height - self.screen_height))

    def apply(self, rect):
        return rect.move(-self.offset.x, -self.offset.y)

    def apply_pos(self, pos):
        return (pos[0] - self.offset.x, pos[1] - self.offset.y)
    def reverse(self, pos):
        return (pos[0] + self.offset.x, pos[1] + self.offset.y)


