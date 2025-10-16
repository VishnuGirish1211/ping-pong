import pygame
from .paddle import Paddle
from .ball import Ball

# Game Engine

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

        self.winning_score = 5


    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        self.ball.move(self.player, self.ai)


        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.ball.reset()

        self.ai.auto_track(self.ball, self.height)

    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

    

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))


    def check_game_over(self, screen):
     winner_text = None
 
     if self.player_score >= self.winning_score:
         winner_text = "Player Wins!"
     elif self.ai_score >= self.winning_score:
         winner_text = "AI Wins!"
 
     if winner_text:
         # Display the winner
         text = self.font.render(winner_text, True, (255, 255, 255))
         screen.blit(text, (self.width // 2 - text.get_width() // 2, self.height // 2 - 80))
         
         # Display replay options
         options = [
             "Press 3 for Best of 3",
             "Press 5 for Best of 5",
             "Press 7 for Best of 7",
             "Press ESC to Exit"
         ]
 
         for i, option in enumerate(options):
             opt_text = self.font.render(option, True, (200, 200, 200))
             screen.blit(opt_text, (self.width // 2 - opt_text.get_width() // 2, self.height // 2 + i * 40))
         
         pygame.display.flip()
 
         # Wait for player input
         waiting = True
         while waiting:
             for event in pygame.event.get():
                 if event.type == pygame.QUIT:
                     pygame.quit()
                     return True
                 elif event.type == pygame.KEYDOWN:
                     if event.key == pygame.K_ESCAPE:
                         pygame.quit()
                         return True
                     elif event.key == pygame.K_3:
                         self.winning_score = 2  # Best of 3 means first to 2
                         waiting = False
                     elif event.key == pygame.K_5:
                         self.winning_score = 3  # Best of 5 means first to 3
                         waiting = False
                     elif event.key == pygame.K_7:
                         self.winning_score = 4  # Best of 7 means first to 4
                         waiting = False
 
             pygame.time.wait(100)
 
         # Reset everything for a new game
         self.player_score = 0
         self.ai_score = 0
         self.ball.reset()
 
         # Return False so main loop continues
         return False
 
     return False
 