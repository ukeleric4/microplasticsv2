import pygame
import random
import time

# Initialize pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FISH_WIDTH = 60
FISH_HEIGHT = 60
PLASTIC_WIDTH = 80
PLASTIC_HEIGHT = 80
NORMAL_SPEED = 3
ACCELERATED_SPEED = NORMAL_SPEED * 2
TIME_LIMIT = 30  # 30 seconds time limit

# Font
font = pygame.font.SysFont(None, 55)

# Other variables
game_over_boolean = False

# Load images
fish_img = pygame.image.load('fish.png')
fish_img = pygame.transform.scale(fish_img, (FISH_WIDTH, FISH_HEIGHT))

bottle_img = pygame.image.load('bottle.png')
bottle_img = pygame.transform.scale(bottle_img, (PLASTIC_WIDTH, PLASTIC_HEIGHT))

plastic_bag_img = pygame.image.load('plastic_bag.png')
plastic_bag_img = pygame.transform.scale(plastic_bag_img, (PLASTIC_WIDTH, PLASTIC_HEIGHT))

straw_img = pygame.image.load('straw.png')
straw_img = pygame.transform.scale(straw_img, (PLASTIC_WIDTH, PLASTIC_HEIGHT))

# Set up the game display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fish Dodging Microplastics")

# Fish class
class Fish:
    def __init__(self):
        self.image = fish_img
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT - FISH_HEIGHT - 10
        self.speed = 10

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        if self.rect.x < 0:  # Keep within screen boundaries
            self.rect.x = 0
        elif self.rect.x > SCREEN_WIDTH - FISH_WIDTH:
            self.rect.x = SCREEN_WIDTH - FISH_WIDTH
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > SCREEN_HEIGHT - FISH_HEIGHT:
            self.rect.y = SCREEN_HEIGHT - FISH_HEIGHT

# Plastic class
class Plastic:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - PLASTIC_WIDTH)
        self.rect.y = -PLASTIC_HEIGHT
        self.speed = NORMAL_SPEED
        self.accelerated = False

    def move(self):
        if self.accelerated:
            self.rect.y += ACCELERATED_SPEED
        else:
            self.rect.y += self.speed
        if self.rect.y > SCREEN_HEIGHT:
            self.rect.y = -PLASTIC_HEIGHT
            self.rect.x = random.randint(0, SCREEN_WIDTH - PLASTIC_WIDTH)
            self.accelerated = False  # Reset acceleration for the next appearance

# Main game loop
def game_loop():
    fish = Fish()

    # List of plastic objects with corresponding images
    plastics = [
        Plastic(bottle_img),
        Plastic(plastic_bag_img),
        Plastic(straw_img),
        Plastic(bottle_img),
        Plastic(plastic_bag_img)
    ]

    clock = pygame.time.Clock()
    start_time = time.time()

    running = True
    while running:
        game_over_boolean = False
        elapsed_time = time.time() - start_time
        if elapsed_time > TIME_LIMIT:# End game when time limit is reached
            running = False
            game_over_boolean = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_over_boolean = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            fish.move(-fish.speed, 0)
        if keys[pygame.K_RIGHT]:
            fish.move(fish.speed, 0)
        if keys[pygame.K_UP]:
            fish.move(0, -fish.speed)
        if keys[pygame.K_DOWN]:
            fish.move(0, fish.speed)

        # Move the plastics and check for collision
        for plastic in plastics:
            plastic.move()
            if random.random() < 0.01:  # 1% chance of plastic accelerating
                plastic.accelerated = True

            if fish.rect.colliderect(plastic.rect):
                running = False
                game_over_boolean = True

        # Drawing
        screen.fill("blue")
        screen.blit(fish.image, fish.rect)

        for plastic in plastics:
            screen.blit(plastic.image, plastic.rect)

        time_text = font.render(f"Time: {TIME_LIMIT - int(elapsed_time)}", True, "green")
        screen.blit(time_text, [SCREEN_WIDTH - 200, 10])

        if game_over_boolean:
            game_over = font.render("Game Over!", True, "black")
            screen.blit(game_over, [SCREEN_WIDTH - 500, 320]) 

        pygame.display.flip()
        clock.tick(60)

        if game_over_boolean:
            pygame.time.delay(1000)

    # End of the game
    print(f"Game over! Time survived: {int(elapsed_time)} seconds")
    pygame.quit()

# Run the game
game_loop()
