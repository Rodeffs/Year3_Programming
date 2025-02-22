from math import sin, cos


def dydx(x, y):
    return 1-sin(x+y)


def d2ydx2(x, y):
    return cos(1+x)-0.5*y**2


def copy_array_of_tuples(arr1, arr2):  # т.к. питон по умолчанию просто ссылку копирует
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


def runge_kutta_method(a, b, p):
    epsilon = 10**-p
    n = 4
    h = (b-a)/n
    
    points = [(a, 0)]  # решение
    
    for i in range(1, n+1):  # первая итерация
        x_prev, y_prev = points[-1]
        
        k1 = dydx(x_prev, y_prev)
        k2 = dydx(x_prev + h/2, y_prev + h/2*k1)
        k3 = dydx(x_prev + h/2, y_prev + h/2*k2)
        k4 = dydx(x_prev + h, y_prev + h*k3)
        
        x = x_prev + h
        y = y_prev + h/6*(k1 + 2*k2 + 2*k3 + k4)
        y = round(y, p+1)

        points.append((x, y))

    while True:
        n *= 2
        h /= 2

        points_2n = [(a, 0)]  # решение с удвоенным разбиением 

        for i in range(1, n+1):  # последующие итерации
            x_prev, y_prev = points_2n[-1]
            
            k1 = dydx(x_prev, y_prev)
            k2 = dydx(x_prev + h/2, y_prev + h/2*k1)
            k3 = dydx(x_prev + h/2, y_prev + h/2*k2)
            k4 = dydx(x_prev + h, y_prev + h*k3)            

            x = x_prev + h
            y = y_prev + h/6*(k1 + 2*k2 + 2*k3 + k4)
            y = round(y, p+1)

            points_2n.append((x, y))
        
        max_diff = 0

        for i in range(n//2+1):
            diff = abs(points_2n[i*2][1] - points[i][1])

            if diff > max_diff:
                max_diff = diff
        
        if max_diff < epsilon:
            return [points, points_2n]  # т.к. нужна ещё предпоследняя итерация

        copy_array_of_tuples(points, points_2n)


def adams_method_order_3(a, b, p):

    # По условию дана функция 2 порядка, значит нужно сделать замену y'=z
    # Тогда имеем:
    # y_i+1 = y_i + h*(23z_i - 16z_i-1 + 5z_i-2)/12
    # z_i+1 = z_i + h*(23z'_i - 16z'_i-1 + 5z'_i-2)/12
    # где z'_i = f(x_i, y_i)
    # Здесь требуется найти значения функции в первых 3 точках для чего используем метод Эйлера 1 порядка точности:
    # y_i+1 = y_i + h*z_i
    # z_i+1 = z_i + h*f(x_i, y_i)

    epsilon = 10**-p
    n = 4
    h = (b-a)/n
    
    points = [(a, 0)]  # решение
    z_points = [1]  # точки z

    for i in range(2):  # ещё 2 точки найдём через метод Эйлера
        x_prev, y_prev = points[-1]
        z_prev = z_points[-1]

        x = x_prev + h
        z = z_prev + h*d2ydx2(x_prev, y_prev)
        y = y_prev + h*z
        y = round(y, p+1)

        z_points.append(z)
        points.append((x, y))

    for i in range(3, n+1):  # первая итерация
        prev_2, prev_1, prev = points[-3:]  # предыдущие 3 координаты
        z_prev_2, z_prev_1, z_prev = z_points[-3:]
        
        x = prev[0] + h
        z = z_prev + h/12*(23*d2ydx2(prev[0], prev[1]) - 16*d2ydx2(prev_1[0], prev_1[1]) + 5*d2ydx2(prev_2[0], prev_2[1]))
        y = prev[1] + h/12*(23*z_prev - 16*z_prev_1 + 5*z_prev_2)
        y = round(y, p+1)

        z_points.append(z)
        points.append((x, y))

    while True:
        n *= 2
        h /= 2

        points_2n = [(a, 0)]  # решение с удвоенным разбиением 
        z_points_2n = [1]  # точки z

        for i in range(2):  # ещё 2 точки найдём через метод Эйлера
            x_prev, y_prev = points_2n[-1]
            z_prev = z_points_2n[-1]

            x = x_prev + h
            z = z_prev + h*d2ydx2(x_prev, y_prev)
            y = y_prev + h*z
            y = round(y, p+1)

            z_points_2n.append(z)
            points_2n.append((x, y))

        for i in range(3, n+1):
            prev_2, prev_1, prev = points_2n[-3:]  # предыдущие 3 точки
            z_prev_2, z_prev_1, z_prev = z_points_2n[-3:]
            
            x = prev[0] + h
            z = z_prev + h/12*(23*d2ydx2(prev[0], prev[1]) - 16*d2ydx2(prev_1[0], prev_1[1]) + 5*d2ydx2(prev_2[0], prev_2[1]))
            y = prev[1] + h/12*(23*z_prev - 16*z_prev_1 + 5*z_prev_2)
            y = round(y, p+1)

            z_points_2n.append(z)
            points_2n.append((x, y))
       
        max_diff = 0

        for i in range(n//2+1):
            diff = abs(points_2n[i*2][1] - points[i][1])

            if diff > max_diff:
                max_diff = diff
        
        if max_diff < epsilon:
            return [points, points_2n]  # т.к. нужна ещё предпоследняя итерация

        copy_array_of_tuples(points, points_2n)

def adams_method_order_4(a, b, p):

    # Принцип аналогичен 3 порядку точности, разве начальных точек больше

    epsilon = 10**-p
    n = 4
    h = (b-a)/n
    
    points = [(a, 0)]  # решение
    z_points = [1]  # точки z

    for i in range(3):
        x_prev, y_prev = points[-1]
        z_prev = z_points[-1]

        x = x_prev + h
        z = z_prev + h*d2ydx2(x_prev, y_prev)
        y = y_prev + h*z
        y = round(y, p+1)

        z_points.append(z)
        points.append((x, y))

    for i in range(4, n+1):  # первая итерация
        prev_3, prev_2, prev_1, prev = points[-4:]
        z_prev_3, z_prev_2, z_prev_1, z_prev = z_points[-4:]
        
        x = prev[0] + h
        z = z_prev + h/24*(55*d2ydx2(prev[0], prev[1]) - 59*d2ydx2(prev_1[0], prev_1[1]) + 37*d2ydx2(prev_2[0], prev_2[1]) - 9*d2ydx2(prev_3[0], prev_3[1]))
        y = prev[1] + h/24*(55*z_prev - 59*z_prev_1 + 37*z_prev_2 - 9*z_prev_3)
        y = round(y, p+1)

        z_points.append(z)
        points.append((x, y))

    while True:
        n *= 2
        h /= 2

        points_2n = [(a, 0)]  # решение с удвоенным разбиением 
        z_points_2n = [1]  # точки z

        for i in range(3):
            x_prev, y_prev = points_2n[-1]
            z_prev = z_points_2n[-1]

            x = x_prev + h
            z = z_prev + h*d2ydx2(x_prev, y_prev)
            y = y_prev + h*z
            y = round(y, p+1)

            z_points_2n.append(z)
            points_2n.append((x, y))

        for i in range(4, n+1):
            prev_3, prev_2, prev_1, prev = points_2n[-4:]
            z_prev_3, z_prev_2, z_prev_1, z_prev = z_points_2n[-4:]
            
            x = prev[0] + h
            z = z_prev + h/24*(55*d2ydx2(prev[0], prev[1]) - 59*d2ydx2(prev_1[0], prev_1[1]) + 37*d2ydx2(prev_2[0], prev_2[1]) - 9*d2ydx2(prev_3[0], prev_3[1]))
            y = prev[1] + h/24*(55*z_prev - 59*z_prev_1 + 37*z_prev_2 - 9*z_prev_3)
            y = round(y, p+1)

            z_points_2n.append(z)
            points_2n.append((x, y))
       
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

    print(f"Уравнение 1: y' = 1-sin(x+y)\nУравнение 2: y'' = cos(1+x)-0.5y^2\nОтрезок: [{a}, {b}]\nТочность: 10^-{precision}\ny({a}) = 0, y'({a}) = 1\n")

    print("Решение методом Эйлера-Коши первого уравнения (y1 - предпоследняя итерация, y2 - последняя):")
    print("i x y2 y1 |y2-y1|")

    euler_prev, euler_last = euler_cauchy_method(a, b, precision)
    for i in range(1, len(euler_last)):
        if i % 2 == 0:
            x, y2, y1 = euler_last[i][0], euler_last[i][1], euler_prev[i//2][1]
            print(i, x, y2, y1, round(abs(y2-y1), precision+1))
        else:
            x, y2 = euler_last[i][0], euler_last[i][1]
            print(i, x, y2, "-", "-")
        
    print("\nРешение методом Рунге-Кутты первого уравнения (y1 - предпоследняя итерация, y2 - последняя):")
    print("i x y2 y1 |y2-y1|")

    runge_prev, runge_last = runge_kutta_method(a, b, precision)
    for i in range(1, len(runge_last)):
        if i % 2 == 0:
            x, y2, y1 = runge_last[i][0], runge_last[i][1], runge_prev[i//2][1]
            print(i, x, y2, y1, round(abs(y2-y1), precision+1))
        else:
            x, y2 = runge_last[i][0], runge_last[i][1]
            print(i, x, y2, "-", "-")

    print("\nРешение методом Адамса (3 порядок точности) второго уравнения (y1 - предпоследняя итерация, y2 - последняя):")
    print("i x y2 y1 |y2-y1|")

    adams3_prev, adams3_last = adams_method_order_3(a, b, precision)
    for i in range(1, len(adams3_last)):
        if i % 2 == 0:
            x, y2, y1 = adams3_last[i][0], adams3_last[i][1], adams3_prev[i//2][1]
            print(i, x, y2, y1, round(abs(y2-y1), precision+1))
        else:
            x, y2 = adams3_last[i][0], adams3_last[i][1]
            print(i, x, y2, "-", "-")

    print("\nРешение методом Адамса (4 порядок точности) второго уравнения (y1 - предпоследняя итерация, y2 - последняя):")
    print("i x y2 y1 |y2-y1|")

    adams4_prev, adams4_last = adams_method_order_4(a, b, precision)
    for i in range(1, len(adams4_last)):
        if i % 2 == 0:
            x, y2, y1 = adams4_last[i][0], adams4_last[i][1], adams4_prev[i//2][1]
            print(i, x, y2, y1, round(abs(y2-y1), precision+1))
        else:
            x, y2 = adams4_last[i][0], adams4_last[i][1]
            print(i, x, y2, "-", "-")


if __name__ == "__main__":
    main()
