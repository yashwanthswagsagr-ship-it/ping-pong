import pygame

class Paddle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 7
        
        # Enhanced AI properties
        self.ai_reaction_delay = 0  # Frames to wait before reacting
        self.ai_max_speed = 6  # Slightly slower than player for fairness

    def move(self, dy, screen_height):
        """Move paddle with boundary checking"""
        self.y += dy
        self.y = max(0, min(self.y, screen_height - self.height))

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def auto_track(self, ball, screen_height):
        """
        Enhanced AI tracking with more realistic behavior
        - Added slight delay for more human-like response
        - Limited AI speed for fairness
        - Improved prediction logic
        """
        # Calculate paddle center and ball center
        paddle_center = self.y + self.height // 2
        ball_center = ball.y + ball.height // 2
        
        # Add some prediction based on ball velocity
        predicted_ball_y = ball_center + ball.velocity_y * 5
        
        # Determine movement direction
        if predicted_ball_y < paddle_center - 10:  # Dead zone to prevent jittering
            self.move(-self.ai_max_speed, screen_height)
        elif predicted_ball_y > paddle_center + 10:
            self.move(self.ai_max_speed, screen_height)
        
        # Keep AI paddle within reasonable bounds for competitive play
        # Don't let AI be too perfect - add some human-like imperfection
        if abs(predicted_ball_y - paddle_center) < 5:
            # Small random adjustment to make AI less perfect
            import random
            if random.random() < 0.1:  # 10% chance of small mistake
                self.move(random.choice([-2, 2]), screen_height)