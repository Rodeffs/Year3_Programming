import matplotlib.pyplot as plt
from numpy import array as arr


def f(x):
    return 2*x


def Ut0(x):
    return 2*x**2-x-1


def Ux0(t):
    return t**2-t-1


def Ux1(t):
    return t**2-t


def lower_right(x0, xmax, tmax, a, h):
    i, j, t = 0, 0, 0
    dt = h/abs(a)
    k = a*dt/h
    U, X, Y, Z = [], [], [], []

    while t < tmax:
        Ux = []

        # Строим "лесенку", если x0 != 0
        ladder = 0

        if x0 < 0:
            ladder = tmax/dt - t

        elif x0 > 0:
            ladder = min(tmax/dt - t, x0/h)

        x = x0 - h*ladder

        while x <= xmax:
            U_next = 0

            if t == 0:
                U_next = Ut0(x)

            elif x == 0:
                U_next = Ux0(t)

            else:
                U_next = k*U[j-1][i-1] + (1-k)*U[j-1][i] + dt*f(x)

            Ux.append(U_next)

            if x >= x0:
                X.append(x)
                Y.append(t)
                Z.append(U_next)
            
            x += h
            i += 1

        U.append(Ux)
        t += dt
        j += 1
        i -= abs(xmax-x0)/h + ladder

    return [X, Y, Z]
            

def lower_left(x0, xmax, tmax, a, h):
    i, j, t = 0, 0, 0
    dt = h/abs(a)
    k = a*dt/h
    U, X, Y, Z = [], [], [], []

    while t < tmax:
        Ux = []

        ladder = 0

        if xmax > 0:
            ladder = tmax/dt - t

        elif xmax < 0:
            ladder = min(tmax/dt - t, abs(xmax)/h)

        x = xmax + h*ladder

        while x >= x0:
            U_next = 0

            if t == 0:
                U_next = Ut0(x)

            elif x == 0:
                U_next = Ux0(t)

            else:
                U_next = (1+k)*U[j-1][i] - k*U[j-1][i-1] + dt*f(x)

            Ux.append(U_next)

            if x <= xmax:
                X.append(x)
                Y.append(t)
                Z.append(U_next)
            
            x -= h
            i += 1

        U.append(Ux)
        t += dt
        j += 1
        i -= abs(xmax-x0)/h + ladder

    return [X, Y, Z]


def upper_right(x0, xmax, tmax, a, h):  # только при x0 >= 0, иначе при t >= 0 нельзя найти
    i, j, t = 0, 0, 0
    dt = h/abs(a)
    k = a*dt/h
    U, X, Y, Z = [], [], [], []

    while t < tmax:
        Ux = []

        ladder = x0/h

        x = x0 - h*ladder

        while x <= xmax:
            U_next = 0

            if t == 0:
                U_next = Ut0(x)

            elif x == 0:
                U_next = Ux0(t)

            else:
                U_next = (U[j-1][i] + k*U[j][i-1] + dt*f(x))/(1+k)

            Ux.append(U_next)

            if x >= x0:
                X.append(x)
                Y.append(t)
                Z.append(U_next)
            
            x += h
            i += 1

        U.append(Ux)
        t += dt
        j += 1
        i = 0

    return [X, Y, Z]


def four_corners(x0, xmax, tmax, a, h):  # можно сделать и для x0 < 0, но по условию не требуется
    i, j, t = 0, 0, 0
    dt = h/abs(a)
    k = a*dt/h
    U, X, Y, Z = [], [], [], []

    while t < tmax:
        Ux = []

        ladder = x0/h

        x = x0 - h*ladder

        while x <= xmax:
            U_next = 0

            if t == 0:
                U_next = Ut0(x)

            elif x == 0:
                U_next = Ux0(t)

            else:
                U_next = U[j-1][i-1] + ((U[j-1][i] - U[j][i-1]) * (1-k) + 2*dt*f(x+h/2)) / (1+k)

            Ux.append(U_next)

            if x >= x0:
                X.append(x)
                Y.append(t)
                Z.append(U_next)
            
            x += h
            i += 1

        U.append(Ux)
        t += dt
        j += 1
        i = 0

    return [X, Y, Z]


def main():
    print("Какой график вывести? (1-6)\n1. Полуплоскость, правый нижний угол\n2. Полуплоскость, левый нижний угол\n3. Прямоугольник, правый нижний угол\n4. Прямоугольник, левый нижний угол\n5. Прямоугольник, правый верхний угол\n 6. Прямоугольник, все 4 угла")

    select = input()

    if select == "1":
        pass

    elif select == "2":
        pass

    elif select == "3":
        pass

    elif select == "4":
        pass

    elif select == "5":
        pass

    elif select == "6":
        pass

    else:
        print("Такого графика нет!")


if __name__ == "__main__":
    main()
