from math import ceil
import matplotlib.pyplot as plt


def Ut0(x):
    return 3 if x >= 0.5 else 4


def artificial_viscosity(a, b, c, d, n, precision):
    h = (b-a)/n
    epsilon = (0.01/h)**2

    dt = 0.5*h
    k = dt/h
    height = ceil((d-c)/dt)
    width = n-1 + 2*height  # двойная лесенка, т.к. в формуле есть индексы i-1 и i+1
    U = [[0 for w in range(width+1)] for h in range(height+1)]
    X, Y, Z = [], [], []
        
    j = 0
    while j <= height:
        t = c + j*dt

        for i in range(j, (width+1)-j):
            x = a + (i-height)*h

            if t == 0:
                U[j][i] = Ut0(x)

            else:
                U[j][i] = round((1 - k*U[j-1][i] + (1 - epsilon)*k*U[j-1][i-1])*U[j-1][i] - 0.5*dt*epsilon/h*(U[j-1][i+1]**2 - 2*U[j-1][i+1]*U[j-1][i] - U[j-1][i-1]**2), precision+1)
            
            new_dt = abs(h/U[j][i])

            if new_dt < dt:
                dt = 0.5*new_dt
                k = dt/h
                height = ceil((d-c)/dt)
                width = n-1 + 2*height
                U = [[0 for w in range(width+1)] for h in range(height+1)]
                X, Y, Z = [], [], []
                j = -1
                break

            if a <= x <= b:
                X.append(x)
                Y.append(t)
                Z.append(U[j][i])

        j += 1
    
    return [X, Y, Z]


def conservative_method(a, b, c, d, n, precision):
    h = (b-a)/n

    dt = 0.5*h
    height = ceil((d-c)/dt)
    width = n-1 + height  # лесенка, т.к. в формуле есть индекс i-1
    U = [[0 for w in range(width+1)] for h in range(height+1)]
    X, Y, Z = [], [], []

    j = 0
    while j <= height:
        t = c + j*dt

        for i in range(j, width+1):
            x = a + (i-height)*h

            if t == 0:
                U[j][i] = Ut0(x)

            else:
                U[j][i] = round(U[j-1][i] + 0.5*dt/h*(U[j-1][i-1]**2 - U[j-1][i]**2), precision+1)
            
            new_dt = abs(h/U[j][i])

            if new_dt < dt:
                dt = 0.5*new_dt
                height = ceil((d-c)/dt)
                width = n-1 + height
                U = [[0 for w in range(width+1)] for h in range(height+1)] 
                X, Y, Z = [], [], []
                j = -1
                break

            if a <= x <= b:
                X.append(x)
                Y.append(t)
                Z.append(U[j][i])

        j += 1

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
    n = 20
    precision = 2
    
    print("График какого решения вывести? (1, 2)\n1. Метод с искусственной вязкостью\n2. Консервативная схема")
    select = input()

    if select == "1":
        plot3d(artificial_viscosity(a, b, c, d, n, precision))

    elif select == "2":
        plot3d(conservative_method(a, b, c, d, n, precision))

    else:
        print("Такого графика нет!")


if __name__ == "__main__":
    main()
