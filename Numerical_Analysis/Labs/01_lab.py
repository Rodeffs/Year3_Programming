import matplotlib.pyplot as plt
import numpy as np


def f(x):
    return 2*np.exp(-x)-(x+1)**2


def dfdx(x):
    return -2*np.exp(-x)-2*(x+1)


def d2fdx2(x):
    return 2*np.exp(-x)-2


def error_eval(x, a):
    # Т.к. производная при x > 0 строго убывает, то min(|f'(x)|) на [a, b] будет в точке a
    return abs(f(x)/dfdx(a))


def print_values_table(a, b, n, p):
    h = round((b-a)/n, p)  # шаг
    
    x = np.arange(a, b, h)

    for i in x:
        t = format(round(i, p), f'.{p}f')  # добавляет незначащие нули вплоть до p знака после запятой
        ft = format(round(f(i), p), f'.{p}f')
        print(f"x = {t} | f(x) = {ft}")


def plot_function(a, b, n):
    h = (b-a)/n  # шаг
    
    x = np.arange(a, b, h)
    y = f(x)

    ax = plt.subplot()

    ax.spines[["left", "bottom"]].set_position(("data", 0))  # сдвинуть оси к 0,0
    ax.spines[["top", "right"]].set_visible(False)  # убрать боковые границы
    ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)  # нарисовать стрелку на оси x
    ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)  # нарисовать стреклу на оси y

    ax.plot(x, y, label="y=f(x)")

    ax.set_xlabel("x", loc='right', fontsize=10)
    ax.set_ylabel("y", loc='top', fontsize=10, rotation=0)
    ax.grid(visible=True)
    
    plt.legend()
    plt.show()


# Метод Ньютона

def newton_iteration(x):
    return x - f(x)/dfdx(x)


def newton_method(a, b, p):
    i = 0
    epsilon = 10**-p

    x = a
    if dfdx(b)*d2fdx2(b) > 0:
        x = b
    
    x_next = round(newton_iteration(x), p+1)  # т.к. нужен ещё один знак после запятой
    while (abs(x_next - x) >= epsilon):
        x = x_next
        x_next = round(newton_iteration(x), p+1)
        i += 1
    
    return (x, i, error_eval(x, a))


# Метод хорд

def chord_iteration(x, c):
    return x - f(x)*(c-x)/(f(c)-f(x))


def chord_method(a, b, p):
    i = 0
    epsilon = 10**-p

    x, c = a, b
    if dfdx(b)*d2fdx2(b) > 0:
        x, c = b, a
    
    x_next = round(chord_iteration(x, c), p+1)  # т.к. нужен ещё один знак после запятой
    while (abs(x_next - x) >= epsilon):
        x = x_next
        x_next = round(chord_iteration(x, c), p+1)
        i += 1
    
    return (x, i, error_eval(x, a))


def convert_to_output(answer, p):  # чтобы ничего лишнего не выводить
    solution = format(answer[0], f'.{p}f')  # добавляет незначащие нули вплоть до p знака после запятой
    iter_count = str(answer[1])  
    error = f'{answer[2]:.1g}'  # округляет вплоть до первого ненулевого знака после запятой
    return (solution, iter_count, error)


def main():
    a = 0  # т.к. нужен положительный корень
    b = 10
    n = 10
    p = 7  # до какого знака после запятой округлять
    
    newton_answer = convert_to_output(newton_method(a, b, p), p+1)
    print(f"Метод Ньютона: решение = {newton_answer[0]}, итерации = {newton_answer[1]}, погрешность = {newton_answer[2]}")

    chord_answer = convert_to_output(chord_method(a, b, p), p+1)
    print(f"Метод Хорд: решение = {chord_answer[0]}, итерации = {chord_answer[1]}, погрешность = {chord_answer[2]}")
    
    print("Вывести таблицу значений? (y/N)")
    if input() == 'y':
        print_values_table(a, b, n, p)

    print("Вывести график? (y/N)")
    if input() == 'y':
        plot_function(a, b, n)


if __name__ == "__main__":
    main()
