from argparse import ArgumentParser  # парсить аргументы
from pathlib import Path


def main():
    
    parser = ArgumentParser()
    
    # Путь к директории, по умолчанию - это cwd
    parser.add_argument("--dirpath", default=".", help="the directory where files will be created")
    
    # В условии не сказано, но по дефолту ищем список несуществующих файлов в cwd
    parser.add_argument("--missing", default="./missing_files.txt", help="the missing files to create")

    # Для хранения переданных аргументов
    args = parser.parse_args()

    if not Path(args.missing).exists():
        print("Error, can't find missing files")
        return

    # Считываем информацию о несуществующих файлах
    missing_files = open(args.missing)

    # Создаём эти файлы
    try:
        missing_list = missing_files.read().split()

        for file in missing_list:
            Path(args.dirpath).joinpath(file).touch()

    except Exception as exc:
        print(exc)

    finally:
        missing_files.close()

        
if __name__ == "__main__":
    main()

