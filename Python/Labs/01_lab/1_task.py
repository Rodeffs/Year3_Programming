from pathlib import Path
from glob import glob
from sys import argv

def main():
    
    directory = Path('.')
    
    if len(argv) > 1:
        directory = Path(argv[1])

    try:
        for elem in directory.iterdir():
            print(elem)

    except Exception:
        print("Error while accessing directory")

    finally:
        return


if __name__ == "__main__":
    main()
