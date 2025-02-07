import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from argparse import ArgumentParser


def coef(data, swap):  # нахождение коэффициентов регрессионной прямой
    sum_x, sum_y, sum_xy, sum_x2 = 0, 0, 0, 0
    N = len(data)

    for i in range(N):
        x, y = data[i][0], data[i][1]
        if swap:
            x, y = y, x
        
        sum_x += x
        sum_y += y
        sum_xy += x*y
        sum_x2 += x**2

    b = (sum_xy - sum_x*sum_y/N)/(sum_x2 - sum_x**2/N)
    a = (sum_y - b*sum_x)/N

    return (a, b)


def f(x, a, b):
    return a + b*x


def main():
    
    # Считывание параметров

    parser = ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="the csv file to open")
    parser.add_argument("-s", "--swap", action="store_true", help="swap columns used for axis, default: first column - x, second column - y")
    args = parser.parse_args()

    data = pd.read_csv(args.input)
    
    # Вывод статистики

    print("STATS\n")
    print(f"COUNT\n{data.count(axis=0)}\n")
    print(f"MINIMUM\n{data.min(axis=0)}\n")
    print(f"MAXIMUM\n{data.max(axis=0)}\n")
    print(f"MEAN\n{data.mean(axis=0)}\n")

    # Основной код

    np_arr = data.to_numpy()

    a, b = coef(np_arr, args.swap)

    X, Y = data.columns[0], data.columns[1]

    transposed = np.transpose(np_arr)  # чтобы чётко отделить координаты x от y
    values = transposed[0]

    if args.swap:  # т.к. по условию можно выбрать что будет x, а что - y
        X, Y = Y, X
        values = transposed[1]

    # Графики
     
    data.plot(x=X, y=Y, kind="scatter", color="#FF0000")  # точки

    ax = plt.subplot()

    ax.plot(values, f(values, a, b), color="#0000FF")  # регрессионная прямая

    for i in range(len(values)):  # квадраты ошибок
        x = values[i]
        y = transposed[1][i]

        if args.swap:
            y = transposed[0][i]
        
        fx = f(x, a, b)
        side = abs(y - fx)

        # Есть некоторые вопросы:
        #   Из-за того, что x и y могут иметь разный масштаб, на графике квадраты могут стать прямоугольниками
        #   Также непонятно когда точка должна находится слева или справа (когда сверху или снизу - понятно)

        ax.add_patch(Rectangle((x, min(y, fx)), side, side, edgecolor="#DD0000FF", facecolor="#DD0000AA"))
    
    plt.show()


if __name__ == "__main__":
    main()
