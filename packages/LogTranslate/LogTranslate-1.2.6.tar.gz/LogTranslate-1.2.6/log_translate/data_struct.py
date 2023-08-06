from enum import Enum

from typer.colors import RED, BLACK, GREEN, MAGENTA

dot = "▫️"


class Level(Enum):
    d = 0
    i = 1
    w = 2
    e = 3

    def color(self):
        # return self.value
        # match self.value:
        #     case 0:
        #         return BLACK
        #     case 1:
        #         return GREEN
        #     case 2:
        #         return MAGENTA
        #     case 3:
        #         return RED
        if self.value == 0:
            return BLACK
        if self.value == 1:
            return GREEN
        if self.value == 2:
            return MAGENTA
        if self.value == 3:
            return RED


class Log(object):
    def __init__(self, time="", process="", origin="", translated="", level: Level = Level.d, type=""):
        self.time = time
        self.process = process
        self.origin = origin
        self.translated = translated
        self.level = level
        self.type = type

    def __str__(self):
        return f"{self.time} {dot} {self.process} {dot} {self.translated}"

    def str_with_origin(self):
        show = f"{self.time} {dot} {self.process} {dot} {self.translated}\n{self.origin}"
        return show


if __name__ == '__main__':
    print(Level.d.value)
    print(Level(Level.d))
    print(Level(3))
