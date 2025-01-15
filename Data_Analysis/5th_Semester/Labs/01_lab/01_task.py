from pathlib import Path
from glob import glob
from sys import argv

from shutil import copy  # чтобы копировать файлы

def main():

    size_check = 2048  # размер в байтах
    
    directory = Path('.')  # по дефолту путь - это cwd
    
    if len(argv) > 1:
        directory = Path(argv[1])

        if not directory.exists():  # если указанной папки не существует, то выводим ошибку
            print("Error, directory", directory, "was not found")
            return
    
    # Сама суть программы, сразу добавляет в список файлы размером меньше указанного
    file_list = [file for file in directory.glob("*") if file.is_file() and file.stat().st_size < size_check]

    if not file_list:
        print("No files with size <", size_check, "bytes were found")
        return

    Path("./small").mkdir(exist_ok=True)  # чтобы не было ошибки, если уже существует

    for file in file_list:
        print(file.name)
        copy(file, "./small/" + file.name)


if __name__ == "__main__":
    main()
