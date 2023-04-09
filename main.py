import time
import pygame
import random

pygame.init()
screen_d = 900
screen_h = 600
screen = pygame.display.set_mode((screen_d, screen_h))
pygame.display.set_caption("MyFirstGame - Snake")
icon = pygame.image.load('images/4591880_animal_carnivore_cartoon_fauna_snake_icon.png')
pygame.display.set_icon(icon)

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

myfont = pygame.font.Font('fonts/Teko-Bold.ttf', 40)

def message(text, color):
    screen.blit(myfont.render(text, False, color), (screen_d // 2 - 100, screen_h // 2 - 50))

def FoodGen():
    f_x = round(random.randrange(0, screen_d - snake_size) / snake_size) * snake_size
    f_y = round(random.randrange(0, screen_h - snake_size) / snake_size) * snake_size
    return (f_x, f_y)

def snake_body(snake_size, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, snake_col, (x[0], x[1], snake_size, snake_size))

def Check(snake_list):
    if snake_list[0][0] >= screen_d or snake_list[0][0] < 0 or snake_list[0][1] >= screen_h or snake_list[0][1] < 0:
        return True
    for i in range(1, len(snake_list)):
        if snake_list[i] == snake_list[0] :
            return True
    return False

snake_size = 30
score = 0
records = []

def PrintRecords():
    records.sort(reverse=True)
    for i in range(min(len(records), 5)):
        screen.blit(myfont.render("{}. {} {}".format(i + 1, records[i][1], records[i][0]), False, red), (0, 50 * i))
    screen.blit(myfont.render("Press Q to return", False, red), (0, 50 * 6))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return

def GameLoop(snake_col, level, name):
    snake_speed = 5
    square = pygame.Surface((snake_size, snake_size))
    square.fill(snake_col)
    x0, y0 = screen_d // 2, screen_h // 2
    dx, dy = 0, 0
    clock = pygame.time.Clock()

    snake = [[x0, y0]]
    fx, fy = -1, -1
    score = 0
    food_flag = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if dx == snake_size:
                        continue
                    dx = -snake_size
                    dy = 0
                elif event.key == pygame.K_RIGHT:
                    if dx == -snake_size:
                        continue
                    dx = snake_size
                    dy = 0
                elif event.key == pygame.K_UP:
                    if dy == snake_size:
                        continue
                    dx = 0
                    dy = -snake_size
                elif event.key == pygame.K_DOWN:
                    if dy == -snake_size:
                        continue
                    dx = 0
                    dy = snake_size
                elif event.key == pygame.K_SPACE:
                    dx = 0
                    dy = 0
        x0 += dx
        y0 += dy
        snake.insert(0, [x0, y0])
        snake.pop(-1)
        if Check(snake):
            running = False
            screen.fill('black')
            message("You are lost!", red)
            screen.blit(myfont.render("Your score is {}!".format(score), False, red),
                        (screen_d // 2 - 100, screen_h // 2))
            pygame.display.update()
            time.sleep(3)
            records.append([score, name])
            break
        if not food_flag:
            fx, fy = FoodGen()
            food_flag = True
        if x0 == fx and y0 == fy and food_flag:
            score += 1
            food_flag = False
            if score == 1:
                snake.append([snake[0][0] - dx, snake[0][1] - dy])
            else:
                snake.append([snake[-1][0] - (snake[-2][0] - snake[-1][0]), snake[-1][1] - (snake[-2][1] - snake[-1][1])])
        screen.fill('black')
        pygame.draw.rect(screen, 'RED', (fx, fy, snake_size, snake_size))
        snake_body(snake_size, snake)
        pygame.display.update()
        clock.tick(snake_speed + score / 3)


while True:
    screen.fill('black')
    message("Hello!", red)
    screen.blit(myfont.render("1-Play 2-Records", False, red), (screen_d // 2 - 100, screen_h // 2))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    screen.fill('black')
                    message("Enter your name!!", red)
                    pygame.display.update()
                    name = ''
                    while event.key != pygame.K_RETURN:
                        pygame.event.clear()
                        pygame.event.wait()
                        name += event.unicode
                        if len(name) > 9:
                            break
                    screen.fill('black')
                    message("Select color of snake!", red)
                    screen.blit(myfont.render("1-Blue 2-Yellow 3-Green", False, red),
                                (screen_d // 2 - 100, screen_h // 2))
                    pygame.display.update()
                    snake_col = ''
                    while True:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False
                                pygame.quit()
                                exit(0)
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_1:
                                    snake_col = 'Blue'
                                    break
                                elif event.key == pygame.K_2:
                                    snake_col = 'Yellow'
                                    break
                                elif event.key == pygame.K_3:
                                    snake_col = 'Green'
                                    break
                        if snake_col != '':
                            break
                    GameLoop(snake_col, 1, name)
                    break
                elif event.key == pygame.K_2:
                    screen.fill('black')
                    PrintRecords()
        break