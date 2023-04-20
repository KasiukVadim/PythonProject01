import random


class Snake:
    def __init__(self, x, y):
        self.sn_bl = [[x, y]]

    def get_head(self):
        return self.sn_bl[0]

    def is_inside(self, screen_size):
        return 0 <= self.sn_bl[0][0] < screen_size and 0 <= self.sn_bl[0][1] < screen_size

    def is_crash(self):
        for i in range(1, len(self.sn_bl) - 1):
            if self.sn_bl[i] == self.sn_bl[0]:
                return True
        return False


class Apple:
    def __init__(self, snake_head, value, flag, cn_bl):
        x_new = random.randint(0, cn_bl - 1)
        y_new = random.randint(0, cn_bl - 1)
        empty_block = [x_new, y_new]
        while empty_block in snake_head:
            x = random.randint(0, cn_bl - 1)
            y = random.randint(0, cn_bl - 1)
            empty_block = [x, y]
        self.x = x_new
        self.y = y_new
        self.flag = flag
        self.value = value

    def try_to_eat_apple(self, score, speed, head, g_a, b_a):
        if [self.x, self.y] == head[0] and self.flag:
            print("eat")
            score += self.value
            speed = abs(score) // 5
            head.append(head[-1])
            self.flag = False
            if random.randint(0, 5) == 1:
                g_a.flag = True
            if random.randint(0, 5) == 1:
                b_a.flag = True
        return score, speed

    def get_apple(self):
        return [self.x, self.y]

    def __eq__(self, other):
        return self.x == other[0] and self.y == other[1]
