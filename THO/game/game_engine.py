import pygame
from .paddle import Paddle
from .ball import Ball

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100
        
        # Game objects
        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        # Score tracking
        self.player_score = 0
        self.ai_score = 0
        
        # TASK 2: Game state management
        self.game_state = "PLAYING"  # PLAYING, GAME_OVER, MENU
        self.winning_score = 5  # Default winning score
        self.winner = None
        
        # TASK 3: Replay system
        self.match_options = [3, 5, 7]  # Best of options
        self.current_match_option = 1  # Index for 5 (best of 5)
        self.games_to_win = (self.match_options[self.current_match_option] + 1) // 2  # 3 for best of 5
        
        # Fonts for different purposes
        self.font = pygame.font.SysFont("Arial", 30)
        self.big_font = pygame.font.SysFont("Arial", 48)
        self.small_font = pygame.font.SysFont("Arial", 20)
        
        # TASK 4: Sound system initialization
        self.sounds_enabled = True
        self.sounds = {}
        self.load_sounds()

    def load_sounds(self):
        """
        TASK 4: Load sound effects
        Note: In a real implementation, you would load actual sound files
        For this example, we'll create placeholder sounds using pygame's sound generation
        """
        try:
            # Create simple sound effects using pygame
            # In a real game, you would load .wav or .ogg files
            pygame.mixer.init()
            
            # Generate simple tones (placeholder - replace with actual sound files)
            self.sounds['paddle_hit'] = self.create_tone(440, 0.1)  # A note, 0.1 second
            self.sounds['wall_bounce'] = self.create_tone(330, 0.1)  # E note
            self.sounds['score'] = self.create_tone(550, 0.3)  # Higher pitch, longer
            
        except pygame.error:
            print("Sound system not available")
            self.sounds_enabled = False

    def create_tone(self, frequency, duration):
        """Generate a simple tone for sound effects"""
        try:
            sample_rate = 22050
            frames = int(duration * sample_rate)
            arr = []
            for i in range(frames):
                wave = 4096 * 0.3 * (i // (sample_rate // frequency) % 2 - 0.5)
                arr.append([wave, wave])
            sound = pygame.sndarray.make_sound(pygame.array.array('i', arr))
            return sound
        except:
            return None

    def play_sound(self, sound_name):
        """Play a sound effect if sounds are enabled"""
        if self.sounds_enabled and sound_name in self.sounds and self.sounds[sound_name]:
            try:
                self.sounds[sound_name].play()
            except:
                pass  # Ignore sound errors

    def handle_input(self):
        """Handle player input based on current game state"""
        keys = pygame.key.get_pressed()
        
        if self.game_state == "PLAYING":
            # Game controls
            if keys[pygame.K_w]:
                self.player.move(-10, self.height)
            if keys[pygame.K_s]:
                self.player.move(10, self.height)
                
        elif self.game_state == "GAME_OVER":
            # TASK 3: Replay controls
            if keys[pygame.K_r]:
                self.restart_game()
            elif keys[pygame.K_UP]:
                self.current_match_option = (self.current_match_option - 1) % len(self.match_options)
                self.games_to_win = (self.match_options[self.current_match_option] + 1) // 2
            elif keys[pygame.K_DOWN]:
                self.current_match_option = (self.current_match_option + 1) % len(self.match_options)
                self.games_to_win = (self.match_options[self.current_match_option] + 1) // 2
            elif keys[pygame.K_RETURN]:
                self.restart_game()

    def update(self):
        """Update game logic based on current state"""
        if self.game_state != "PLAYING":
            return
            
        # Move ball and check wall collisions
        old_y = self.ball.y
        self.ball.move()
        
        # TASK 4: Play wall bounce sound
        if (self.ball.y <= 0 or self.ball.y + self.ball.height >= self.height) and old_y != self.ball.y:
            self.play_sound('wall_bounce')
        
        # Check paddle collisions
        if self.ball.check_collision(self.player, self.ai):
            # TASK 4: Play paddle hit sound
            self.play_sound('paddle_hit')

        # Check for scoring
        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
            self.play_sound('score')  # TASK 4: Play score sound
            self.check_game_over()  # TASK 2: Check if game should end
            
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.ball.reset()
            self.play_sound('score')  # TASK 4: Play score sound
            self.check_game_over()  # TASK 2: Check if game should end

        # Update AI
        self.ai.auto_track(self.ball, self.height)

    def check_game_over(self):
        """
        TASK 2: Check if game should end based on winning score
        """
        if self.player_score >= self.games_to_win:
            self.game_state = "GAME_OVER"
            self.winner = "Player"
        elif self.ai_score >= self.games_to_win:
            self.game_state = "GAME_OVER"
            self.winner = "AI"

    def restart_game(self):
        """
        TASK 3: Restart the game with current settings
        """
        self.player_score = 0
        self.ai_score = 0
        self.game_state = "PLAYING"
        self.winner = None
        self.ball.reset()
        
        # Reset paddle positions
        self.player.y = self.height // 2 - 50
        self.ai.y = self.height // 2 - 50

    def render(self, screen):
        """Render the game based on current state"""
        if self.game_state == "PLAYING":
            self.render_game(screen)
        elif self.game_state == "GAME_OVER":
            self.render_game_over(screen)

    def render_game(self, screen):
        """Render the main game screen"""
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        
        # Draw center line
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))
        
        # Draw match info
        match_text = self.small_font.render(f"Best of {self.match_options[self.current_match_option]}", True, WHITE)
        screen.blit(match_text, (10, self.height - 30))

    def render_game_over(self, screen):
        """
        TASK 2 & 3: Render game over screen with replay options
        """
        # Draw semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # Draw winner text
        winner_color = GREEN if self.winner == "Player" else RED
        winner_text = self.big_font.render(f"{self.winner} Wins!", True, winner_color)
        winner_rect = winner_text.get_rect(center=(self.width//2, self.height//3))
        screen.blit(winner_text, winner_rect)
        
        # Draw final score
        score_text = self.font.render(f"Final Score: {self.player_score} - {self.ai_score}", True, WHITE)
        score_rect = score_text.get_rect(center=(self.width//2, self.height//2))
        screen.blit(score_text, score_rect)
        
        # Draw replay options
        options_y = self.height//2 + 60
        
        # Best of options
        options_text = self.font.render("Choose Match Length:", True, WHITE)
        options_rect = options_text.get_rect(center=(self.width//2, options_y))
        screen.blit(options_text, options_rect)
        
        for i, option in enumerate(self.match_options):
            color = GREEN if i == self.current_match_option else WHITE
            option_text = self.small_font.render(f"Best of {option}", True, color)
            option_rect = option_text.get_rect(center=(self.width//2, options_y + 40 + i * 25))
            screen.blit(option_text, option_rect)
        
        # Controls
        controls_y = options_y + 140
        controls = [
            "↑/↓ - Change match length",
            "ENTER or R - Play Again",
            "ESC - Exit"
        ]
        
        for i, control in enumerate(controls):
            control_text = self.small_font.render(control, True, WHITE)
            control_rect = control_text.get_rect(center=(self.width//2, controls_y + i * 25))
            screen.blit(control_text, control_rect)