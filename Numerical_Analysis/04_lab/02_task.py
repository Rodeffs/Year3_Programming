from math import sin, cos


def f(x):
    return sin(2*x)**2  # = 1/2 - cos(4*x)/2, так проще считать производные

def df(x):
    return 2*sin(4*x)

def d2f(x):
    return 8*cos(4*x)


def first_order_error(h):  # погрешность 1 порядка точности равна max(f''(x))/2! * h, где x - точка отрезка [a, b]
    return 4*h


def second_order_error(h):  # погрешность 2 порядка точности равна max(f'''(x))/3! * h^2, где x - точка отрезка [a, b]
    return 32/6*h**2


def differentiate(a, b, h, precision):
    x = a

    print(f"x | f'(x) слева | f'(x) справа | f'(x) центр | f''(x) | f'(x) точно | f''(x) точно")

    while x <= b:
        df_rounded = round(df(x), precision)
        d2f_rounded = round(d2f(x), precision)

        if x == a:
            d_right = round((f(x+h) - f(x)) / h, precision)
            print(x, "--", d_right, "--", "--", df_rounded, d2f_rounded)

        elif x == b:
            d_left = round((f(x) - f(x-h)) / h, precision)
            print(x, d_left, "--", "--", "--", df_rounded, d2f_rounded)

        else:
            d_left = round((f(x) - f(x-h)) / h, precision)
            d_right = round((f(x+h) - f(x)) / h, precision)
            d_mid = round((f(x+h) - f(x-h)) / (2*h), precision)
            d2 = round((f(x+h) - 2*f(x) + f(x-h)) / (h**2), precision)
            print(x, d_left, d_right, d_mid, d2, df_rounded, d2f_rounded)
         
        x = round(x+h, precision)


def main():
    a, b = 0, 1
    precision = 4
    n = 5
    h = round((b-a)/n, precision)

    print(f"Функция: sin(2x)^2\nОтрезок: [{a}, {b}]\nКол-во точек: {n}\n")

    print("Значения производных в узлах отрезка:\n")
    
    differentiate(a, b, h, precision)

    print("\nПогрешность 1 порядка точности:", first_order_error(h))
    print("Погрешность 2 порядка точности:", second_order_error(h))


if __name__ == "__main__":
    main()
