from escape_path_finder import EscapePathFinder
from level_io import Level
from render import BackgroundColor, render_grid
from tile import Tile, TileType


# The main game class runs in a loop, repeatedly rendering the current state of the grid and
# prompting the player to place or unplace walls. If the horse can escape, it will show the escape
# path. Otherwise, it will display the enclosed area and show the number of points enclosed.
class Game:
    def __init__(self, level: Level):
        self.running = False
        self.grid = [row[:] for row in level.grid]
        self.walls_remaining = level.walls

    def in_bounds(self, row: int, col: int) -> bool:
        return 0 <= row < len(self.grid) and 0 <= col < len(self.grid[0])

    def place_wall(self, row: int, col: int) -> bool:
        if not self.in_bounds(row, col):
            print(f"Out of bounds. Grid is {len(self.grid)}x{len(self.grid[0])}.")
            return False
        if self.walls_remaining == 0:
            print("No walls left to place.")
            return False
        if self.grid[row][col].tile_type != TileType.GRASS:
            print("Cannot place a wall there.")
            return False
        self.grid[row][col] = Tile(TileType.WALL)
        self.walls_remaining -= 1
        return True

    def unplace_wall(self, row: int, col: int) -> bool:
        if not self.in_bounds(row, col):
            print(f"Out of bounds. Grid is {len(self.grid)}x{len(self.grid[0])}.")
            return False
        if self.grid[row][col].tile_type != TileType.WALL:
            print("No placed wall there.")
            return False
        self.grid[row][col] = Tile(TileType.GRASS)
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
            elif cmd.startswith("place") or cmd.startswith("unplace"):
                parts = cmd.split()
                if len(parts) != 3:
                    print("Usage: place <row> <col> / unplace <row> <col>")
                    continue
                try:
                    row = int(parts[1])
                    if len(parts[2]) != 1 or not parts[2].isalpha():
                        raise ValueError
                    col = ord(parts[2]) - ord('a')
                except ValueError:
                    print("Row must be a number, col must be a single letter.")
                    continue
                if parts[0] == "place":
                    done = self.place_wall(row, col)
                else:
                    done = self.unplace_wall(row, col)
            else:
                print("Unknown command. Try: place 0 b / unplace 0 b / quit")
        print()
