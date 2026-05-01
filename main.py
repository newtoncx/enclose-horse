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
