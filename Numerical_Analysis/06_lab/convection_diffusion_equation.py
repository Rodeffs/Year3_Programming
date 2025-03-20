import matplotlib.pyplot as plt
import numpy as np


def f(x):
    return 2*x


def Ut0(x):
    return 2*x**2-x-1


def Ux0(t):
    return t**2-t-1


def Ux1(t):
    return t**2-t


def lower_right(x0, xmax, tmax, a, h, precision):
    i, j, t = 0, 0, 0
    dt = h/abs(a)
    k = a*dt/h
    U, X, Y, Z = [], [], [], []

    while t <= tmax:
        Ux = []

        # Строим "лесенку", если x0 != 0
        ladder = 0

        if x0 < 0:
            ladder = round(tmax/dt - t, precision)

        elif x0 > 0:
            ladder = round(min(tmax/dt - t, x0/h), precision)

        x = x0 - h*ladder

        while x <= xmax:
            U_next = 0

            if t == 0:
                U_next = Ut0(x)

            elif x == 0 and a > 0 and x0 == 0:
                U_next = Ux0(t)

            elif x == 1 and a < 0 and x0 == 0:
                U_next = Ux1(t)

            else:
                U_next = k*U[j-1][i-1] + (1-k)*U[j-1][i] + dt*f(x)

            Ux.append(U_next)

            if x >= x0:
                X.append(x)
                Y.append(t)
                Z.append(U_next)
            
            x = round(x + h, precision)
            i += 1

        U.append(Ux)
        t = round(t + dt, precision)
        j += 1
        i -= int(abs(xmax-x0)/h + ladder + 1)

    return [X, Y, Z]
            

def lower_left(x0, xmax, tmax, a, h, precision):
    i, j, t = 0, 0, 0
    dt = h/abs(a)
    k = a*dt/h
    U, X, Y, Z = [], [], [], []

    while t <= tmax:
        Ux = []

        ladder = 0

        if xmax > 0:
            ladder = round(tmax/dt - t, precision)

        elif xmax < 0:
            ladder = round(min(tmax/dt - t, abs(xmax)/h), precision)

        x = xmax + h*ladder

        while x >= x0:
            U_next = 0

            if t == 0:
                U_next = Ut0(x)

            elif x == 0 and a > 0 and x0 == 0:
                U_next = Ux0(t)

            elif x == 1 and a < 0 and x0 == 0:
                U_next = Ux1(t)

            else:
                U_next = (1+k)*U[j-1][i] - k*U[j-1][i-1] + dt*f(x)

            Ux.append(U_next)

            if x <= xmax:
                X.append(x)
                Y.append(t)
                Z.append(U_next)
            
            x = round(x - h, precision)
            i += 1

        U.append(Ux)
        t = round(t + dt, precision)
        j += 1
        i -= int(abs(xmax-x0)/h + ladder + 1)
        print(i)
    
    return [X[::-1], Y, Z]


def upper_right(x0, xmax, tmax, a, h, precision):  # только при x0 >= 0, иначе при t >= 0 нельзя найти
    i, j, t = 0, 0, 0
    dt = h/abs(a)
    k = a*dt/h
    U, X, Y, Z = [], [], [], []

    while t <= tmax:
        Ux = []
        x = 0

        while x <= xmax:
            U_next = 0

            if t == 0:
                U_next = Ut0(x)

            elif x == 0 and a > 0 and x0 == 0:
                U_next = Ux0(t)

            elif x == 1 and a < 0 and x0 == 0:
                U_next = Ux1(t)

            else:
                U_next = (U[j-1][i] + k*Ux[i-1] + dt*f(x))/(1+k)

            Ux.append(U_next)

            if x >= x0:
                X.append(x)
                Y.append(t)
                Z.append(U_next)
            
            x = round(x + h, precision)
            i += 1

        U.append(Ux)
        t = round(t + dt, precision)
        j += 1
        i = 0

    return [X, Y, Z]


def four_corners(x0, xmax, tmax, a, h, precision):  # можно сделать и для x0 < 0, но по условию не требуется
    i, j, t = 0, 0, 0
    dt = h/abs(a)
    k = a*dt/h
    U, X, Y, Z = [], [], [], []

    while t <= tmax:
        Ux = []
        x = 0

        while x <= xmax:
            U_next = 0

            if t == 0:
                U_next = Ut0(x)

            elif x == 0 and a > 0 and x0 == 0:
                U_next = Ux0(t)

            elif x == 1 and a < 0 and x0 == 0:
                U_next = Ux1(t)

            else:
                U_next = U[j-1][i-1] + ((U[j-1][i] - Ux[i-1]) * (1-k) + 2*dt*f(x+h/2)) / (1+k)

            Ux.append(U_next)

            if x >= x0:
                X.append(x)
                Y.append(t)
                Z.append(U_next)
            
            x = round(x + h, precision)
            i += 1

        U.append(Ux)
        t = round(t + dt, precision)
        j += 1
        i = 0

    return [X, Y, Z]


def plot3d(points):
    x = np.array(points[0])
    y = np.array(points[1])
    z = np.array(points[2])

    ax = plt.figure().add_subplot(projection="3d")
    
    ax.plot(x, y, z)
    ax.set_xlabel("x")
    ax.set_ylabel("t")
    ax.set_zlabel("U(x, t)")

    plt.show()


def main():
    print("Какой график вывести? (1-6)\n1. Полуплоскость, правый нижний угол\n2. Полуплоскость, левый нижний угол\n3. Прямоугольник, правый нижний угол\n4. Прямоугольник, левый нижний угол\n5. Прямоугольник, правый верхний угол\n6. Прямоугольник, все 4 угла")

    select = input()

    if select == "1":
        plot3d(lower_right(-5, 5, 15, 2, 0.1, 2))

    elif select == "2":
        plot3d(lower_left(-5, 5, 15, -2, 0.1, 2))

    elif select == "3":
        plot3d(lower_right(0, 1, 10, 2, 0.1, 2))

    elif select == "4":
        plot3d(lower_left(0, 1, 10, -2, 0.1, 2))

    elif select == "5":
        plot3d(upper_right(0, 1, 10, 2, 0.1, 2))

    elif select == "6":
        plot3d(four_corners(0, 1, 10, 2, 0.1, 2))

    else:
        print("Такого графика нет!")


if __name__ == "__main__":
    main()
