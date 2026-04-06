from game import Game
from level_io import load_level
from tile import Tile, TileType
 
 
def main() -> int:
    level = load_level("levels/01.json")
    game = Game(level)
    game.run()

    return 0
 
 
if __name__ == "__main__":
    raise SystemExit(main())
 
# first a dfs to see if can escape (maybe also show escape path)
# way of printing the grid
# then a way to create a level which would include # walls and allow successively placing them
# then a json creator and loader for making and saving levels
# safeties
#
# keep high score and the position of walls?
# additional features like cherries, bees, portals
# i guess would want an optimal solver so that we can compare scores to optimal
# maybe two horses? and how would scoring work?
# ideally a smoother ui where we can scroll around to place walls instead of entering coordinates
