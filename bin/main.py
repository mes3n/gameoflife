import pyglet

import random


class Tile:
    def __init__(self, x, y, live, batch):
        self.x, self.y = x, y
        self.live = live

        self.neighbors: list[Tile] = []

        self.shape = pyglet.shapes.Rectangle(x * 9, y * 9, 9, 9, batch=batch)
        self.set_color()
    
    def set_color(self):
        self.shape.color = (255,)*3 if self.live else (0,)*3

    def population(self):
        count = 0
        for t in self.neighbors:
            if t.live:
                count += 1
        return count


class Grid:
    def __init__(self, width, height, batch):
        self.width, self.height = width, height

        self.shape = batch

        self.grid: list[list[Tile]] = [[Tile(x, y, bool(random.getrandbits(1)), batch) for x in range(self.width)] for y in range(self.height)]

        for y, row in enumerate(self.grid):
            for x, tile in enumerate(row):
                if x == 0 or y == 0 or x == width - 1 or y == width - 1:
                    pass
                else:
                    tile.neighbors = [
                        self.grid[y - 1][x - 1],
                        self.grid[y - 1][x],
                        self.grid[y - 1][x + 1],
                        row[x - 1],
                        row[x + 1],
                        self.grid[y + 1][x - 1],
                        self.grid[y + 1][x],
                        self.grid[y + 1][x + 1],
                    ]

    def step(self, *args):
        states = []
        for row in self.grid:
            for tile in row:
                population = tile.population()
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
            self.stepping = True

    def on_key_release(self, symbol, modifiers):
        if symbol == pyglet.window.key.SPACE:
            self.stepping = False


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

    grid = Grid(100, 100, batch)
    window.track(grid)
    # pyglet.clock.schedule_interval(grid.step, 0.2)

    window.start()

if __name__ == '__main__':
    main()