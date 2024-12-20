import pygame, random, json
from pygame.locals import *

# Funções auxiliares
def on_grid_random():
    x = random.randint(0, 59)
    y = random.randint(0, 59)
    return (x * 10, y * 10)

def collision(c1, c2):
    return (c1[0] == c2[0]) and (c1[1] == c2[1])

# Carrega o HighScore de um arquivo JSON
def load_highscore():
    try:
        with open('highscore.json', 'r') as f:
            data = json.load(f)
            return data.get("highscore", 0)
    except (FileNotFoundError, json.JSONDecodeError):
        return 0

# Salva o HighScore em um arquivo JSON
def save_highscore(highscore):
    with open('highscore.json', 'w') as f:
        json.dump({"highscore": highscore}, f)

# Definição de macro para o movimento da cobra.
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Snake')

snake = [(200, 200), (210, 200), (220, 200)]
snake_skin = pygame.Surface((10, 10))
snake_skin.fill((255, 255, 255))  # Branco

apple_pos = on_grid_random()
apple = pygame.Surface((10, 10))
apple.fill((255, 0, 0))

my_direction = LEFT

clock = pygame.time.Clock()

font = pygame.font.Font('freesansbold.ttf', 18)
score = 0

# Carrega o HighScore
highscore = load_highscore()

game_over = False
while not game_over:
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == KEYDOWN:
            if event.key == K_UP and my_direction != DOWN:
                my_direction = UP
            if event.key == K_DOWN and my_direction != UP:
                my_direction = DOWN
            if event.key == K_LEFT and my_direction != RIGHT:
                my_direction = LEFT
            if event.key == K_RIGHT and my_direction != LEFT:
                my_direction = RIGHT

    if collision(snake[0], apple_pos):
        apple_pos = on_grid_random()
        snake.append((0, 0))
        score += 1
        
        # Atualiza o HighScore
        if score > highscore:
            highscore = score
        
    # Verifique se a cobra colidiu com os limites
    if snake[0][0] == 600 or snake[0][1] == 600 or snake[0][0] < 0 or snake[0][1] < 0:
        game_over = True
        break
    
    # Verifique se a cobra se acertou
    for i in range(1, len(snake) - 1):
        if snake[0][0] == snake[i][0] and snake[0][1] == snake[i][1]:
            game_over = True
            break

    if game_over:
        break
    
    for i in range(len(snake) - 1, 0, -1):
        snake[i] = (snake[i-1][0], snake[i-1][1])
        
    # Na verdade, faça a cobra se mover.
    if my_direction == UP:
        snake[0] = (snake[0][0], snake[0][1] - 10)
    if my_direction == DOWN:
        snake[0] = (snake[0][0], snake[0][1] + 10)
    if my_direction == RIGHT:
        snake[0] = (snake[0][0] + 10, snake[0][1])
    if my_direction == LEFT:
        snake[0] = (snake[0][0] - 10, snake[0][1])
    
    screen.fill((0, 0, 0))
    screen.blit(apple, apple_pos)
    
    for x in range(0, 600, 10):  # Desenhe linhas verticais
        pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, 600))
    for y in range(0, 600, 10):  # Desenhe linhas horizontais
        pygame.draw.line(screen, (40, 40, 40), (0, y), (600, y))
    
    score_font = font.render('Score: %s' % (score), True, (255, 255, 255))
    score_rect = score_font.get_rect()
    score_rect.topleft = (10, 10)
    screen.blit(score_font, score_rect)

    highscore_font = font.render('HighScore: %s' % (highscore), True, (255, 255, 255))
    highscore_rect = highscore_font.get_rect()
    highscore_rect.topleft = (10, 30)
    screen.blit(highscore_font, highscore_rect)
    
    for pos in snake:
        screen.blit(snake_skin, pos)

    pygame.display.update()

# Salva o HighScore antes de encerrar
save_highscore(highscore)

while True:
    game_over_font = pygame.font.Font('freesansbold.ttf', 75)
    game_over_screen = game_over_font.render('Game Over', True, (255, 255, 255))
    game_over_rect = game_over_screen.get_rect()
    game_over_rect.midtop = (600 / 2, 10)
    screen.blit(game_over_screen, game_over_rect)
    pygame.display.update()
    pygame.time.wait(500)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
