import pygame
import random

# Initialize Pygame
pygame.init()

# Set up constants
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
GAME_WIDTH, HEIGHT = 600, 600
SCOREBOARD_WIDTH = 200
WIDTH = GAME_WIDTH + SCOREBOARD_WIDTH 
FPS = 60

# Set up screen and clock
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Normal difficulty")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 50)
font1 = pygame.font.Font(None, 17)

# Game variables
stick_width, stick_height = 100, 20
stick_x = (GAME_WIDTH - stick_width) // 2
stick_y = HEIGHT - 50
stick_speed = 10

ball_radius = 10
fall_count = 0
score = 0

bricks = []  # List of brick rows
brick_width = 75
brick_height = 30
brick_rows = 5
brick_columns = GAME_WIDTH // (brick_width + 10)

balls = []  # List to store multiple balls

# Function to spawn new ball
def spawn_balls():
    new_ball_1 = {'x': random.randint(0, GAME_WIDTH - ball_radius * 2), 'y': 250, 'x_speed': -3, 'y_speed': 1}
    balls.append(new_ball_1)


# Function to check collision with bricks
def check_brick_collision(ball):
    for row in bricks:
        for brick in row:
            if brick['visible']:
                brick_x, brick_y = brick['x'], brick['y']
                if brick_x < ball['x'] < brick_x + brick_width and brick_y < ball['y'] < brick_y + brick_height:
                    ball['y_speed'] *= -1  # Bounce the ball
                    brick['visible'] = False  # Hide the brick
                    return True
    return False

# Initialize bricks
def initialize_bricks():
    global bricks
    bricks = []
    for row in range(brick_rows):
        brick_row = []
        for col in range(brick_columns):
            brick_x = col * (brick_width + 10) + 5
            brick_y = row * (brick_height + 10) + 5
            brick_row.append({'x': brick_x, 'y': brick_y, 'visible': True})
        bricks.append(brick_row)

# Function to add a new row of bricks at the top
def add_new_row():
    new_row = []
    for col in range(brick_columns):
        brick_x = col * (brick_width + 10) + 5
        brick_y = 5  # Start the new row at the top
        new_row.append({'x': brick_x, 'y': brick_y, 'visible': True})
    bricks.insert(0, new_row)  # Add the new row at the top

# Function to move all rows down
def move_bricks_down():
    for row in bricks:
        for brick in row:
            brick['y'] += (brick_height + 10)  # Move each brick down

# Draw stick
def draw_stick(x, y):
    pygame.draw.rect(window, BLACK, (x, y, stick_width, stick_height))

# Draw ball
def draw_ball(ball_x, ball_y):
    pygame.draw.circle(window, BLACK, (ball_x, ball_y), ball_radius)

# Draw bricks
def draw_bricks():
    for row in bricks:
        for brick in row:
            if brick['visible']:
                pygame.draw.rect(window, BLACK, (brick['x'], brick['y'], brick_width, brick_height))

# Draw score
def draw_score():
    text = font.render(f'Score: {score}', True, BLACK)
    window.blit(text, (GAME_WIDTH + 10, 20))  # Draw the score outside the game boundary


# Main game loop
def game_loop():
    global stick_x, score, fall_count, balls

    running_ez = True

    # Spawn the first ball
    balls.append({'x': random.randint(0, GAME_WIDTH - ball_radius * 2), 'y': 250, 'x_speed': 0, 'y_speed': 1})

    # Initialize bricks
    initialize_bricks()

    while running_ez:
        window.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_ez = False

        # Stick movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and stick_x > 0:
            stick_x -= stick_speed
        elif keys[pygame.K_RIGHT] and stick_x < GAME_WIDTH - stick_width:
            stick_x += stick_speed

        # Handle ball movement for all balls
        for ball in balls[:]:  # Copy the list to safely modify it during iteration
            ball['y'] += ball['y_speed']
            ball['x'] += ball['x_speed']  # Ball's horizontal movement

            # Ball bounce off walls (left and right boundaries)
            if ball['x'] - ball_radius <= 0 or ball['x'] + ball_radius >= GAME_WIDTH:
                ball['x_speed'] *= -1  # Reverse direction when hitting boundaries

            if ball['y'] - ball_radius <= 0:  # Bounce off top boundary
                ball['y_speed'] *= -1

            # Check if the ball hits the stick
            if (ball['y'] + ball_radius * 2 >= stick_y and stick_x < ball['x'] + ball_radius and ball['x'] + ball_radius < stick_x + stick_width):
                ball_bounceheight = 4  # Default bounce height

                # Increase bounce height if space bar is held
                if keys[pygame.K_SPACE]:
                    ball_bounceheight = 8

                ball['y_speed'] = -abs(ball_bounceheight)  # Reverse ball speed (bounce)

                # Make ball inherit stick's horizontal speed
                if keys[pygame.K_RIGHT]:
                    ball['x_speed'] = 3  # Move ball right
                elif keys[pygame.K_LEFT]:
                    ball['x_speed'] = -3  # Move ball left
                else:
                    ball['x_speed'] = 0  # No horizontal movement if stick isn't moving

            # Brick collision
            if check_brick_collision(ball):
                score += 10  # Increase score for hitting a brick
                continue  # Skip further logic if a brick was hit to avoid double detection

            # Gravity effect after bouncing
            if ball['y'] + ball_radius * 2 < stick_y:
                ball['y_speed'] += 0.05  # Gravity effect

            # Check if the ball falls below the screen (missed catch)
            if ball['y'] > HEIGHT:
                fall_count += 1
                balls.remove(ball)  # Remove the fallen ball
                spawn_balls()  # Spawn new ball
                move_bricks_down()  # Move all bricks down
                add_new_row()  # Add a new row of bricks at the top

        # Check if the game is over (bricks reach the stick)
        if any(brick['y'] >= stick_y - brick_height and brick['visible'] for row in bricks for brick in row):
            window.fill(WHITE)
            text = font.render('Game Over', True, RED)
            window.blit(text, (GAME_WIDTH // 2.5, HEIGHT // 2))
            pygame.display.update()
            pygame.time.wait(2000)
            running_ez = False

        # Check if the player wins (no more bricks)
        if all(not brick['visible'] for row in bricks for brick in row):
            window.fill(WHITE)
            text = font.render('You Win!', True, GREEN)
            window.blit(text, (GAME_WIDTH // 2.5, HEIGHT // 2))
            pygame.display.update()
            pygame.time.wait(2000)
            running_ez = False

        # Draw everything
        draw_stick(stick_x, stick_y)
        for ball in balls:
            draw_ball(ball['x'], ball['y'])
        draw_bricks()
        draw_score()
        pygame.draw.rect(window,BLACK,(598,0,4,600))


        pygame.display.update()
        clock.tick(FPS)

# Run the game loop
game_loop()

# Quit Pygame
pygame.quit()
