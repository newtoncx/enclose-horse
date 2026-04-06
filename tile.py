from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional
 
 
class TileType(Enum):
    HORSE = auto()
    GRASS = auto()
    WALL = auto()
    WATER = auto()
    PORTAL = auto()
 
 
@dataclass(frozen=True)
class Tile:
    tile_type: TileType
    portal_color: Optional[str] = None
 
    def __post_init__(self) -> None:
        is_portal = self.tile_type == TileType.PORTAL
 
        if is_portal and not self.portal_color:
            raise ValueError("PORTAL tile requires portal_color")
        if not is_portal and self.portal_color is not None:
            raise ValueError("portal_color only allowed for PORTAL tiles")
 
    def passable(self) -> bool:
        return self.tile_type not in [TileType.WALL, TileType.WATER]
 
    def point_value(self) -> int:
        points_map = {
            TileType.WALL: 0,
            TileType.WATER: 0
        }
        return points_map.get(self.tile_type, 1)
 