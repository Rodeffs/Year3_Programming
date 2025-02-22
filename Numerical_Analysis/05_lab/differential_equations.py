from math import sin, cos


def dydx(x, y):
    return 1-sin(x+y)


def d2ydx2(x, y):
    return cos(1+x)-0.5*y**2


def copy_array_of_tuples(arr1, arr2):
    arr1.clear()

    for component in arr2:
        copy_component = []

        for elem in component:
            copy_component.append(elem)

        arr1.append(tuple(copy_component))


def euler_cauchy_method(a, b, p):
    epsilon = 10**-p
    n = 4
    h = (b-a)/n
    
    points = [(a, 0)]  # решение
    
    for i in range(1, n+1):  # первая итерация
        x_prev, y_prev = points[-1]
        f = dydx(x_prev, y_prev)
        
        x = x_prev + h
        y_tilda = y_prev + h * f
        y = y_prev + h/2 * (f + dydx(x, y_tilda))
        y = round(y, p+1)  # точнее нет смысла считать

        points.append((x, y))

    while True:
        n *= 2
        h /= 2

        points_2n = [(a, 0)]  # решение с удвоенным разбиением 

        for i in range(1, n+1):  # последующие итерации
            x_prev, y_prev = points_2n[-1]
            f = dydx(x_prev, y_prev)
            
            x = x_prev + h
            y_tilda = y_prev + h * f
            y = y_prev + h/2 * (f + dydx(x, y_tilda))
            y = round(y, p+1)

            points_2n.append((x, y))
        
        # Контролирование вычислений методом двойного пересчёта
        # Т.е. если максимальный модуль разности значений в соответсвующих узлах меньше эпсилон, то решение найдено

        max_diff = 0

        for i in range(n//2+1):
            diff = abs(points_2n[i*2][1] - points[i][1])

            if diff > max_diff:
                max_diff = diff
        
        if max_diff < epsilon:
            return [points, points_2n]  # т.к. нужна ещё предпоследняя итерация

        copy_array_of_tuples(points, points_2n)


def main():
    a, b = 0, 0.5
    precision = 3

    print(f"Уравнение 1: y' = 1-sin(x+y)\nУравнение 2: y'' = cos(1+x)-0.5y^2\nОтрезок: [{a}, {b}]\n")

    euler_prev, euler_last = euler_cauchy_method(a, b, precision)
    
    print("Решение методом Эйлера-Коши (y1 - предпоследняя итерация, y2 - последняя):")
    print("x y2 y1 y2-y1")

    for i in range(len(euler_last)):
        if i % 2 == 0:
            x, y2, y1 = euler_last[i][0], euler_last[i][1], euler_prev[i//2][1]
            print(x, y2, y1, round(y2-y1, precision+1))
        else:
            x, y2= euler_last[i][0], euler_last[i][1]
            print(x, y2)
        


if __name__ == "__main__":
    main()
