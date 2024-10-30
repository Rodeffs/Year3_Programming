import xmlschema
from argparse import ArgumentParser


def main():
    
    parser = ArgumentParser()
    parser.add_argument("-s", required=True, help="the xsd schema to check the files by")
    parser.add_argument("-f", required=True, help="the xml file to check")
    args = parser.parse_args()

    # Загрузка схемы
    sample = xmlschema.XMLSchema(args.s) 

    # Проверка файлов по ней
    if sample.is_valid(args.f):
        print("This xml file is valid")
    else:
        print("This xml file is not valid")


if __name__ == "__main__":
    main()
