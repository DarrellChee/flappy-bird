import pygame
import random

# Game constants
WIDTH, HEIGHT = 400, 600
FPS = 60
GRAVITY = 0.5
JUMP_VELOCITY = -10
PIPE_SPEED = 3
PIPE_GAP = 150
PIPE_DISTANCE = 300

class Bird:
    def __init__(self):
        self.x = WIDTH // 4
        self.y = HEIGHT // 2
        self.velocity = 0
        self.width = 34
        self.height = 24
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        self.rect.y = int(self.y)

    def jump(self):
        self.velocity = JUMP_VELOCITY

    def draw(self, surface):
        self.rect.x = self.x
        pygame.draw.rect(surface, (255, 255, 255), self.rect)

class Pipe:
    def __init__(self, x):
        self.x = x
        self.width = 52
        self.top = random.randint(50, HEIGHT - PIPE_GAP - 50)
        self.bottom = self.top + PIPE_GAP
        self.passed = False

    def update(self):
        self.x -= PIPE_SPEED

    def draw(self, surface):
        top_rect = pygame.Rect(self.x, 0, self.width, self.top)
        bottom_rect = pygame.Rect(self.x, self.bottom, self.width, HEIGHT - self.bottom)
        pygame.draw.rect(surface, (0, 255, 0), top_rect)
        pygame.draw.rect(surface, (0, 255, 0), bottom_rect)

    def collide(self, bird_rect):
        top_rect = pygame.Rect(self.x, 0, self.width, self.top)
        bottom_rect = pygame.Rect(self.x, self.bottom, self.width, HEIGHT - self.bottom)
        return bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect)

def main():
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 32)

    bird = Bird()
    pipes = [Pipe(WIDTH + 100)]
    score = 0
    running = True

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    bird.jump()

        bird.update()
        add_pipe = False
        for pipe in list(pipes):
            pipe.update()
            if pipe.collide(bird.rect):
                running = False
            if pipe.x + pipe.width < 0:
                pipes.remove(pipe)
            if not pipe.passed and pipe.x + pipe.width < bird.x:
                pipe.passed = True
                add_pipe = True
        if add_pipe:
            score += 1
            pipes.append(Pipe(pipes[-1].x + PIPE_DISTANCE))
        if bird.y + bird.height >= HEIGHT or bird.y <= 0:
            running = False

        window.fill((0, 0, 0))
        for pipe in pipes:
            pipe.draw(window)
        bird.draw(window)
        score_text = font.render(str(score), True, (255, 255, 255))
        window.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
