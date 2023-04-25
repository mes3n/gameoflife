import pyglet

import random


class Tile:
    def __init__(self, x, y, w, h, live, batch):
        self.x, self.y = x, y
        self.live = live

        self.neighbors: list[Tile] = []

        self.shape = pyglet.shapes.Rectangle(x * w, y * h, w, h, batch=batch)
        self.set_color()
    
    def set_color(self):
        self.shape.color = (255,)*3 if self.live else (0,)*3


class Grid:
    def __init__(self, width, height, tw, th, batch):
        self.width, self.height = width, height

        self.shape = batch

        self.grid: list[list[Tile]] = [[Tile(x, y, tw, th, bool(random.getrandbits(1)), batch) 
            for x in range(self.width)] for y in range(self.height)]

        for y, row in enumerate(self.grid):
            for x, tile in enumerate(row):
                tile.neighbors = [
                    self.grid[y - 1][x - 1] if y - 1 > 0 and x - 1 > 0 else None,
                    self.grid[y - 1][x]     if y - 1 > 0 else None,
                    self.grid[y - 1][x + 1] if y - 1 > 0 and x + 1 < self.width else None,
                    row[x - 1]              if x - 1 > 0 else None,
                    row[x + 1]              if x + 1 < self.width else None,
                    self.grid[y + 1][x - 1] if y + 1 < self.height and x - 1 > 0 else None,
                    self.grid[y + 1][x]     if y + 1 < self.height else None,
                    self.grid[y + 1][x + 1] if y + 1 < self.height and x + 1 < self.width else None,
                ]
                tile.neighbors = [t for t in tile.neighbors if t != None]

    def step(self, *args):
        states = []
        for row in self.grid:
            for tile in row:
                population = [t.live for t in tile.neighbors].count(True)
                if population < 2 or 3 < population:
                    states.append(False)
                elif tile.live:
                    states.append(True)
                elif population == 3:
                    states.append(True)
                else:
                    states.append(False)

        for y, row in enumerate(self.grid):
            for x, tile in enumerate(row):
                tile.live = states[y*self.width + x]
                tile.set_color()

                
    def get_size(self) -> tuple[int, int]:
        return self.width, self.height


class Window(pyglet.window.Window):
    def __init__(self, width, height, caption):
        super(Window, self).__init__(width=width, height=height, caption=caption)

        self.grid: Grid = None

        self.stepping = False

    def track(self, grid):
        self.grid = grid

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            self.close()
        elif symbol == pyglet.window.key.SPACE:
            self.stepping = not self.stepping

    def on_draw(self):
        if self.stepping:
            self.grid.step()

        self.clear()
        self.grid.shape.draw()

    def start(self):
        pyglet.app.run()


def main():
    window = Window(900, 900, "Game of Life")

    batch = pyglet.graphics.Batch()

    grid = Grid(150, 150, 6, 6, batch)
    window.track(grid)

    window.start()

if __name__ == '__main__':
    main()
