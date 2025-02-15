from math import sin, cos


def f(x):
    return sin(2*x)**2  # = 1/2 - cos(4*x)/2, так проще считать производные

def df(x):
    return 2*sin(4*x)

def d2f(x):
    return 8*cos(4*x)


def differentiate(a, b, distance, precision):
    h = (b-a)/distance
    x = a

    while x <= b:
        if x == a:
            d_right = round((f(x+h) - f(x)) / h, precision)
            print(f"x = {x}\nf'(x) слева = -\nf'(x) справа = {d_right}\nf'(x) центр = -\nf''(x) = -\nf'(x) точно = {round(df(x), precision)}\nf''(x) точно = {round(d2f(x), precision)}")

        elif x == b:
            d_left = round((f(x) - f(x-h)) / h, precision)
            print(f"x = {x}\nf'(x) слева = {d_left}\nf'(x) справа = -\nf'(x) центр = -\nf''(x) = -\nf'(x) точно = {round(df(x), precision)}\nf''(x) точно = {round(d2f(x), precision)}")

        else:
            d_left = round((f(x) - f(x-h)) / h, precision)
            d_right = round((f(x+h) - f(x)) / h, precision)
            d_mid = round((f(x+h) - f(x-h)) / (2*h), precision)
            d2 = round((f(x+h) - 2*f(x) + f(x-h)) / (h**2), precision)

            print(f"x = {x}\nf'(x) слева = {d_left}\nf'(x) справа = {d_right}\nf'(x) центр = {d_mid}\nf''(x) = {d2}\nf'(x) точно = {round(df(x), precision)}\nf''(x) точно = {round(d2f(x), precision)}")
        
        print()
        x += h


def main():
    a, b = 0, 1
    distance = 5
    precision = 4

    print(f"Функция: sin(2x)^2\nОтрезок: [{a}, {b}]\nКоличество узлов: {distance}")

    print("\nЗначения производных в узлах отрезка:\n")
    
    differentiate(a, b, distance, precision)


if __name__ == "__main__":
    main()
