import json
from dataclasses import dataclass
from tile import Tile, TileType
from typing import List

# Utility file for converting levels between two grid representations:
#   (a) Python dataclass with 2D-list of Tile objects
#   (b) JSON string array where each string represents an ASCII encoded grid row

TILE_TO_CHAR = {
    TileType.HORSE: "H",
    TileType.GRASS: ".",
    TileType.WATER: "~"
}

CHAR_TO_TILE = {v: Tile(k) for k, v in TILE_TO_CHAR.items()}


@dataclass(frozen=True)
class Level:
    grid: List[List[Tile]]
    walls: int


def load_level(path: str) -> Level:
    with open(path) as f:
        data = json.load(f)
    grid = [
        [CHAR_TO_TILE.get(ch, Tile(TileType.GRASS)) for ch in row]
        for row in data["grid"]
    ]
    return Level(grid=grid, walls=data["walls"])


def save_level(level: Level, path: str) -> None:
    rows = [
        "".join(TILE_TO_CHAR.get(tile.tile_type, ".") for tile in row)
        for row in level.grid
    ]
    data = {
        "walls": level.walls,
        "grid": rows,
    }
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
