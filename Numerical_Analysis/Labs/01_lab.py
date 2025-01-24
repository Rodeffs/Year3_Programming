import matplotlib.pyplot as plt
import numpy as np


def f(x):
    return 2*np.exp(-x)-(x+1)**2


def dfdx(x):
    return -2*np.exp(-x)-2*(x+1)


def d2fdx2(x):
    return 2*np.exp(-x)-2


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


def newton_iteration(x):
    return x - f(x)/dfdx(x)


def newton_method(a, b, p):

    i = 0
    epsilon = 10**-p

    x = a

    if dfdx(b)*d2fdx2(b) > 0:
        x = b
    
    x_next = round(newton_iteration(x), p)

    while (abs(x_next - x) >= epsilon):
        x = x_next
        x_next = round(newton_iteration(x), p)
        i += 1

    return (x, i)


def main():

    a = 0  # т.к. нужен положительный корень
    b = 10
    n = 100
    precision = 7  # до какого знака после запятой округлять
    
    # Метод Ньютона

    newton_solution = newton_method(a, b, precision)
    print(f"Метод Ньютона: решение = {newton_solution[0]}, итерации = {newton_solution[1]}")
    
    print("Вывести график? (y/N)")
    if input() is 'y':
        plot_function(a, b, n)


if __name__ == "__main__":
    main()
