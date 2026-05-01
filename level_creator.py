from escape_path_finder import EscapePathFinder
from level_io import Level, save_level
from render import BackgroundColor, render_grid
from tile import Tile, TileType

PLACEABLE_TYPES = {
    "water": TileType.WATER,
    "horse": TileType.HORSE,
    "grass": TileType.GRASS
}


class LevelCreator:
    def __init__(self):
        self.grid = None
        self.walls = None

    def prompt_int(self, prompt: str, min_val: int = 1) -> int:
        while True:
            try:
                val = int(input(prompt))
                if val < min_val:
                    print(f"Must be at least {min_val}.")
                else:
                    return val
            except ValueError:
                print("Please enter a whole number.")

    def setup(self):
        rows = self.prompt_int("Grid rows: ")
        cols = self.prompt_int("Grid cols: ")
        self.walls = self.prompt_int("Number of walls: ", min_val=0)
        self.grid = [
            [Tile(TileType.GRASS) for _ in range(cols)]
            for _ in range(rows)
        ]

    def in_bounds(self, row: int, col: int) -> bool:
        return 0 <= row < len(self.grid) and 0 <= col < len(self.grid[0])

    def place(self, row: int, col: int, tile_type: TileType) -> bool:
        if not self.in_bounds(row, col):
            print(f"Out of bounds. Grid is {len(self.grid)}x{len(self.grid[0])}.")
            return False
        self.grid[row][col] = Tile(tile_type)
        return True

    def run(self):
        self.setup()
        self.running = True
        while self.running:
            self.render()
            self.handle_input()
        self.save()

    def render(self):
        render_grid(self.grid, [], None)

    def handle_input(self):
        done = False
        while not done:
            cmd = input("Command: ").strip().lower()
            if cmd == "quit":
                done = True
                self.running = False
            elif cmd.startswith("place"):
                parts = cmd.split()
                if len(parts) != 4:
                    print("Usage: place <row> <col> <type>")
                    continue
                try:
                    row = int(parts[1])
                    col = ord(parts[2]) - ord('a')
                    if len(parts[2]) != 1 or not parts[2].isalpha():
                        raise ValueError
                except ValueError:
                    print("Row must be a number, col must be a single letter.")
                    continue
                tile_type = PLACEABLE_TYPES.get(parts[3])
                if tile_type is None:
                    print(f"Unknown type '{parts[3]}'. Options: {', '.join(PLACEABLE_TYPES)}")
                else:
                    done = self.place(row, col, tile_type)
            else:
                print("Unknown command. Try: place 0 b [water|horse|grass] / quit")
        print()

    def save(self):
        while True:
            path = input("Save level to file: ").strip()
            if not path:
                print("Path cannot be empty.")
                continue
            try:
                save_level(Level(self.grid, self.walls), path)
                print(f"Level saved to {path}")
                break
            except OSError as e:
                print(f"Could not save: {e}")


if __name__ == "__main__":
    level_creator = LevelCreator()
    level_creator.run()
    raise SystemExit(0)
