from pathlib import Path
from glob import glob
from sys import argv

from shutil import copy  # to copy files

def main():

    size_check = 2048  # in bytes
    
    directory = Path('.')
    
    if len(argv) > 1:
        directory = Path(argv[1])

        if not directory.exists():
            print("Error, directory", directory, "was not found")
            return

    file_list = [file for file in directory.glob("*") if file.is_file() and file.stat().st_size < size_check]

    if not file_list:
        print("No files with size <", size_check, "bytes were found")
        return

    Path("./small").mkdir(exist_ok=True)

    for file in file_list:
        print(file)

        copy(file, Path("./small").joinpath(file.name))



if __name__ == "__main__":
    main()
