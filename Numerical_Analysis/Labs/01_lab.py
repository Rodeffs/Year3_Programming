import matplotlib.pyplot as plt
import numpy as np


def f(x):
    return 2*np.exp(-x)-(x+1)**2


def main():
    
    # Границы и шаг

    a = -5
    b = 10
    n = 100
    step = (b-a)/n
    
    # Задаём x и y

    x = np.arange(a, b, step)
    y = f(x)

    ax = plt.subplot()

    # Рисуем оси абсцисс и ординат

    ax.spines[["left", "bottom"]].set_position(("data", 0))
    ax.spines[["top", "right"]].set_visible(False)
    ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
    ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)

    # Вывод

    ax.plot(x, y)

    ax.set_xlabel("x", loc='right', fontsize=10)
    ax.set_ylabel("y", loc='top', fontsize=10, rotation=0)
 
    plt.show()


if __name__ == "__main__":
    main()
