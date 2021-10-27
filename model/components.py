import pygame
import math

class Component:
    _x = 0
    _y = 0
    _visible = True

    def __init__(self, x, y) -> None:
        self._x = x
        self._y = y
        self._visible = True

    def onclick(self, x, y):
        return False

class Button(Component):
    _text = ""
    _width = 0
    _height = 0
    _color = ()
    _font = None
    _intent = 0

    def __init__(self, x, y, width, height, color, font, text, intent) -> None:
        super().__init__(x, y)
        self._width = width
        self._height = height
        self._color = color
        self._font = font
        self._text = text
        self._intent = intent
    
    def onclick(self, x, y):
        return (x >= self._x and x <= self._x + self._width) and (y >= self._y and y <= self._y + self._height) and self._visible

    def draw(self, window):
        if not self._visible: return
        pygame.draw.rect(window, self._color, pygame.Rect(self._x, self._y, self._width, self._height), 2)
        text = self._font.render(self._text, 1, self._color)
        window.blit(text, (self._x + (self._width - text.get_width()) / 2, self._y + (self._height - text.get_height()) / 2))

    def get_text(self):
        return self._text

    def get_intent(self):
        return self._intent

    def set_visible(self, visible):
        self._visible = visible

class Label(Component):
    __text = ""
    __color = ()
    __font = None

    def __init__(self, x, y, color, font, text) -> None:
        super().__init__(x, y)
        self.__color = color
        self.__font = font
        self.__text = text
    
    def draw(self, window):
        if not self._visible: return
        text = self.__font.render(self.__text, 1, self.__color)
        window.blit(text, (self._x, self._y))

    def get_text(self):
        return self.__text
    
class CircleButton(Button):
    __radius = 0

    def __init__(self, x, y, radius, color, font, text, intent) -> None:
        super().__init__(x, y, 0, 0, color, font, text, intent)
        self.__radius = radius
    
    def onclick(self, x, y):
        return (math.sqrt((self._x - x) ** 2 + (self._y - y) ** 2) <= self.__radius) and self._visible

    def draw(self, window):
        if not self._visible: return
        pygame.draw.circle(window, self._color, (self._x, self._y), self.__radius, 2)
        text = self._font.render(self._text, 1, self._color)
        window.blit(text, (self._x - text.get_width() / 2, self._y - text.get_height() / 2))

class Image(Component):

    __img = None

    def __init__(self, x, y, img) -> None:
        super().__init__(x, y)
        self.__img = img

    def draw(self, window):
        window.blit(self.__img, (self._x, self._y)) 

    def set_img(self, img):
        self.__img = img