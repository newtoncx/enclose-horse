from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional
 
 
class TileType(Enum):
    HORSE = auto()
    GRASS = auto()
    WALL = auto()
    WATER = auto()
 
 
@dataclass(frozen=True)
class Tile:
    tile_type: TileType
 
    def passable(self) -> bool:
        return self.tile_type not in [TileType.WALL, TileType.WATER]
 
    def point_value(self) -> int:
        points_map = {
            TileType.WALL: 0,
            TileType.WATER: 0
        }
        return points_map.get(self.tile_type, 1)
 