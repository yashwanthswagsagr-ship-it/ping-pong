import pygame
import os
from .paddle import Paddle
from .ball import Ball

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)

        # ---- SOUND INITIALIZATION ----
        try:
            pygame.mixer.init()
            self.hit_sound = pygame.mixer.Sound(os.path.join("assets", "hit.wav"))
            self.wall_sound = pygame.mixer.Sound(os.path.join("assets", "wall.wav"))
            self.score_sound = pygame.mixer.Sound(os.path.join("assets", "score.wav"))
        except Exception as e:
            print("⚠ Sound files missing or not loaded properly:", e)
            self.hit_sound = self.wall_sound = self.score_sound = None
        # --------------------------------

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        self.ball.move()
        self.ball.check_collision(self.player, self.ai)

        # Scoring logic
        if self.ball.x <= 0:
            self.ai_score += 1
            score_sound.play()
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            score_sound.play()
            self.ball.reset()

    # AI tracking
        self.ai.auto_track(self.ball, self.height)

    # 🏁 Game over condition
        if self.player_score >= 5 or self.ai_score >= 5:
            self.show_game_over_screen()

    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width // 2, 0), (self.width // 2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width // 4, 20))
        screen.blit(ai_text, (self.width * 3 // 4, 20))

    def show_game_over_screen(self):
        winner = "Player" if self.player_score > self.ai_score else "AI"
        text = self.font.render(f"{winner} Wins!", True, (255, 255, 255))
        pygame.display.get_surface().blit(text, (self.width // 2 - 100, self.height // 2))
        pygame.display.flip()
        pygame.time.delay(3000)
        pygame.quit()
        exit()


pygame.mixer.init()
hit_sound = pygame.mixer.Sound("assets/paddle_hit.wav")
wall_sound = pygame.mixer.Sound("assets/wall_bounce.wav")
score_sound = pygame.mixer.Sound("assets/score.wav")