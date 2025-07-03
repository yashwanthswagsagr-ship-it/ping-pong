import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])
        
        # TASK 1: Add collision flags to prevent multiple collisions per frame
        self.last_collision_time = 0
        self.collision_cooldown = 100  # milliseconds

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Wall collision (top and bottom)
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            # Keep ball within bounds to prevent sticking
            if self.y <= 0:
                self.y = 0
            else:
                self.y = self.screen_height - self.height

    def check_collision(self, player, ai):
        """
        TASK 1: Enhanced collision detection with improved accuracy
        - Added collision cooldown to prevent multiple hits per frame
        - Added position-based collision handling for better physics
        - Improved collision response based on where the ball hits the paddle
        """
        current_time = pygame.time.get_ticks()
        
        # Check if enough time has passed since last collision
        if current_time - self.last_collision_time < self.collision_cooldown:
            return False
        
        ball_rect = self.rect()
        player_rect = player.rect()
        ai_rect = ai.rect()
        
        # Check collision with player paddle (left side)
        if ball_rect.colliderect(player_rect) and self.velocity_x < 0:
            self.last_collision_time = current_time
            self.velocity_x = abs(self.velocity_x)  # Ensure ball goes right
            
            # Add spin based on where ball hits paddle
            hit_pos = (self.y + self.height/2) - (player.y + player.height/2)
            self.velocity_y += hit_pos * 0.1  # Add some spin
            
            # Keep ball outside paddle to prevent sticking
            self.x = player_rect.right
            return True
            
        # Check collision with AI paddle (right side)
        elif ball_rect.colliderect(ai_rect) and self.velocity_x > 0:
            self.last_collision_time = current_time
            self.velocity_x = -abs(self.velocity_x)  # Ensure ball goes left
            
            # Add spin based on where ball hits paddle
            hit_pos = (self.y + self.height/2) - (ai.y + ai.height/2)
            self.velocity_y += hit_pos * 0.1  # Add some spin
            
            # Keep ball outside paddle to prevent sticking
            self.x = ai_rect.left - self.width
            return True
            
        return False

    def reset(self):
        """Reset ball to center with random direction"""
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])
        self.last_collision_time = 0

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)