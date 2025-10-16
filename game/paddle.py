import pygame

class Paddle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 7

    def move(self, dy, screen_height):
        self.y += dy
        self.y = max(0, min(self.y, screen_height - self.height))

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def auto_track(self, ball, screen_height):
    # Small delay factor — AI doesn't move every frame
        reaction_delay = 10  # higher = slower AI reaction
        if pygame.time.get_ticks() % reaction_delay == 0:
        # Follow the ball with a limited tracking ability
            target_y = ball.y - (self.height // 2)
            if self.y + self.height / 2 < target_y:
                self.move(self.speed - 2, screen_height)
            elif self.y + self.height / 2 > target_y:
                self.move(-self.speed + 2, screen_height)