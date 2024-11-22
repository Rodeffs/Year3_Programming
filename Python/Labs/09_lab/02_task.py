import openpyxl


def avg(values):
    total = 0

    for value in values:
        total += value

    return round(total / len(values), 2)


def main():
    wb = openpyxl.load_workbook("salaries.xlsx")
    sheet = wb.active

    workers = [sheet['A2':'I2'][0], sheet['A3':'I3'][0], sheet['A5':'I5'][0], sheet['A6':'I6'][0], sheet['A7':'I7'][0], sheet['A8':'I8'][0], sheet['A10':'I10'][0]]
    
    max_salary_worker = max(workers, key=lambda x:x[8].value)
    print(f"Наибольшая зп: {max_salary_worker[8].value} - {max_salary_worker[1].value}")
    
    min_salary_worker = min(workers, key=lambda x:x[8].value)
    print(f"Наименьшая зп: {min_salary_worker[8].value} - {min_salary_worker[1].value}")

    print("Средняя зп в бухгалтерии:", avg([workers[0][8].value, workers[1][8].value]))
    print("Средняя зп в отделе кадров:", avg([workers[2][8].value, workers[3][8].value, workers[4][8].value, workers[5][8].value]))
    print("Средняя зп в бухгалтерии:", avg([workers[6][8].value]))

    # Что значит вывести наименования с 14 строки? В файле вообще её нет


if __name__ == "__main__":
    main()
