import pygame
import sys
from game.game_engine import GameEngine

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Enhanced Edition")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Game loop
engine = GameEngine(WIDTH, HEIGHT)

def main():
    """
    Enhanced main game loop with proper exit handling
    Changes made:
    - Added ESC key handling for graceful exit
    - Added proper game state management
    - Added frame rate display option
    """
    running = True
    show_fps = False  # Toggle with F key
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_f:
                    show_fps = not show_fps
        
        # Clear screen
        SCREEN.fill(BLACK)
        
        # Update game logic
        engine.handle_input()
        engine.update()
        
        # Render game
        engine.render(SCREEN)
        
        # Show FPS if enabled (helpful for debugging)
        if show_fps:
            fps_text = pygame.font.SysFont("Arial", 16).render(f"FPS: {int(clock.get_fps())}", True, WHITE)
            SCREEN.blit(fps_text, (10, 10))
        
        # Update display
        pygame.display.flip()
        clock.tick(FPS)

    # Cleanup
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()