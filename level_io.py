import json
from dataclasses import dataclass
from pathlib import Path
from tile import Tile, TileType
from typing import List


@dataclass(frozen=True)
class Level:
    grid: List[List[Tile]]
    walls: int


def tile_from_str(s: str) -> Tile:
    if s.startswith("PORTAL:"):
        color = s.split(":")[1]
        return Tile(TileType.PORTAL, portal_color=color)
    return Tile(TileType[s])


def tile_to_str(tile: Tile) -> str:
    if tile.tile_type == TileType.PORTAL:
        return f"PORTAL:{tile.portal_color}"
    return tile.tile_type.name


def load_level(path: str) -> Level:
    with open(path) as f:
        data = json.load(f)
    grid = [
        [tile_from_str(cell) for cell in row]
        for row in data["grid"]
    ]
    return Level(grid=grid, walls=data["walls"])


def save_level(level: Level, path: str) -> None:
    data = {
        "walls": level.walls,
        "grid": [
            [tile_to_str(tile) for tile in row]
            for row in level.grid
        ]
    }
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
