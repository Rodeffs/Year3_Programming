import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np


def Ut0(x):
    return x+2+x**2*(1-x)


def Ux0(t):
    return 2


def Ux1(t):
    return 3


def explicit_method(D, a, b, c, d, h, T):
    x = np.arange(a, b + h, h)
    t = np.arange(c, d + T, T)
    height, width = len(t), len(x)

    U = np.zeros((height, width))

    for j in range(height):
        for i in range(width):
            if i == 0:
                U[j][i] = Ux0(t[j])

            elif i == width - 1:
                U[j][i] = Ux1(t[j])

            elif j == 0:
                U[j][i] = Ut0(x[i])

            else:
                l = D*T/(h**2)
                U[j][i] = l*U[j-1][i+1] + (1-2*l)*U[j-1][i] + l*U[j-1][i-1]

    return [x, t, U]


def implicit_method(D, a, b, c, d, h, T):
    x = np.arange(a, b + h, h)
    t = np.arange(c, d + T, T)
    height, width = len(t), len(x)

    U = np.zeros((height, width))

    for j in range(height):  # граничные условия
        U[j][0] = Ux0(t[j])
        U[j][width-1] = Ux1(t[j])

    for i in range(1, width-1):  # начальные условия
        U[0][i] = Ut0(x[i])

    # Далее метод прогонки

    for j in range(1, height):
        # Сначала находим прогоночные коэф. альфа и бета

        alpha = np.zeros(width-1)
        beta = np.zeros(width-1)
        beta[0] = Ux0(t[j])  # ВАЖНО! Иначе всё неправильно

        l = D*T/(h**2)
        A = l
        B = -(1+2*l)
        C = l

        for i in range(1, width-1):
            F = -U[j-1][i]

            alpha[i] = -C/(A*alpha[i-1] + B)
            beta[i] = (F - A*beta[i-1])/(A*alpha[i-1] + B)

        # Потом, начиная с конца, находим все значения U[j][i]

        for i in range(width-2, 0, -1):
            U[j][i] = alpha[i]*U[j][i+1] + beta[i]

    return [x, t, U]

   
def plot3d(points):
    ax = plt.figure().add_subplot(projection="3d")
    X, T = np.meshgrid(points[0], points[1])
    
    ax.plot_surface(X, T, points[2], cmap=cm.magma)
    ax.set_xlabel("x")
    ax.set_ylabel("t")
    ax.set_zlabel("U(x, t)")

    plt.show()


def main():
    a, b = 0, 1
    c, d = 0, 10
    D = 1

    # D*T/h^2 <= 1/2 и погрешность O(T + h^2) должна быть не больше 0.01
    h = 0.05
    T = 0.001

    print("Решение каким методом вывести? (1-2)\n1). Явный метод\n2). Неявный метод\n")
    select = input()

    if select == "1":
        plot3d(explicit_method(D, a, b, c, d, h, T))

    elif select == "2":
        plot3d(implicit_method(D, a, b, c, d, h, T))

    else:
        print("Такого шаблона нет!")


if __name__ == "__main__":
    main()
