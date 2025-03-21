import matplotlib.pyplot as plt
import numpy as np
from math import ceil


def f(x, t):
    return 2*x


def Ut0(x):
    return 2*x**2-x-1


def Ux0(t):
    return t**2-t-1


def Ux1(t):
    return t**2-t


def lower_right(x0, xmax, tmax, a, h, precision):
    k = 0.5
    dt = h/a*k

    height = ceil(round(tmax/dt, precision))

    # Строим "лесенку", если x0 != 0

    stair, offset = 0, 0

    if x0 < 0:
        stair = height

    elif x0 > 0:
        stair = min(height, x0/h)

    width = ceil(round(abs(xmax-x0)/h + stair, precision))

    U = [[0 for w in range(width+1)] for h in range(height+1)]
    X, Y, Z = [], [], []

    for j in range(height+1):
        t = round(j*dt, precision)
        
        for i in range(offset, width+1):
            x = round(x0 - h*(stair-i), precision)

            if t == 0:
                U[j][i] = Ut0(x)

            elif x0 == x == 0:
                U[j][i] = Ux0(t)

            else:
                U[j][i] = k*U[j-1][i-1] + (1-k)*U[j-1][i] + dt*f(x, t)

            if x0 <= x <= xmax:
                X.append(x)
                Y.append(t)
                Z.append(U[j][i])

        if (x0 < 0 or (x0 > 0 and (tmax-t)/dt < x0/h)) and offset < stair:
            offset += 1

    return [X, Y, Z]
            

def lower_left(x0, xmax, tmax, a, h, precision):
    k = -0.5
    dt = h/a*k

    height = ceil(round(tmax/dt, precision))

    stair, offset = 0, 0

    if xmax > 1:
        stair = height

    elif xmax < 1:
        stair = min(height, (1-xmax)/h)

    width = ceil(round(abs(xmax-x0)/h + stair, precision))

    U = [[0 for w in range(width+1)] for h in range(height+1)]
    X, Y, Z = [], [], []

    for j in range(height+1):
        t = round(j*dt, precision)
        
        for i in range(width-offset, -1, -1):
            x = round(x0 + h*i, precision)

            if t == 0:
                U[j][i] = Ut0(x)

            elif xmax == x == 1:
                U[j][i] = Ux1(t)

            else:
                U[j][i] = (1+k)*U[j-1][i] - k*U[j-1][i+1] + dt*f(x, t)

            if x0 <= x <= xmax:
                X.append(x)
                Y.append(t)
                Z.append(U[j][i])

        if (xmax > 1 or (xmax < 1 and (tmax-t)/dt < (1-xmax)/h)) and offset < stair:
            offset += 1

    return [X, Y, Z]


def upper_right(x0, xmax, tmax, a, h, precision):  # только при x0 >= 0, иначе при t >= 0 нельзя найти
    k = 0.5
    dt = h/a*k

    height = ceil(round(tmax/dt, precision))
    width = ceil(round(abs(xmax-x0)/h + x0/h, precision))

    U = [[0 for w in range(width+1)] for h in range(height+1)]
    X, Y, Z = [], [], []

    for j in range(height+1):
        t = round(j*dt, precision)
        
        for i in range(width+1):
            x = round(i*h, precision)

            if t == 0:
                U[j][i] = Ut0(x)

            elif x0 == x == 0:
                U[j][i] = Ux0(t)

            else:
                U[j][i] = (U[j-1][i] + k*U[j][i-1] + dt*f(x, t))/(1+k)

            if x0 <= x <= xmax:
                X.append(x)
                Y.append(t)
                Z.append(U[j][i])

    return [X, Y, Z]


def four_corners(x0, xmax, tmax, a, h, precision):
    dt = h/abs(a)*0.5
    k = a*dt/h

    height = ceil(round(tmax/dt, precision))
    width = 0

    if a > 0:
        width = ceil(round(abs(xmax-x0)/h + x0/h, precision))

    else:
        width = ceil(round(abs(xmax-x0)/h + (1-xmax)/h, precision))


    U = [[0 for w in range(width+1)] for h in range(height+1)]
    X, Y, Z = [], [], []

    for j in range(height+1):
        t = round(j*dt, precision)

        if a > 0:
            for i in range(width+1):
                x = round(i*h, precision)

                if t == 0:
                    U[j][i] = Ut0(x)

                elif x0 == x == 0:
                    U[j][i] = Ux0(t)

                else:
                    U[j][i] = U[j-1][i-1] + ((U[j-1][i]-U[j][i-1])*(1-k) + 2*dt*f(x-h/2, t+dt/2))/(1+k)

                if x0 <= x <= xmax:
                    X.append(x)
                    Y.append(t)
                    Z.append(U[j][i])

        else:
            for i in range(width, -1, -1):
                x = round(i*h, precision)

                if t == 0:
                    U[j][i] = Ut0(x)

                elif xmax == x == 1:
                    U[j][i] = Ux1(t)

                else:
                    U[j][i] = U[j-1][i+1] + ((U[j-1][i]-U[j][i+1])*(1+k) + 2*dt*f(x-h/2, t+dt/2))/(1-k)

                if x0 <= x <= xmax:
                    X.append(x)
                    Y.append(t)
                    Z.append(U[j][i])


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
        plot3d(lower_right(-1, 2, 10, 2, 0.1, 4))

    elif select == "2":
        plot3d(lower_left(-1, 2, 10, -2, 0.1, 4))

    elif select == "3":
        plot3d(lower_right(0, 1, 10, 2, 0.1, 4))

    elif select == "4":
        plot3d(lower_left(0, 1, 10, -2, 0.1, 4))

    elif select == "5":
        plot3d(upper_right(0, 1, 10, 2, 0.1, 4))

    elif select == "6":
        plot3d(four_corners(0, 1, 10, 2, 0.1, 4))

    else:
        print("Такого графика нет!")


if __name__ == "__main__":
    main()
