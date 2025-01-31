import openpyxl
from openpyxl import Workbook


def main():
    wb = Workbook()
    sheet = wb.active

    data = [
            [
                { 'Таб. номер': '0002', 'ФИО': 'Петров П.П.', 'Отдел': 'Бухгалтерия', 'Сумма по окладу, руб.': 3913.04, 'Сумма по надбавкам, руб.': 2608.7 },
                { 'Таб. номер': '0005', 'ФИО': 'Васин В. В.', 'Отдел': 'Бухгалтерия', 'Сумма по окладу, руб.': 5934.78, 'Сумма по надбавкам, руб.': 913.04 }
            ],
            [
                { 'Таб. номер': '0001', 'ФИО': 'Иванов И.И.', 'Отдел': 'Отдел кадров', 'Сумма по окладу, руб.': 6000.0, 'Сумма по надбавкам, руб.': 4000.0 },
                { 'Таб. номер': '0003', 'ФИО': 'Сидоров С.С.', 'Отдел': 'Отдел кадров', 'Сумма по окладу, руб.': 5000.0, 'Сумма по надбавкам, руб.': 4500.0 },
                { 'Таб. номер': '0006', 'ФИО': 'Львов Л.Л.', 'Отдел': 'Отдел кадров', 'Сумма по окладу, руб.': 4074.07, 'Сумма по надбавкам, руб.': 2444.44 },
                { 'Таб. номер': '0007', 'ФИО': 'Волков В.В.', 'Отдел': 'Отдел кадров', 'Сумма по окладу, руб.': 1434.78, 'Сумма по надбавкам, руб.': 1434.78 },
            ],
            [
               { 'Таб. номер': '0004', 'ФИО': 'Мишин М.М.', 'Отдел': 'Столовая', 'Сумма по окладу, руб.': 5500.0, 'Сумма по надбавкам, руб.': 3500.0 }
            ]
        ] 
    
    columns = ["Таб. номер", "ФИО", "Отдел", "Сумма по окладу, руб.", "Сумма по надбавкам, руб.", "Сумма зарплаты, руб.", "НДФЛ, %", "Сумма НДФЛ, %", "Сумма к выдаче, руб."]

    sheet.append(columns)

    grand_total1, grand_total2, grand_total3, grand_total4, grand_total5 = 0, 0, 0, 0, 0

    for occupation in data:
        occupation_name, total1, total2, total3, total4, total5 = "", 0, 0, 0, 0, 0

        for entry in occupation:
            occupation_name = entry['Отдел']
            
            # round() необходим, чтобы правильно считать дробную часть, иначе будут погрешности
            entry['Сумма по окладу, руб.'] = round(entry['Сумма по окладу, руб.'], 2)
            entry['Сумма по надбавкам, руб.'] = round(entry['Сумма по надбавкам, руб.'], 2)

            total1 += entry['Сумма по окладу, руб.']
            total2 += entry['Сумма по надбавкам, руб.']

            entry['Сумма зарплаты, руб.'] = round(entry['Сумма по окладу, руб.'] + entry['Сумма по надбавкам, руб.'], 2)
            total3 += entry['Сумма зарплаты, руб.']

            entry['НДФЛ, %'] = 13
            entry['Сумма НДФЛ, %'] = round(entry['Сумма зарплаты, руб.'] * entry['НДФЛ, %'] / 100, 2)
            total4 += entry['Сумма НДФЛ, %']

            entry['Сумма к выдаче, руб.'] = round(entry['Сумма зарплаты, руб.'] - entry['Сумма НДФЛ, %'], 2)
            total5 += entry['Сумма к выдаче, руб.']

            row = list(entry.values())
            sheet.append(row)
        
        grand_total1 += total1
        grand_total2 += total2
        grand_total3 += total3
        grand_total4 += total4
        grand_total5 += total5

        sheet.append(["", "", occupation_name + " Итог", total1, total2, total3, "", total4, total5])
    
    sheet.append(["", "", "Общий итог", grand_total1, grand_total2, grand_total3, "", grand_total4, grand_total5])

    wb.save("salaries.xlsx")


if __name__ == "__main__":
    main()
