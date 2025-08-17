import pygame, sys, random

pygame.init()
screen = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 35)

snake = [(200, 200)]
direction = (20, 0)
food = (random.randrange(0, 400, 20), random.randrange(0, 400, 20))
score = 0
game_over = False
special_food = None
normal_food_count = 0
grow = 0

def reset_game():
    global snake, direction, food, score, game_over, special_food, normal_food_count, grow
    snake = [(200, 200)]
    direction = (20, 0)
    food = (random.randrange(0, 400, 20), random.randrange(0, 400, 20))
    special_food = None
    score = 0
    game_over = False
    normal_food_count = 0
    grow = 0

def move_snake():
    global snake, grow
    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    snake.insert(0, new_head)
    if grow > 0:
        grow -= 1
    else:
        snake.pop()

def check_collision():
    global game_over
    x, y = snake[0]
    if x < 0 or x >= 400 or y < 0 or y >= 400:
        game_over = True
    if snake[0] in snake[1:]:
        game_over = True

def main():
    global direction, food, score, special_food, normal_food_count, grow, game_over

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if not game_over:
                    if event.key == pygame.K_UP and (len(snake) == 1 or snake[0][0] != snake[1][0]):
                        direction = (0, -20)
                    if event.key == pygame.K_DOWN and (len(snake) == 1 or snake[0][0] != snake[1][0]):
                        direction = (0, 20)
                    if event.key == pygame.K_LEFT and (len(snake) == 1 or snake[0][1] != snake[1][1]):
                        direction = (-20, 0)
                    if event.key == pygame.K_RIGHT and (len(snake) == 1 or snake[0][1] != snake[1][1]):
                        direction = (20, 0)
                if game_over and event.key == pygame.K_r:
                    reset_game()

        if not game_over:
            move_snake()

            if snake[0] == food:
                grow += 1
                score += 1
                normal_food_count += 1
                food = (random.randrange(0, 400, 20), random.randrange(0, 400, 20))
                if normal_food_count % 3 == 0:
                    special_food = (random.randrange(0, 400, 20), random.randrange(0, 400, 20))

            if special_food and snake[0] == special_food:
                grow += 1
                score += 5
                special_food = None

            check_collision()

        screen.fill((0, 0, 0))
        for i, segment in enumerate(snake):
            color = (0, 200, 0) if i % 2 == 0 else (0, 255, 0)
            pygame.draw.rect(screen, color, (*segment, 20, 20))

        head_x, head_y = snake[0]
        eye_color = (0, 0, 0)
        if direction == (20, 0):
            pygame.draw.circle(screen, eye_color, (head_x + 15, head_y + 5), 3)
            pygame.draw.circle(screen, eye_color, (head_x + 15, head_y + 15), 3)
        if direction == (-20, 0):
            pygame.draw.circle(screen, eye_color, (head_x + 5, head_y + 5), 3)
            pygame.draw.circle(screen, eye_color, (head_x + 5, head_y + 15), 3)
        if direction == (0, -20):
            pygame.draw.circle(screen, eye_color, (head_x + 5, head_y + 5), 3)
            pygame.draw.circle(screen, eye_color, (head_x + 15, head_y + 5), 3)
        if direction == (0, 20):
            pygame.draw.circle(screen, eye_color, (head_x + 5, head_y + 15), 3)
            pygame.draw.circle(screen, eye_color, (head_x + 15, head_y + 15), 3)

        pygame.draw.rect(screen, (255, 0, 0), (*food, 20, 20))
        if special_food:
            pygame.draw.rect(screen, (0, 0, 255), (*special_food, 20, 20))

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        if game_over:
            over_text = font.render("Game Over! Press R to Restart", True, (255, 0, 0))
            screen.blit(over_text, (20, 180))

        pygame.display.flip()
        clock.tick(10)

if __name__ == "__main__":
    main()
