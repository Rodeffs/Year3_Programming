from math import ceil
import matplotlib.pyplot as plt


def Ut0(x):
    return 3 if x >= 0.5 else 4


def artificial_viscosity(a, b, c, d, h, dt):
    epsilon = 0.01

    height = ceil((d-c)/dt)
    width = ceil((b-a)/h) + 2*height  # двойная лесенка, т.к. в формуле есть индексы i-1 и i+1

    U = [[0 for w in range(width+1)] for h in range(height+1)]
    X, Y, Z = [], [], []
        
    for j in range(height+1):
        t = c + j*dt

        for i in range(j, (width+1)-j):
            x = a + (i-height)*h

            if t == 0:
                U[j][i] = Ut0(x)

            else:
                U[j][i] = U[j-1][i] - dt/h * U[j-1][i] * (U[j-1][i] - U[j-1][i-1]) - epsilon**2 * dt * 0.5 / h**3 * (U[j-1][i+1] - U[j-1][i-1]) * (U[j-1][i+1] - 2 * U[j-1][i] + U[j-1][i-1])

            if a <= x <= b:
                X.append(x)
                Y.append(t)
                Z.append(U[j][i])
    
    return [X, Y, Z]


def conservative_method(a, b, c, d, h, dt):
    height = ceil((d-c)/dt)
    width = ceil((b-a)/h) + height  # лесенка, т.к. в формуле есть индексы i-1

    U = [[0 for w in range(width+1)] for h in range(height+1)]
    X, Y, Z = [], [], []

    for j in range(height+1):
        t = c + j*dt

        for i in range(j, width+1):
            x = a + (i-height)*h

            if t == 0:
                U[j][i] = Ut0(x)

            else:
                U[j][i] = U[j-1][i] + 0.5*dt/h*(U[j-1][i-1]**2 - U[j-1][i]**2)
            
            if a <= x <= b:
                X.append(x)
                Y.append(t)
                Z.append(U[j][i])

    return [X, Y, Z]


def plot3d(points):
    ax = plt.figure().add_subplot(projection="3d")
    
    ax.plot(points[0], points[1], points[2])
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
