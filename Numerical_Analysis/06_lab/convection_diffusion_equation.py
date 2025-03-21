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
    dt = h/a*0.5
    k = a*dt/h

    height = int(round(tmax/dt, precision))

    # Строим "лесенку", если x0 != 0

    ladder, offset = 0, 0

    if x0 < 0:
        ladder = height

    elif x0 > 0:
        ladder = min(height, x0/h)

    width = int(round(abs(xmax-x0)/h + ladder, precision))

    U = [[0 for w in range(width+1)] for h in range(height+1)]
    X, Y, Z = [], [], []

    for j in range(height+1):
        t = round(j*dt, precision)
        
        if (x0 < 0 or (x0 > 0 and (tmax-t)/dt < x0/h)) and offset < ladder:
            offset += 1

        for i in range(offset, width+1):
            x = round(x0 - h*(ladder - offset - i), precision)

            if t == 0:
                U[j][i] = Ut0(x)

            elif x0 == x == 0 and a > 0:
                U[j][i] = Ux0(t)

            elif xmax == x == 1 and a < 0:
                U[j][i] = Ux1(t)

            else:
                U[j][i] = k*U[j-1][i-1] + (1-k)*U[j-1][i] + dt*f(x)

            if x0 <= x <= xmax:
                X.append(x)
                Y.append(t)
                Z.append(U[j][i])

    return [X, Y, Z]
            

def lower_left(x0, xmax, tmax, a, h, precision):
    dt = -h/a*0.5
    k = a*dt/h

    height = int(round(tmax/dt, precision))

    ladder, offset = 0, 0

    if xmax > 0:
        ladder = height

    elif xmax < 0:
        ladder = min(height, -xmax/h)

    width = int(round(abs(xmax-x0)/h + ladder, precision))

    U = [[0 for w in range(width+1)] for h in range(height+1)]
    X, Y, Z = [], [], []

    for j in range(height+1):
        t = round(j*dt, precision)
        
        if (xmax > 0 or (xmax < 0 and (tmax-t)/dt < -xmax/h)) and offset < ladder:
            offset += 1

        for i in range(width-offset, -1, -1):
            x = round(xmax + h*(ladder - offset - i), precision)

            if t == 0:
                U[j][i] = Ut0(x)

            elif x0 == x == 0 and a > 0:
                U[j][i] = Ux0(t)

            elif xmax == x == 1 and a < 0:
                U[j][i] = Ux1(t)

            else:
                U[j][i] = (1+k)*U[j-1][i] - k*U[j-1][i+1] + dt*f(x)

            if x0 <= x <= xmax:
                X.append(x)
                Y.append(t)
                Z.append(U[j][i])

    return [X, Y, Z]


def upper_right(x0, xmax, tmax, a, h, precision):  # только при x0 >= 0, иначе при t >= 0 нельзя найти
    dt = h/a*0.5
    k = a*dt/h

    height = int(round(tmax/dt, precision))
    width = int(round(abs(xmax-x0)/h + x0/h, precision))

    U = [[0 for w in range(width+1)] for h in range(height+1)]
    X, Y, Z = [], [], []

    for j in range(height+1):
        t = round(j*dt, precision)
        
        for i in range(width+1):
            x = round(i*h, precision)

            if t == 0:
                U[j][i] = Ut0(x)

            elif x0 == x == 0 and a > 0:
                U[j][i] = Ux0(t)

            elif xmax == x == 1 and a < 0:
                U[j][i] = Ux1(t)

            else:
                U[j][i] = (U[j-1][i] + k*U[j][i-1] + dt*f(x))/(1+k)

            if x0 <= x <= xmax:
                X.append(x)
                Y.append(t)
                Z.append(U[j][i])

    return [X, Y, Z]


def four_corners(x0, xmax, tmax, a, h, precision):  # можно сделать и для x0 < 0, но по условию не требуется
    dt = h/abs(a)*0.5
    k = a*dt/h

    height = int(round(tmax/dt, precision))
    width = int(round(abs(xmax-x0)/h + x0/h, precision))

    U = [[0 for w in range(width+1)] for h in range(height+1)]
    X, Y, Z = [], [], []

    for j in range(height+1):
        t = round(j*dt, precision)
        
        for i in range(width+1):
            x = round(i*h, precision)

            if t == 0:
                U[j][i] = Ut0(x)

            elif x0 == x == 0 and a > 0:
                U[j][i] = Ux0(t)

            elif xmax == x == 1 and a < 0:
                U[j][i] = Ux1(t)

            else:
                U[j][i] = U[j-1][i-1] + ((U[j-1][i] - U[j][i-1]) * (1-k) + 2*dt*f(x+h/2)) / (1+k)

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
