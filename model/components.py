import pygame
import math
from abc import ABC, abstractmethod
from pygame import Surface

from pygame.font import Font

class Component(ABC):
    _x : int
    _y : int
    _visible : bool

    def __init__(self, x, y) -> None:
        self._x = x
        self._y = y
        self._visible = True

    @abstractmethod
    def onclick(self, x, y):
        pass

    @abstractmethod
    def draw(self, window):
        pass

    def set_visible(self, visible):
        self._visible = visible

class Button(Component):
    _text : str
    _width : int
    _height : int
    _color : tuple
    _font : Font
    _intent : int

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

class Label(Component):
    __text : str
    __color : tuple
    __font : Font

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
    
    def onclick(self, x, y):
        return False
    
class CircleButton(Button):
    __radius : int

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

    __img : Surface

    def __init__(self, x, y, img) -> None:
        super().__init__(x, y)
        self.__img = img

    def draw(self, window):
        window.blit(self.__img, (self._x, self._y)) 

    def set_img(self, img):
        self.__img = img

    def onclick(self, x, y):
        return False