import xml.etree.ElementTree as ET


def main():

    # Пример, по которому будем проверять другие xml
    example = ET.parse("ex_1.xml")

    # Создание неправельного файла
    elem1 = ET.Element("migration", {"urlid": "http://www.microsoft.com/migration/1.0/migxmlext/CustomFile"})

     


if __name__ == "__main__":
    main()
