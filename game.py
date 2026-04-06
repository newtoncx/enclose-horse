from escape_path_finder import EscapePathFinder
from level_io import Level
from render import BackgroundColor, render_grid
from tile import Tile, TileType


class Game:
    def __init__(self, level: Level):
        self.running = False
        self.grid = level.grid
        self.walls_remaining = level.walls

    def place_wall(self, row: int, col: int) -> bool:
        if self.walls_remaining == 0:
            print("No walls left to place.")
            return False
        current_tile = self.grid[row][col]
        if current_tile.tile_type != TileType.GRASS:
            print("Cannot place a wall there.")
            return False

        new_tile = Tile(TileType.WALL)
        self.grid[row][col] = new_tile
        self.walls_remaining -= 1
        return True

    def unplace_wall(self, row: int, col: int) -> bool:
        current_tile = self.grid[row][col]
        if current_tile.tile_type != TileType.WALL:
            print("No placed wall there.")
            return False

        new_tile = Tile(TileType.GRASS)
        self.grid[row][col] = new_tile
        self.walls_remaining += 1
        return True

    def run(self):
        self.running = True
        while self.running:
            self.render()
            self.handle_input()

    def render(self):
        render_grid(self.grid, [], None)

        finder = EscapePathFinder(self.grid)
        finder_result = finder.find()
        if finder_result.can_escape:
            print("Horse will escape along this path:")
            render_grid(self.grid, finder_result.escape_path, BackgroundColor.RED)
        else:
            print(f"Currently enclosed points: {finder_result.enclosed_points}")
            render_grid(self.grid, finder_result.enclosed_tiles, BackgroundColor.YELLOW)

        print(f"Walls remaining: {self.walls_remaining}")

    def handle_input(self):
        done = False
        while not done:
            cmd = input("Command: ").strip().lower()
            if cmd == "quit":
                done = True
                self.running = False
            elif cmd.startswith("place"):
                _, row, col = cmd.split()
                done = self.place_wall(int(row), ord(col) - ord('a'))
            elif cmd.startswith("unplace"):
                _, row, col = cmd.split()
                done = self.unplace_wall(int(row), ord(col) - ord('a'))
            else:
                print("Unknown command. Try: place 0 b / unplace 0 b / quit")
        print()
