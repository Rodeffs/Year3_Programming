from argparse import ArgumentParser  # парсить аргументы
from pathlib import Path
from glob import glob


def main():
    
    parser = ArgumentParser()
    
    # Путь к директории, по умолчанию - это cwd
    parser.add_argument("--dirpath", default=".", help="the directory to scan")
    
    # Сами файлы, их может быть сколько угодно
    parser.add_argument("--files", nargs="*", help="the files to check")
    
    # Для хранения переданных аргументов
    args = parser.parse_args()

    # Файлы в указанной папке
    file_list = [file for file in Path(args.dirpath).glob("*") if file.is_file()]

    # Если не даны файлы для проверок, то просто выводим инфу о папке
    if not args.files:
        total_size = 0

        for file in file_list:
            total_size += file.stat().st_size

        print("Total file count =", len(file_list))
        print("Total file size =", total_size, "bytes")

        return
    
    missing_list = []

    file_list = [file.name for file in file_list]  # чтобы избавиться от абсолютных путей

    for file in args.files:
        if file not in file_list:
            missing_list.append(file)
    
    # Запись в файлы
    missing_files = open("missing_files.txt", "w")
    existing_files = open("existing_files.txt", "w")

    try:
        for file in file_list:
            existing_files.write(file + "\n")

        for file in missing_list:
            missing_files.write(file + "\n")
    
    except Exception as exc:
        print(exc)

    finally:
        missing_files.close()
        existing_files.close()

        
if __name__ == "__main__":
    main()

