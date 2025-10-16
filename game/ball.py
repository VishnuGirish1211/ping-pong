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
        self.sound_paddle = pygame.mixer.Sound("assets/paddle_hit.wav")
        self.sound_wall = pygame.mixer.Sound("assets/wall_bounce.wav")
        self.sound_score = pygame.mixer.Sound("assets/score.wav")


    def move(self, player, ai):
        """Move the ball and handle collisions with paddles and walls."""
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Bounce off top/bottom walls
        if self.y <= 0:
            self.y = 0
            self.velocity_y *= -1
            self.sound_wall.play()
        elif self.y + self.height >= self.screen_height:
            self.y = self.screen_height - self.height
            self.velocity_y *= -1
            self.sound_wall.play()

        # Paddle collision (player)
        ball_rect = self.rect()
        if ball_rect.colliderect(player.rect()):
            self.x = player.x + player.width  # prevent sticking
            self.velocity_x = abs(self.velocity_x)
            self.sound_paddle.play()

        # Paddle collision (AI)
        elif ball_rect.colliderect(ai.rect()):
            self.x = ai.x - self.width  # prevent sticking
            self.velocity_x = -abs(self.velocity_x)
            self.sound_paddle.play()


    def reset(self):
        """Reset ball to center and play scoring sound."""
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])
        self.sound_score.play()
       
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
