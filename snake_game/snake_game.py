'''Classes and functions for running snake game.'''
import random

import numpy as np
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.vector import Vector
from kivy.core.window import Window
from kivy.clock import Clock

SCALE = 50


def distance(a, b):
    '''Calculate Euclidean distance between two points.'''
    return np.sqrt(np.power(b[0]-a[0], 2) + np.power(b[1]-a[1], 2))


class Snake(Widget):
    '''Snake widget in the game.'''
    velocity = [1 * SCALE, 0]
    snake_tail = []
    position = []
    is_dead = False
    prev_pos = [0, 0]

    def move(self, direction):
        self.prev_pos = self.pos
        self.position.insert(0, list(self.prev_pos))

        del self.position[-(len(self.position) - len(self.snake_tail))]

        self.velocity = direction
        move = Vector(direction) + self.pos

        w, h = Window.size
        x, y = move

        if np.abs(x - 0) < SCALE or np.abs(x - w) < SCALE or np.abs(y - 0) < SCALE or np.abs(y - h) < SCALE / 2:
            self.dead()
            return

        for block_pos in self.position:
            if distance(move, block_pos) < SCALE / 2:
                self.dead()
                break

        else:
            self.pos = move

    def move_tail(self):
        if self.is_dead:
            for tail in self.snake_tail:
                self.remove_widget(tail)
            del self.snake_tail[0:len(self.snake_tail)]
            del self.position[0:len(self.position)]
            return

        for position, tail in zip(self.position, self.snake_tail):
            tail.pos = position

    def eat(self):
        tail = Tail(self.prev_pos)
        self.add_widget(tail)
        self.snake_tail.insert(0, tail)
        self.position.append(list(self.prev_pos))

    def dead(self):
        print('Try again!')
        self.is_dead = True
        self.pos = self.parent.center


class Tail(Widget):
    def __init__(self, position):
        super().__init__()
        self.pos = position


class Food(Widget):
    food = ObjectProperty(0)

    def change_location(self):
        wd, hg = Window.size
        location = [random.randrange(0+50, wd-50, SCALE),
                    random.randrange(0+50, hg-50, SCALE)]
        self.pos = location
        return location


class SnakeGame(Widget):
    '''Game board widget.'''
    snake = ObjectProperty(0)
    food = ObjectProperty(0)
    score = ObjectProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, *args):
        keycode = args[1]

        if keycode[1] == 'up' and self.snake.velocity != [0, 1 * SCALE] and self.snake.velocity != [0, -1 * SCALE]:
            self.snake.move([0, 1 * SCALE])
        elif keycode[1] == 'down' and self.snake.velocity != [0, -1*SCALE] and self.snake.velocity != [0, 1 * SCALE]:
            self.snake.move([0, -1 * SCALE])
        elif keycode[1] == 'right' and self.snake.velocity != [1*SCALE, 0] and self.snake.velocity != [-1 * SCALE, 0]:
            self.snake.move([1 * SCALE, 0 * SCALE])
        elif keycode[1] == 'left' and self.snake.velocity != [-1 * SCALE, 0] and self.snake.velocity != [1 * SCALE, 0]:
            self.snake.move([-1 * SCALE, 0])

        return True

    def update(self, _):
        if self.snake.is_dead:
            self.score.text = '0'
            self.snake.is_dead = False

        self.snake.move(self.snake.velocity)
        self.snake.move_tail()

        if distance(self.snake.pos, self.food.pos) < SCALE:
            self.food.change_location()
            self.snake.eat()
            self.score.text = str(int(self.score.text) + 1)


class SnakeApp(App):
    def build(self):
        game = SnakeGame()
        Clock.schedule_interval(game.update, 1/8)
        return game


def start_game():
    '''Start snake game.'''
    SnakeApp().run()


if __name__ == '__main__':
    start_game()
