from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, ListProperty
from kivy.vector import Vector
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
import numpy as np
import random


def distance(a, b):
    return np.sqrt(np.power(b[0]-a[0], 2) + np.power(b[1]-a[1], 2))


scl = 50


class Snake(Widget):
    velocity = [1*scl, 0]
    snakeTails = []
    snakePos = []
    isDead = False
    prevPos = [0, 0]


    def move(self, direction):
        self.prevPos = self.pos
        self.snakePos.insert(0, list(self.prevPos))

        del self.snakePos[-(len(self.snakePos) - len(self.snakeTails))]

        self.velocity = direction
        move = Vector(direction) + self.pos

        w, h = Window.size
        x, y = move

        if np.abs(x-0) < scl or np.abs(x-w) < scl or np.abs(y-0) < scl or np.abs(y-h) < scl/2:
            self.dead()
            return

        for blockPositions in self.snakePos:
            if distance(move, blockPositions) < scl/2:
                self.dead()
                break

        else:
            self.pos = move



    def moveTail(self):
        if self.isDead:
            for tail in self.snakeTails:
                self.remove_widget(tail)
            del self.snakeTails[0:len(self.snakeTails)]
            del self.snakePos[0:len(self.snakePos)]
            return

        for position, tail in zip(self.snakePos, self.snakeTails):
                tail.pos = position

    def eat(self):
        tail = Tail(self.prevPos)
        self.add_widget(tail)
        self.snakeTails.insert(0, tail)
        self.snakePos.append(list(self.prevPos))

    def dead(self):
        print("Try again!")
        self.isDead = True
        self.pos = self.parent.center


class Tail(Widget):
    def __init__(self, position):
        super().__init__()
        self.pos = position


class Food(Widget):
    food = ObjectProperty(0)

    def changeLocation(self):
        wd, hg = Window.size
        location = [random.randrange(0+50, wd-50, scl), random.randrange(0+50, hg-50, scl)]
        self.pos = location
        return location


class SnakeGame(Widget):
    snake = ObjectProperty(0)
    food = ObjectProperty(0)
    score = ObjectProperty(0)

    def __init__(self, **kwargs):
        super(SnakeGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'up' and self.snake.velocity != [0,1*scl] and self.snake.velocity != [0, -1*scl]:
            self.snake.move([0,1*scl])
        elif keycode[1] == 'down' and self.snake.velocity != [0, -1*scl] and self.snake.velocity != [0, 1*scl]:
            self.snake.move([0, -1*scl])
        elif keycode[1] == 'right' and self.snake.velocity != [1*scl, 0] and self.snake.velocity != [-1*scl, 0]:
            self.snake.move([1*scl, 0*scl])
        elif keycode[1] == 'left' and self.snake.velocity != [-1*scl, 0]and self.snake.velocity != [1*scl, 0]:
            self.snake.move([-1*scl, 0])

        return True

    def update(self, dt):
        if self.snake.isDead:
            self.score.text = "0"
            self.snake.isDead = False

        self.snake.move(self.snake.velocity)
        self.snake.moveTail()

        if distance(self.snake.pos, self.food.pos) < scl:
            self.food.changeLocation()
            self.snake.eat()
            self.score.text = str(int(self.score.text) + 1)


class SnakeApp(App):
    def build(self):
        game = SnakeGame()
        Clock.schedule_interval(game.update, 1/8)
        return game


if __name__ == "__main__":
    SnakeApp().run()
