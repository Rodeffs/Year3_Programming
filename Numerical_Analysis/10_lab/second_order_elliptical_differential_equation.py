import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm


def U0(x, y):
    return x + y


def f(x, y):
    return 2*x*(10 - y)


def simple_iteration(a, b, c, d, n, precision):
    h = (b-a)/n

    U = np.zeros((n+1, n+1))
    x = np.arange(a, b + h, h)
    y = np.arange(c, d + h, h)

    for i in range(n+1):
        U[0][i] = U0(x[i], c)
        U[n][i] = U0(x[i], d)

    for j in range(n+1):
        U[j][0] = U0(a, y[j])
        U[j][n] = U0(b, y[j])

    while True:
        U_next = np.zeros((n+1, n+1))

        for i in range(n+1):
            U_next[0][i] = U0(x[i], c)
            U_next[n][i] = U0(x[i], d)

        for j in range(n+1):
            U_next[j][0] = U0(a, y[j])
            U_next[j][n] = U0(b, y[j])

        max_diff = 0

        for j in range(1, n):
            for i in range(1, n):
                U_next[j][i] = 1/4 * (U[j][i+1] + U[j][i-1] + U[j+1][i] + U[j-1][i] - h**2*f(x[i], y[j]))
                U_next[j][i] = round(U_next[j][i], precision+1)

                diff = abs(U_next[j][i] - U[j][i])
                max_diff = max(max_diff, diff)

        if max_diff < 10**-precision:
            return [x, y, U_next]

        np.copyto(U, U_next)



def seidel_method(a, b, c, d, n, precision):
    h = (b-a)/n
    
    U = np.zeros((n+1, n+1))
    x = np.arange(a, b + h, h)
    y = np.arange(c, d + h, h)

    for i in range(n+1):
        U[0][i] = U0(x[i], c)
        U[n][i] = U0(x[i], d)

    for j in range(n+1):
        U[j][0] = U0(a, y[j])
        U[j][n] = U0(b, y[j])

    while True:
        max_diff = 0

        for j in range(1, n):
            for i in range(1, n):
                new_value = 1/4 * (U[j][i+1] + U[j][i-1] + U[j+1][i] + U[j-1][i] - h**2*f(x[i], y[j]))
                new_value = round(new_value, precision+1)

                diff = abs(new_value - U[j][i])
                U[j][i] = new_value

                max_diff = max(max_diff, diff)

        if max_diff < 10**-precision:
            return [x, y, U]


def plot3d(data1, data2):
    fig = plt.figure()
    ax = fig.add_subplot(1, 2, 1, projection="3d")
    X, Y = np.meshgrid(data1[0], data1[1])
    
    ax.plot_surface(X, Y, data1[2], cmap=cm.Reds)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("U(x, y)")
    ax.set_title("Метод простых итераций")

    ax = fig.add_subplot(1, 2, 2, projection="3d")
    ax.plot_surface(X, Y, data2[2], cmap=cm.Blues)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("U(x, y)")
    ax.set_title("Метод Зейделя")

    plt.show()


def main():

    # Стороны должны быть соразмерны
    a, b = 0, 10
    c, d = 0, 10

    precision = 2  # точность знаков после запятой

    print("Введите размер сетки:")
    n = int(input())
    
    plot3d(simple_iteration(a, b, c, d, n, precision), seidel_method(a, b, c, d, n, precision))


if __name__ == "__main__":
    main()
