import matplotlib.pyplot as plt
import numpy as np


def Ut0(x):
    return 3 if x >= 0.5 else 4


def artificial_viscosity(a, b, c, d, h, dt):
    epsilon = 0.01

    T = np.arange(c, d + dt, dt)
    height = len(T)

    X = np.arange(a - h*(height-1), b + h*height, h) # двойная лесенка, т.к. в формуле есть индексы i-1 и i+1
    width = len(X)

    U = np.zeros((height, width))

    for j in range(height):
        for i in range(j, width-j):
            if T[j] == 0:
                U[j][i] = Ut0(X[i])

            else:
                U[j][i] = U[j-1][i] - dt/h * U[j-1][i] * (U[j-1][i] - U[j-1][i-1]) - epsilon**2 * dt * 0.5 / h**3 * (U[j-1][i+1] - U[j-1][i-1]) * (U[j-1][i+1] - 2 * U[j-1][i] + U[j-1][i-1])

    X = X[height:-height+1]  # срезаем лишние данные
    U = U[:, height:-height+1]

    return [X, T, U]


def conservative_method(a, b, c, d, h, dt):
    T = np.arange(c, d + dt, dt)
    height = len(T)

    X = np.arange(a - h*(height-1), b + h, h) # лесенка, т.к. в формуле есть индексы i-1
    width = len(X)

    U = np.zeros((height, width))

    for j in range(height):
        for i in range(j, width):
            if T[j] == 0:
                U[j][i] = Ut0(X[i])

            else:
                U[j][i] = U[j-1][i] + 0.5*dt/h*(U[j-1][i-1]**2 - U[j-1][i]**2)
            
    X = X[height:]
    U = U[:, height:]

    return [X, T, U]


def plot3d(points):
    ax = plt.figure().add_subplot(projection="3d")
    X, T = np.meshgrid(points[0], points[1])
    
    ax.plot_surface(X, T, points[2])
    ax.set_xlabel("x")
    ax.set_ylabel("t")
    ax.set_zlabel("U(x, t)")

    plt.show()


def main():
    a, b = 0, 1
    c, d = 0, 1
    h = 0.01
    dt = 0.001  # необходимо, чтобы dt <= h/U(x, t)
    
    print("График какого решения вывести? (1, 2)\n1. Метод с искусственной вязкостью\n2. Консервативная схема")
    select = input()

    if select == "1":
        plot3d(artificial_viscosity(a, b, c, d, h, dt))

    elif select == "2":
        plot3d(conservative_method(a, b, c, d, h, dt))

    else:
        print("Такого графика нет!")


if __name__ == "__main__":
    main()
