import xml.etree.ElementTree as ET


def main():
    
    # Парсим xml файл
    tree = ET.parse("ex_2.xml")
    root = tree.getroot()

    # Определяем новый элемент
    new_item = ET.Element("Item")

    ET.SubElement(new_item, "ArtName").text = "Сыр косичка"
    ET.SubElement(new_item, "Barcode").text = "2000000000188"
    ET.SubElement(new_item, "QNT").text = "270,20"
    ET.SubElement(new_item, "QNTPack").text = "270,20"
    ET.SubElement(new_item, "Unit").text = "шт"
    ET.SubElement(new_item, "SN1").text = "00000009"
    ET.SubElement(new_item, "SN2").text = "30.10.2024"
    ET.SubElement(new_item, "QNTRows").text = "12"

    # Добавляем новый элемент
    detail = root.find("Detail")
    detail.append(new_item)
    ET.indent(tree, '    ')  # чтобы были отступы слева

    # Пересчитываем все значения
    summ_1, summ_2, summ_rows = 0, 0, 0

    for item in detail.findall("Item"):
        val_1 = item.find("QNT").text
        val_2 = item.find("QNTRows").text

        comma = val_1.index(",")

        summ_1 += int(val_1[:comma])
        summ_2 += int(val_1[comma+1:])
        summ_rows += int(val_2)

    summary = root.find("Summary")
    summary.find("Summ").text = str(summ_1) + "," + str(summ_2)
    summary.find("SummRows").text = str(summ_rows)

    # Записываем:
    tree.write("new.xml", encoding="UTF-8", xml_declaration=True)


if __name__ == "__main__":
    main()
