from math import sin, factorial


def f(x):
    return sin(2*x)


def lagrange_polynomial(x, points):
    n = len(points)
    polynomial = 0

    for i in range(n):
        value = f(points[i])

        for j in range(n):
            if j == i:
                continue

            value *= (x-points[j])/(points[i]-points[j])

        polynomial += value

    return polynomial

   
def lagrange_polynomial_error(x, points):
    n = len(points)

    # 4 производная от f равна 16sin(2x)
    # На отрезке [0.10, 0.25] её максимальное по модулю значение будет в точке 0.25

    error = 16*sin(2*0.25)/factorial(n)

    for i in range(n):
        error *= abs(x-points[i])

    return error


def absolute_error(y_approx, y):
    return abs(y - y_approx)


def main():
    points = [0.10, 0.15, 0.20, 0.25]
    precision = 5
    x = 0.22

    print("Данная функия: y = sin(2x)")
    print("Точки отрезка:", points)

    print("\nЗначения в точках отрезка:")
    for i in points:
        print(f"    x = {i}\tf(x) = {round(f(i), precision)}")
    
    y = f(x)
    y_approx = lagrange_polynomial(x, points)

    print(f"\nЗначения в заданной точке x = {x}:")
    print("    Аналитически:", y)
    print("    Через многочлен Лагранжа:", y_approx)
    
    print("\nПогрешность формулы Лагранжа:", f"{lagrange_polynomial_error(x, points):0.1g}")
    print("\nАбсолютная погрешность вычислений:", f"{absolute_error(y_approx, y):0.1g}")


if __name__ == "__main__":
    main()
