import pygame
import sys
import random
import pygame_menu

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


def draw_block(color, row, column):
    pygame.draw.rect(screen, color, [SIZE_BLOCK + column * SIZE_BLOCK + MARGIN * (column + 1),
                                     HEADER_MARGIN + SIZE_BLOCK + row * SIZE_BLOCK + MARGIN * (row + 1),
                                     SIZE_BLOCK,
                                     SIZE_BLOCK])


def get_random_empty_block():
    x = random.randint(0, COUNT_BLOCKS - 1)
    y = random.randint(0, COUNT_BLOCKS - 1)
    empty_block = SnakeBlock(x, y)
    while empty_block in snake_blocks:
        x = random.randint(0, COUNT_BLOCKS - 1)
        y = random.randint(0, COUNT_BLOCKS - 1)
        empty_block = SnakeBlock(x, y)
    return empty_block


class SnakeBlock:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_inside(self):
        return 0 <= self.x < SIZE_BLOCK and 0 <= self.y < SIZE_BLOCK

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


snake_blocks = [SnakeBlock(COUNT_BLOCKS // 2, COUNT_BLOCKS // 2)]

RECORDS = []


def start_the_game():
    d_row, d_col = 1, 0
    apple = get_random_empty_block()
    golden_apple = get_random_empty_block()
    black_apple = get_random_empty_block()
    total = 0
    speed = 0
    snake_blocks = [SnakeBlock(COUNT_BLOCKS // 2, COUNT_BLOCKS // 2)]
    golden_apple_flag = False
    black_apple_flag = False

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
        text_total = courier.render(f"Total: {total}", False, WHITE)
        text_speed = courier.render(f"Speed: {speed}", False, WHITE)
        screen.blit(text_total, (SIZE_BLOCK, SIZE_BLOCK))
        screen.blit(text_speed, (SIZE_BLOCK + 200, SIZE_BLOCK))
        for row in range(COUNT_BLOCKS):
            for column in range(COUNT_BLOCKS):
                if (column + row) % 2 == 0:
                    colour = BLUE
                else:
                    colour = WHITE
                draw_block(colour, row, column)

        head = snake_blocks[-1]
        if not head.is_inside():
            print('crash')
            RECORDS.append([total, name.get_value()])
            break
        draw_block(RED, apple.x, apple.y)
        if golden_apple_flag:
            draw_block(YELLOW, golden_apple.x, golden_apple.y)
        if black_apple_flag:
            draw_block(BLACK, black_apple.x, black_apple.y)
        for block in snake_blocks:
            draw_block(SNAKE_COLOR, block.x, block.y)
        if apple == head:
            print("eat")
            total += 1
            speed = abs(total) // 5
            snake_blocks.append(apple)
            apple = get_random_empty_block()
            if random.randint(0, 5) == 1:
                golden_apple_flag = True
            if random.randint(0, 5) == 1:
                black_apple_flag = True
        if golden_apple == head:
            print("eat")
            total += 3
            speed = abs(total) // 5
            snake_blocks.append(golden_apple)
            golden_apple_flag = False
            if random.randint(0, 5) == 1:
                golden_apple_flag = True
            if random.randint(0, 5) == 1:
                black_apple_flag = True
        if black_apple == head:
            print("eat")
            total -= 5
            speed = abs(total) // 5
            snake_blocks.append(black_apple)
            black_apple_flag = False
            if random.randint(0, 5) == 1:
                golden_apple_flag = True
            if random.randint(0, 5) == 1:
                black_apple_flag = True
        new_head = SnakeBlock(head.x + d_row, head.y + d_col)
        if new_head in snake_blocks:
            print('crash')
            RECORDS.append([total, name.get_value()])
            break
        snake_blocks.append(new_head)
        snake_blocks.pop(0)

        pygame.display.flip()
        timer.tick(3 + speed)


def records_table():
    screen.fill(FRAME_COLOR)
    RECORDS.sort(reverse=True)
    screen.blit(courier.render("№  Name   Score", False, WHITE), (SIZE_BLOCK, SIZE_BLOCK))
    for rec in range(min(len(RECORDS), 5)):
        text = courier.render("{}. {} {}".format(rec + 1, RECORDS[rec][1], RECORDS[rec][0]), False, WHITE)
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


menu = pygame_menu.Menu('Welcome', 400, 300,
                        theme=pygame_menu.themes.THEME_BLUE)

name = menu.add.text_input('Имя:', default='Игрок 1')
menu.add.button('Рекорды', records_table)
menu.add.button('Играть', start_the_game)
menu.add.button('Выход', pygame_menu.events.EXIT)

while True:

    screen.blit(bg_image, (0, 0))

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()

    if menu.is_enabled():
        menu.update(events)
        menu.draw(screen)

    pygame.display.update()
