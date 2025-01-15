import xml.etree.ElementTree as ET


def main():
    # Linux не отображает русские буквы в кодировке windows по очевидным причинам

    tree = ET.parse("ex_3.xml")
    root = tree.getroot()

    for item in root.findall("Документ/ТаблСчФакт/СведТов"):
        print(f"НАИМЕНОВАНИЕ ТОВАРА: {item.get("НаимТов")}; КОЛИЧЕСТВО ТОВАРА:{item.get("КолТов")}; ЦЕНА ТОВАРА: {item.get("ЦенаТов")}")


if __name__ == "__main__":
    main()
