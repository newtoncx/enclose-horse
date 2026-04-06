from collections import deque
from dataclasses import dataclass
from tile import Tile, TileType
from typing import List, Optional, Tuple
 
 
@dataclass(frozen=True)
class EscapePathFinderResult:
    can_escape: bool
    escape_path: Optional[List[Tuple[int, int]]]
    enclosed_tiles: Optional[List[Tuple[int, int]]]
    enclosed_points: Optional[int]
 
 
class EscapePathFinder:
    def __init__(self, grid: List[List[Tile]]):
        self.grid = grid
 
        self.m = len(self.grid)
        if self.m == 0:
            raise RuntimeError("Grid must be non-empty")
        self.n = len(self.grid[0])
        if self.n == 0:
            raise RuntimeError("Grid must be non-empty")
 
        horse_coordinates = None
        for x in range(self.m):
            for y in range(self.n):
                if grid[x][y].tile_type == TileType.HORSE:
                    if horse_coordinates:
                        raise RuntimeError("Only one horse is allowed")
                    horse_coordinates = (x, y)
        self.start = horse_coordinates
 
    def find(self) -> EscapePathFinderResult:
        bfs_queue = deque()
        bfs_queue.append(self.start)
        reverse_path_keeper = [[None for _ in range(self.n)] for _ in range(self.m)]
        reverse_path_keeper[self.start[0]][self.start[1]] = (-1, -1)
 
        while len(bfs_queue) > 0:
            current = bfs_queue.popleft()
            if self.is_edge_tile(current):
                reversed_escape_path = []
                while current != (-1, -1):
                    reversed_escape_path.append(current)
                    current = reverse_path_keeper[current[0]][current[1]]
                return EscapePathFinderResult(True, reversed_escape_path[::-1], None, None)
 
            for neighbor in self.get_neighbors(current):
                if not self.grid[neighbor[0]][neighbor[1]].passable():
                    continue
                if reverse_path_keeper[neighbor[0]][neighbor[1]] is None:
                    reverse_path_keeper[neighbor[0]][neighbor[1]] = current
                    bfs_queue.append(neighbor)
 
        enclosed_tiles = []
        enclosed_points = 0
        for x in range(self.m):
            for y in range(self.n):
                if reverse_path_keeper[x][y] is not None:
                    enclosed_tiles.append((x, y))
                    enclosed_points += self.grid[x][y].point_value()
 
        return EscapePathFinderResult(False, None, enclosed_tiles, enclosed_points)
 
    def get_neighbors(self, coordinates: Tuple[int, int]) -> bool:
        if self.is_edge_tile(coordinates):
            raise RuntimeError("Should not call get_neighbors() on an edge tile")
        x = coordinates[0]
        y = coordinates[1]
        return [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]
 
    def is_edge_tile(self, coordinates: Tuple[int, int]) -> bool:
        return coordinates[0] == 0 or coordinates[0] == self.m - 1 or coordinates[1] == 0 or coordinates[1] == self.n - 1
