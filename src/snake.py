

class Snake:
    def __init__(self, x, y):
        self.snake_blocks = [[x, y]]

    def get_head(self):
        return self.snake_blocks[0]

    def is_inside(self, screen_size):
        return 0 <= self.snake_blocks[0][0] < screen_size and 0 <= self.snake_blocks[0][1] < screen_size

    def is_crash(self):
        for i in range(1, len(self.snake_blocks)):
            if self.snake_blocks[i] == self.snake_blocks[0]:
                return True
        return False
