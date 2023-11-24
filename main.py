import pygame
import random


# Define Colors
DARK_GREY = (50, 50, 50)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

def check_collision(object1, object2):
    for i in range(len(object1)):
        for j in range(len(object2)):
            if rectCollide(object1[i], object2[j]):
                return j
    return -1

def rectCollide(rect1, rect2):
    return rect1.x < rect2.x + rect2.width and rect1.y < rect2.y + rect2.height and rect1.x + rect1.width > rect2.x and rect1.y + rect1.height > rect2.y

class Circle():
    def __init__(self, x, y, width, height, colour, change_x, change_y, line_width):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.change_x = change_x
        self.change_y = change_y
        self.line_width = line_width

    def edge_collision(self):
        if self.x > SCREEN_WIDTH - self.width:
            self.change_x = -1 * self.change_x
        elif self.y > 650 - self.height:
            self.change_y = -1 * self.change_y
        elif self.x < 0:
            self.change_x = -1 * self.change_x
        elif self.y < 0:
            self.change_y = -1 * self.change_y
    
    def update(self):
        self.x = self.x + self.change_x
        self.y = self.y + self.change_y


    def draw_circle(self, screen):
        pygame.draw.ellipse(screen, self.colour, [self.x, self.y, self.width, self.height], self.line_width)

class Player():
    def __init__(self, x, y, width, height, change_x, change_y):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.change_x = change_x
        self.change_y = change_y

    def go_left(self):
        self.change_x = -3
    
    def go_right(self):
        self.change_x = 3

    def hzstop(self):
        self.change_x = 0

    def update(self):
        self.x = self.x + self.change_x
        self.y = self.y + self.change_y
    
    def draw_player(self, screen):
        pygame.draw.ellipse(screen, WHITE, [self.x, self.y, self.width, self.height])
        pygame.draw.rect(screen, RED, [self.x + (self.width / 2.25), self.y, self.width / 8, self.height / 2])

def main():
    # Initialize pygame
    pygame.init()

    # Circles list
    random_circles = []

    # Bullet list
    bullets = []

    # Player
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100, 50, 50, 0, 0)
    # Screen
    size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen = pygame.display.set_mode(size)
    frameCount = 1

    clock = pygame.time.Clock()
    # Loop
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            # Player movement
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.go_left()
                elif event.key == pygame.K_d:
                    player.go_right()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a and player.change_x < 0 or event.key == pygame.K_d and player.change_x > 0:
                    player.hzstop
            # When I click the mouse I make a new bullet
            elif event.type == pygame.MOUSEBUTTONDOWN:
                bullets.append(Circle(player.x + (player.width / 2.5), player.y, 10, 10, WHITE, 0, -10, 0))

        # make new width and height for random circles every loop
        circle_width = random.randrange(20, 50)
        circle_height = circle_width
        random_colour = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
        if frameCount % 120 == 0:
            random_circles.append(Circle(random.randrange(0, SCREEN_WIDTH - circle_width), random.randrange(0, 550), circle_width, circle_height, random_colour, random.randrange(1, 5), random.randrange(1, 5), 2))
        # move circles
        for i in range(len(random_circles)):
            random_circles[i].update()
            random_circles[i].edge_collision()
        # move bullets
        for i in range(len(bullets)):
            bullets[i].update()
        # Check bullet and random circle collision
        if check_collision(bullets, random_circles) != -1:
            print(check_collision(bullets, random_circles))
            random_circles.pop(check_collision(bullets, random_circles))
        # Remove bullets when at the top of the screen
        for i in range(len(bullets)):
            if bullets[i].y < 0:
                bullets.pop(i)
        # move player
        player.update()
        print(len(bullets))

    # Drawing
        screen.fill(DARK_GREY)
        # line above player
        pygame.draw.line(screen, WHITE, (0, 650), (SCREEN_WIDTH, 650), 2)
        # draw player
        player.draw_player(screen)
        # Draw circles
        for i in range(len(random_circles)):
            random_circles[i].draw_circle(screen)
        # Draw bullets
        for i in range(len(bullets)):
            bullets[i].draw_circle(screen)

        # Manage how fast the screen updates
        frameCount += 1
        clock.tick(60)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()