from enum import Enum, auto
from tile import Tile, TileType
from typing import List, Optional, Tuple
 
 
class TextColor(Enum):
    GREEN = auto()
    WHITE = auto()
    BLUE = auto()
 
 
class BackgroundColor(Enum):
    RED = auto()
    YELLOW = auto()


def render_grid(grid: List[List[Tile]], highlighted: List[Tuple[int, int]], highlight_color: Optional[BackgroundColor]):
    tile_chars = {
        TileType.HORSE: "H",
        TileType.GRASS: "_",
        TileType.WALL: "#",
        TileType.WATER: "W"
    }
    tile_colors = {
        TileType.HORSE: TextColor.WHITE,
        TileType.GRASS: TextColor.GREEN,
        TileType.WALL: TextColor.WHITE,
        TileType.WATER: TextColor.BLUE
    }
    highlighted_set = set(highlighted or [])
 
    print(" ".join(['  ' if i == -1 else chr(ord('a') + i) for i in range(-1, len(grid[0]))]))
    for x, row in enumerate(grid):
        row_output = [str(x) + (' ' if x < 10 else '')]
        for y, tile in enumerate(row):
            coordinates = (x, y)
            if coordinates in highlighted_set:
                row_output.append(colorize(tile_chars[tile.tile_type], tile_colors[tile.tile_type], highlight_color))
            else:
                row_output.append(colorize(tile_chars[tile.tile_type], tile_colors[tile.tile_type]))
        print(" ".join(row_output))
 

def colorize(ch: str, text_color: TextColor, background_color: Optional[BackgroundColor] = None) -> str:
    RESET = "\033[0m"
    text_color_codes = {
        TextColor.GREEN: "\033[32m",
        TextColor.WHITE: "\033[37m",
        TextColor.BLUE: "\033[34m"
    }
    background_color_codes = {
        BackgroundColor.RED: "\033[41m",
        BackgroundColor.YELLOW: "\033[43m"
    }
    return f"{background_color_codes[background_color] if background_color else ''}{text_color_codes[text_color]}{ch}{RESET}"
