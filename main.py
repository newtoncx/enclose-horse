from game import Game
from level_io import load_level


def main() -> int:
    while True:
        name = input("Level name: ").strip()
        if not name:
            print("Please enter a level name.")
            continue
        path = f"levels/{name}.json"
        try:
            level = load_level(path)
            break
        except FileNotFoundError:
            print(f"Level '{name}' not found. Try again.")
        except Exception as e:
            print(f"Error loading level: {e}")

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
