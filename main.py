import pygame
import sys
import pygame_menu
import snake_meth_class

pygame.init()
bg_image = pygame.image.load('logo.jpg')
YELLOW = (204, 204, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
FRAME_COLOR = (0, 255, 204)
WHITE = (255, 255, 255)
BLUE = (204, 255, 255)
SIZE_BLOCK = 20
COUNT_BLOCKS = 20
MARGIN = 1
HEADER_COLOR = (0, 204, 153)
HEADER_MARGIN = 70
SNAKE_COLOR = (0, 102, 0)
timer = pygame.time.Clock()

size = [SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCKS,
        SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCKS + HEADER_MARGIN]

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Змейка')
courier = pygame.font.SysFont('courier', 36)

rec_file = open('records.txt', 'r')
records = []
for rec in rec_file:
    rec_l = rec.split()
    rec_l[0] = int(rec_l[0])
    records.append(rec_l)
rec_file.close()


def draw_block(color, row, column, s_bl, mar, head_mar):
    pygame.draw.rect(screen, color, [s_bl + column * s_bl + mar * (column + 1),
                                     head_mar + s_bl + row * s_bl + mar * (row + 1),
                                     s_bl,
                                     s_bl])


def start_the_game():
    d_row, d_col = 1, 0
    score = 0
    speed = 0
    snake = snake_meth_class.Snake(COUNT_BLOCKS // 2, COUNT_BLOCKS // 2)
    apple = snake_meth_class.Apple(snake.sn_bl, 1, True, COUNT_BLOCKS)
    golden_apple = snake_meth_class.Apple(snake.sn_bl, 3, False, COUNT_BLOCKS)
    black_apple = snake_meth_class.Apple(snake.sn_bl, -5, False, COUNT_BLOCKS)
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('exit')
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                print('KEY')
                if event.key == pygame.K_UP and d_row != 1:
                    d_row, d_col = -1, 0
                elif event.key == pygame.K_DOWN and d_row != -1:
                    d_row, d_col = 1, 0
                elif event.key == pygame.K_LEFT and d_col != 1:
                    d_row, d_col = 0, -1
                elif event.key == pygame.K_RIGHT and d_col != 1:
                    d_row, d_col = 0, 1

        screen.fill(FRAME_COLOR)
        pygame.draw.rect(screen, HEADER_COLOR, [0, 0, size[0], HEADER_MARGIN])
        text_score = courier.render(f"Score: {score}", False, WHITE)
        text_speed = courier.render(f"Speed: {speed}", False, WHITE)
        screen.blit(text_score, (SIZE_BLOCK, SIZE_BLOCK))
        screen.blit(text_speed, (SIZE_BLOCK + 200, SIZE_BLOCK))
        for row in range(COUNT_BLOCKS):
            for column in range(COUNT_BLOCKS):
                if (column + row) % 2 == 0:
                    colour = BLUE
                else:
                    colour = WHITE
                draw_block(colour, row, column, SIZE_BLOCK, MARGIN, HEADER_MARGIN)

        if not snake.is_inside(SIZE_BLOCK):
            print('crash Out')
            records.append([score, name.get_value()])
            break
        if snake.is_crash():
            print('crash Out')
            records.append([score, name.get_value()])
            break
        draw_block(RED, apple.x, apple.y, SIZE_BLOCK, MARGIN, HEADER_MARGIN)
        if golden_apple.flag:
            draw_block(YELLOW, golden_apple.x, golden_apple.y, SIZE_BLOCK, MARGIN, HEADER_MARGIN)
        if black_apple.flag:
            draw_block(BLACK, black_apple.x, black_apple.y, SIZE_BLOCK, MARGIN, HEADER_MARGIN)

        for block in snake.sn_bl:
            draw_block(SNAKE_COLOR, block[0], block[1], SIZE_BLOCK, MARGIN, HEADER_MARGIN)
        score, speed = apple.try_to_eat_apple(score, speed, snake.sn_bl, golden_apple, black_apple)
        if not apple.flag:
            apple = snake_meth_class.Apple(snake.sn_bl, 1, True, COUNT_BLOCKS)
        score, speed = golden_apple.try_to_eat_apple(score, speed, snake.sn_bl, golden_apple, black_apple)
        if not golden_apple.flag:
            golden_apple = snake_meth_class.Apple(snake.sn_bl, 3, False, COUNT_BLOCKS)
        score, speed = black_apple.try_to_eat_apple(score, speed, snake.sn_bl, golden_apple, black_apple)
        if not black_apple.flag:
            black_apple = snake_meth_class.Apple(snake.sn_bl, -5, False, COUNT_BLOCKS)

        new_head = [d_row + snake.sn_bl[0][0], d_col + snake.sn_bl[0][1]]
        snake.sn_bl.insert(0, new_head)
        snake.sn_bl.pop()
        pygame.display.flip()
        timer.tick(3 + speed)


def records_table():
    screen.fill(FRAME_COLOR)
    records.sort(reverse=True)
    screen.blit(courier.render("№  Name   Score", False, WHITE), (SIZE_BLOCK, SIZE_BLOCK))
    for rec in range(min(len(records), 5)):
        text = courier.render(f"{rec + 1}. {records[rec][1]} {records[rec][0]}", False, WHITE)
        screen.blit(text, (SIZE_BLOCK, SIZE_BLOCK + 50 * (rec + 1)))
    screen.blit(courier.render("Press Q to return", False, WHITE), (0, 50 * 8))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return


def save_records():
    w_rec_file = open('records.txt', 'w')
    for rec in records:
        w_rec_file.write(str(rec[0]) + ' ' + rec[1] + '\n')
    w_rec_file.close()


menu = pygame_menu.Menu('Welcome', 400, 300,
                        theme=pygame_menu.themes.THEME_BLUE)

name = menu.add.text_input('Имя:', default='Игрок 1')
menu.add.button('Рекорды', records_table)
menu.add.button('Сохранить результаты', save_records)
menu.add.button('Играть', start_the_game)
menu.add.button('Выход', pygame_menu.events.EXIT)

while True:  # Оставляю

    screen.blit(bg_image, (0, 0))

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()

    if menu.is_enabled():
        menu.update(events)
        menu.draw(screen)

    pygame.display.update()
