from math import sqrt


def f(x):
    return x*sqrt(x**2-1)


def F(x):
    return sqrt((x**2-1)**3)/3


def left_rectangle_method(a, b, p):
    n = 4
    h = (b-a)/n
    epsilon = 10**-p
    integral = 0

    for i in range(n):
        integral += h*f(a+i*h)

    while True:
        n *= 2
        h /= 2
        integral_2n = 0

        for i in range(n):
            integral_2n += h*f(a+i*h)

        if abs(integral_2n - integral) < epsilon:
            return (round(integral_2n, p+1), h, n)
        
        integral = integral_2n


def right_rectangle_method(a, b, p):
    n = 4
    h = (b-a)/n
    epsilon = 10**-p
    integral = 0

    for i in range(1, n+1):
        integral += h*f(a+i*h)

    while True:
        n *= 2
        h /= 2
        integral_2n = 0

        for i in range(1, n+1):
            integral_2n += h*f(a+i*h)

        if abs(integral_2n - integral) < epsilon:
            return (round(integral_2n, p+1), h, n)

        integral = integral_2n


def mid_rectangle_method(a, b, p):
    n = 4
    h = (b-a)/n
    epsilon = 10**-p
    integral = 0

    for i in range(n):
        integral += h*f(a+h/2+i*h)

    while True:
        n *= 2
        h /= 2
        integral_2n = 0

        for i in range(n):
            integral_2n += h*f(a+h/2+i*h)

        if abs(integral_2n - integral) < epsilon:
            return (round(integral_2n, p+1), h, n)

        integral = integral_2n


def trapezoid_method(a, b, p):
    n = 4
    h = (b-a)/n
    epsilon = 10**-p
    integral = (f(a)+f(b))*h/2

    for i in range(1, n):
        integral += h*f(a+i*h)

    while True:
        n *= 2
        h /= 2
        integral_2n = (f(a)+f(b))*h/2

        for i in range(1, n):
            integral_2n += h*f(a+i*h)

        if abs(integral_2n - integral) < epsilon:
            return (round(integral_2n, p+1), h, n)

        integral = integral_2n


def simpson_method(a, b, p):
    n = 4
    h = (b-a)/n
    epsilon = 10**-p
    integral = (f(a)+f(b))*h/3

    for i in range(1, n):
        integral += (2**(1+i%2))*f(a+i*h)*h/3  # слегка переписал формулу

    while True:
        n *= 2
        h /= 2
        integral_2n = (f(a)+f(b))*h/3

        for i in range(1, n):
            integral_2n += (2**(1+i%2))*f(a+i*h)*h/3

        if abs(integral_2n - integral) < epsilon:
            return (round(integral_2n, p+1), h, n)

        integral = integral_2n


def relative_error(approximate, precise):
    return 100*abs((precise - approximate)/precise)


def main():
    a, b = 1, 2
    p = 4  # до какого знака после запятой считать
    precise = round(F(b)-F(a), p+1)
    
    print(f"Функция: x*sqrt(x^2-1)\nОтрезок: [{a}, {b}]\nТочность: 10^-{p}\nТочное значение интеграла: {precise}\n")
    print("Формат вывода:\nприближённое значение; величина последнего шага; количество точек разбиения; относительная погрешность")

    I1, h1, n1 = left_rectangle_method(a, b, p)
    print("\nМетод левых прямоугольников")
    print(I1, h1, n1, f"{relative_error(I1, precise):.1g}%")

    I2, h2, n2 = right_rectangle_method(a, b, p)
    print("\nМетод правых прямоугольников")
    print(I2, h2, n2, f"{relative_error(I1, precise):.1g}%")

    I3, h3, n3 = mid_rectangle_method(a, b, p)
    print("\nМетод центральных прямоугольников")
    print(I3, h3, n3, f"{relative_error(I1, precise):.1g}%")

    I4, h4, n4 = trapezoid_method(a, b, p)
    print("\nМетод трапеций")
    print(I4, h4, n4, f"{relative_error(I1, precise):.1g}%")

    I5, h5, n5 = simpson_method(a, b, p)
    print("\nМетод Симпсона")
    print(I5, h5, n5, f"{relative_error(I1, precise):.1g}%")


if __name__ == "__main__":
    main()
