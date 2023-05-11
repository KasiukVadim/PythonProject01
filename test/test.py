import unittest


import snake
import apple


class TestSnakeMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.sn1 = snake.Snake(1, 1)
        self.sn2 = snake.Snake(10, 8)
        sn2_list = [[11, 8], [12, 8], [13, 8], [13, 9], [12, 9], [11, 9], [10, 9], [10, 8]]
        for block in sn2_list:
            self.sn2.snake_blocks.append(block)
        self.sn3 = snake.Snake(5, 13)
        sn3_list = [[4, 13], [3, 13], [3, 12], [3, 11]]
        for block in sn3_list:
            self.sn3.snake_blocks.append(block)
        # 3 змейки готово 1 - точка, 3 - буква г, 2 - самопересекающаяся(ударилась головой об себя)

    def test_get_head(self):
        self.assertEqual(self.sn1.get_head(), [1, 1], 'Snake.get_head is working bad! Test1')
        self.assertEqual(self.sn2.get_head(), [10, 8], 'Snake.get_head is working bad! Test2')
        self.assertEqual(self.sn3.get_head(), [5, 13], 'Snake.get_head is working bad! Test3')

    def test_is_inside(self):
        self.assertTrue(self.sn1.is_inside(2), 'Snake.is_inside is working bad! Test 1')
        self.assertFalse(self.sn1.is_inside(1), 'Snake.is_inside is working bad! Test 2')
        self.assertTrue(self.sn2.is_inside(20), 'Snake.is_inside is working bad! Test 3')
        self.assertFalse(self.sn2.is_inside(5), 'Snake.is_inside is working bad! Test 4')
        self.assertTrue(self.sn3.is_inside(100), 'Snake.is_inside is working bad! Test 5')
        self.assertFalse(self.sn3.is_inside(10), 'Snake.is_inside is working bad! Test 6')

    def test_is_crash(self):
        self.assertFalse(self.sn1.is_crash(), 'Snake.is_crash is working bad! Test 1')
        self.assertTrue(self.sn2.is_crash(), 'Snake.is_crash is working bad! Test 2')
        self.assertFalse(self.sn3.is_crash(), 'Snake.is_crash is working bad! Test 3')


class TestAppleMethods(unittest.TestCase):

    def setUp(self) -> None:
        self.apple = apple.Apple([[0, 0]], 1, True, 20)
        self.apple.x, self.apple.y = 10, 10
        self.golden_apple = apple.Apple([[0, 0]], 3, True, 20)
        self.golden_apple.x, self.golden_apple.y = 10, 10
        self.black_apple = apple.Apple([[0, 0]], -5, True, 20)
        self.black_apple.x, self.black_apple.y = 10, 10

    def test_try_to_eat(self):
        self.assertEqual(self.apple.try_to_eat_apple(0, 1, [[5, 5]], self.golden_apple, self.black_apple),
                         (0, 1), 'Apple.try_to_eat_apple is working bad! Test 1')
        self.assertEqual(self.apple.try_to_eat_apple(0, 1, [[10, 10]], self.golden_apple, self.black_apple),
                         (1, 0), 'Apple.try_to_eat_apple is working bad! Test 2')
        self.assertEqual(self.golden_apple.try_to_eat_apple(0, 1, [[5, 5]], self.golden_apple, self.black_apple),
                         (0, 1), 'Apple.try_to_eat_apple is working bad! Test 3')
        self.assertEqual(self.golden_apple.try_to_eat_apple(0, 1, [[10, 10]], self.golden_apple, self.black_apple),
                         (3, 0), 'Apple.try_to_eat_apple is working bad! Test 4')
        self.assertEqual(self.black_apple.try_to_eat_apple(0, 1, [[5, 5]], self.golden_apple, self.black_apple),
                         (0, 1), 'Apple.try_to_eat_apple is working bad! Test 5')
        self.assertEqual(self.black_apple.try_to_eat_apple(0, 1, [[10, 10]], self.golden_apple, self.black_apple),
                         (-5, 1), 'Apple.try_to_eat_apple is working bad! Test 6')


if __name__ == '__main__':
    unittest.main()
