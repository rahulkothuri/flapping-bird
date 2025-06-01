import pygame
import sys
import random
import os
from pygame.locals import *

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 900
GRAVITY = 0.25
FLAP_POWER = -5
PIPE_SPEED = 3
PIPE_GAP = 150
PIPE_FREQUENCY = 1500  # milliseconds
FLOOR_HEIGHT = 100
GAME_SPEED = 60  # FPS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)
GREEN = (0, 128, 0)
RED = (255, 0, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flapping Bird')
clock = pygame.time.Clock()

# Load assets
def load_image(name):
    """Load an image and return the image object"""
    try:
        image = pygame.image.load(os.path.join('assets', 'images', name))
        return image
    except pygame.error:
        print(f"Cannot load image: {name}")
        return pygame.Surface((50, 50))

def load_sound(name):
    """Load a sound and return the sound object"""
    try:
        sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', name))
        return sound
    except pygame.error:
        print(f"Cannot load sound: {name}")
        return None

# Bird class
class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0
        self.animation_count = 0
        self.image = load_image('bird.png')
        self.rect = self.image.get_rect(center=(x, y))
        self.flap_sound = load_sound('flap.wav')
        
    def flap(self):
        self.velocity = FLAP_POWER
        if self.flap_sound:
            self.flap_sound.play()
    
    def update(self):
        # Apply gravity
        self.velocity += GRAVITY
        self.y += self.velocity
        
        # Update rectangle position
        self.rect.centery = self.y
        
        # Keep bird on screen
        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity = 0
            
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
    def get_mask(self):
        return pygame.mask.from_surface(self.image)

# Pipe class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = 0
        self.gap_pos = random.randint(150, SCREEN_HEIGHT - 150 - FLOOR_HEIGHT)
        
        self.top_pipe = load_image('pipe_top.png')
        self.bottom_pipe = load_image('pipe_bottom.png')
        
        # Scale pipes if needed
        pipe_width = 80
        top_height = self.gap_pos - PIPE_GAP // 2
        bottom_height = SCREEN_HEIGHT - self.gap_pos - PIPE_GAP // 2 - FLOOR_HEIGHT
        
        # Create rectangles for collision detection
        self.top_rect = pygame.Rect(x, 0, pipe_width, top_height)
        self.bottom_rect = pygame.Rect(x, self.gap_pos + PIPE_GAP // 2, pipe_width, bottom_height)
        
        self.passed = False
        
    def update(self):
        self.x -= PIPE_SPEED
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x
        
    def draw(self, surface):
        # Draw top pipe
        pygame.draw.rect(surface, GREEN, self.top_rect)
        
        # Draw bottom pipe
        pygame.draw.rect(surface, GREEN, self.bottom_rect)
        
    def collide(self, bird):
        bird_mask = bird.get_mask()
        
        # Check if bird collides with either pipe
        if bird.rect.colliderect(self.top_rect) or bird.rect.colliderect(self.bottom_rect):
            return True
            
        return False

# Game class
class Game:
    def __init__(self):
        self.bird = Bird(100, SCREEN_HEIGHT // 2)
        self.pipes = []
        self.score = 0
        self.font = pygame.font.SysFont('Arial', 32)
        self.last_pipe = pygame.time.get_ticks()
        self.running = True
        self.game_over = False
        self.point_sound = load_sound('point.wav')
        self.hit_sound = load_sound('hit.wav')
        
        # Try to load background music
        try:
            pygame.mixer.music.load(os.path.join('assets', 'sounds', 'background.wav'))
            pygame.mixer.music.play(-1)  # Loop indefinitely
        except:
            print("Could not load background music")
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE and not self.game_over:
                    self.bird.flap()
                if event.key == K_SPACE and self.game_over:
                    self.reset()
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
    
    def update(self):
        if not self.game_over:
            self.bird.update()
            
            # Generate new pipes
            time_now = pygame.time.get_ticks()
            if time_now - self.last_pipe > PIPE_FREQUENCY:
                self.pipes.append(Pipe(SCREEN_WIDTH))
                self.last_pipe = time_now
            
            # Update pipes and check for score
            for pipe in self.pipes:
                pipe.update()
                
                # Check if bird has passed the pipe
                if not pipe.passed and pipe.x < self.bird.x:
                    pipe.passed = True
                    self.score += 1
                    if self.point_sound:
                        self.point_sound.play()
            
            # Remove pipes that have gone off screen
            self.pipes = [pipe for pipe in self.pipes if pipe.x > -100]
            
            # Check for collisions
            for pipe in self.pipes:
                if pipe.collide(self.bird):
                    if self.hit_sound:
                        self.hit_sound.play()
                    self.game_over = True
            
            # Check if bird has hit the ground or gone off the top
            if self.bird.rect.bottom >= SCREEN_HEIGHT - FLOOR_HEIGHT or self.bird.rect.top <= 0:
                if self.hit_sound:
                    self.hit_sound.play()
                self.game_over = True
    
    def draw(self):
        # Draw sky background
        screen.fill(SKY_BLUE)
        
        # Draw pipes
        for pipe in self.pipes:
            pipe.draw(screen)
        
        # Draw floor
        pygame.draw.rect(screen, GREEN, (0, SCREEN_HEIGHT - FLOOR_HEIGHT, SCREEN_WIDTH, FLOOR_HEIGHT))
        
        # Draw bird
        self.bird.draw(screen)
        
        # Draw score
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # Draw game over screen
        if self.game_over:
            game_over_text = self.font.render('GAME OVER', True, RED)
            restart_text = self.font.render('Press SPACE to restart', True, WHITE)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
                                        SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 
                                      SCREEN_HEIGHT // 2 + 50))
        
        pygame.display.update()
    
    def reset(self):
        self.bird = Bird(100, SCREEN_HEIGHT // 2)
        self.pipes = []
        self.score = 0
        self.last_pipe = pygame.time.get_ticks()
        self.game_over = False
        
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(GAME_SPEED)

# Main function
def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
