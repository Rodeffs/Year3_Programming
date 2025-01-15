"""
написать программу, которая сканирует текущую папку на графические файлы заданного расширения и если их находит выводит их в виде уменьшенных до размера 50 на 50 картинок
"""

from PIL import Image
from argparse import ArgumentParser
from pathlib import Path


def main():

    parser = ArgumentParser()
    parser.add_argument("-ftype", required=True, help="the filetype to search for")
    parser.add_argument("-dir", default=".", help="dir to scan")

    arg = parser.parse_args()

    # Проверяем все файлы в cwd, если они указанного типа, то уменьшаем их до 50x50 и показываем

    for file in Path(arg.dir).iterdir():
        if file.is_file():
            try:
                with Image.open(file) as img:
                    if img.format == arg.ftype:
                        img.thumbnail((50, 50))
                        img.show()
            except:
                continue


if __name__ == "__main__":
    main()
