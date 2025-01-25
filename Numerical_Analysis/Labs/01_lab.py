import matplotlib.pyplot as plt
import numpy as np


def f(x):
    return 2*np.exp(-x)-(x+1)**2


def dfdx(x):
    return -2*np.exp(-x)-2*(x+1)


def d2fdx2(x):
    return 2*np.exp(-x)-2


def error_eval(x, a):  # т.к. производная при x >= 0 строго убывает, то min(|f'(x)|) на [a, b] будет в точке a
    return abs(f(x)/dfdx(a))


def print_values_table(a, b, n, p):
    h = round((b-a)/n, p)  # шаг
    
    x = np.arange(a, b+1, h)

    for i in x:
        t = format(round(i, p), f'.{p}f')  # добавляет нули вплоть до p знака после запятой
        ft = format(round(f(i), p), f'.{p}f')
        print(f"x = {t}\tf(x) = {ft}")


def plot_function(a, b, n):
    h = (b-a)/n  # шаг
    
    x = np.arange(a, b, h)
    y = f(x)

    ax = plt.subplot()

    ax.spines[["left", "bottom"]].set_position(("data", 0))  # сдвинуть оси к 0,0
    ax.spines[["top", "right"]].set_visible(False)  # убрать боковые границы
    ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)  # нарисовать стрелку на оси x
    ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)  # нарисовать стреклу на оси y

    ax.plot(x, y, label="y=f(x)")

    ax.set_xlabel("x", loc='right', fontsize=10)
    ax.set_ylabel("y", loc='top', fontsize=10, rotation=0)
    ax.grid(visible=True)
    
    plt.legend()
    plt.show()


# Метод Ньютона

def newton_iteration(x):
    return x - f(x)/dfdx(x)


def newton_method(a, b, p):
    i = 0
    epsilon = 10**-p

    x = a
    if dfdx(b)*d2fdx2(b) > 0:
        x = b
    print(f"i = {i}\tx = {format(x, f'.{p+1}f')}")
    
    x_next = round(newton_iteration(x), p+1)  # т.к. нужен ещё один знак после запятой
    while (abs(x_next - x) >= epsilon):
        x = x_next
        x_next = round(newton_iteration(x), p+1)
        i += 1
        print(f"i = {i}\tx = {format(x, f'.{p+1}f')}")
    
    return (x, i, error_eval(x, a))


# Метод хорд

def chord_iteration(x, c):
    return x - f(x)*(c-x)/(f(c)-f(x))


def chord_method(a, b, p):
    i = 0
    epsilon = 10**-p

    x, c = a, b
    if dfdx(b)*d2fdx2(b) > 0:
        x, c = b, a
    print(f"i = {i}\tx = {format(x, f'.{p+1}f')}")
    
    x_next = round(chord_iteration(x, c), p+1)  # т.к. нужен ещё один знак после запятой
    while (abs(x_next - x) >= epsilon):
        x = x_next
        x_next = round(chord_iteration(x, c), p+1)
        i += 1
        print(f"i = {i}\tx = {format(x, f'.{p+1}f')}")
    
    return (x, i, error_eval(x, a))


# Метод секущих

def secant_method(a, b, p):
    i = 0
    epsilon = 10**-p

    x, x_prev = a, b
    print(f"i = {i}\tx = {format(x, f'.{p+1}f')}")

    x_next = round(chord_iteration(x, x_prev), p+1)  # т.к. нужен ещё один знак после запятой
    while (abs(x_next - x) >= epsilon):
        x_prev = x
        x = x_next
        x_next = round(chord_iteration(x, x_prev), p+1)
        i += 1
        print(f"i = {i}\tx = {format(x, f'.{p+1}f')}")
    
    return (x, i, error_eval(x, a))


# Конечноразностный метод Ньютона

def finite_difference_iteration(x, h):
    return x-h*f(x)/(f(x+h)-f(x))


def finite_difference_method(a, b, p):
    i = 0
    epsilon = 10**-p

    x = (a+b)/2 # начальное приближение
    h = 0.001 # произвольное малое h > 0
    print(f"i = {i}\tx = {format(x, f'.{p+1}f')}")

    x_next = round(finite_difference_iteration(x, h), p+1)  # т.к. нужен ещё один знак после запятой
    while (abs(x_next - x) >= epsilon):
        x = x_next
        x_next = round(finite_difference_iteration(x, h), p+1)
        i += 1
        print(f"i = {i}\tx = {format(x, f'.{p+1}f')}")
    
    return (x, i, error_eval(x, a))


# Метод Стеффенсена

def steffensen_iteration(x):
    return x - f(x)**2/(f(x+f(x))-f(x))

def steffensen_method(a, b, p):
    i = 0
    epsilon = 10**-p

    x = (a+b)/2 # начальное приближение
    print(f"i = {i}\tx = {format(x, f'.{p+1}f')}")

    x_next = round(steffensen_iteration(x), p+1)  # т.к. нужен ещё один знак после запятой
    while (abs(x_next - x) >= epsilon):
        x = x_next
        x_next = round(steffensen_iteration(x), p+1)
        i += 1
        print(f"i = {i}\tx = {format(x, f'.{p+1}f')}")
    
    return (x, i, error_eval(x, a))


# Метод простых итераций

def fixed_point_iteration(x, t):
    return x - t*f(x)


def fixed_point_iteration_method(a, b, p):
    i = 0
    epsilon = 10**-p

    m = b
    if dfdx(a) < dfdx(b):  # т.к. функция строго возрастает/убывает при x>0, то минимум будет на одном из концов
        m = a

    x = (a+b)/2 # начальное приближение
    
    t_max = 2/dfdx(m)
    t = t_max/2  # по условию параметр должен быть t < 2/min(f'(x)), но я решил взять вполовину меньше, чтобы гарантировать условие
    if t_max < 0:
        t = t_max*3/2  # т.к. для отрицательных значений t > tmax/2

    print(f"i = {i}\tx = {format(x, f'.{p+1}f')}")
    
    x_next = round(fixed_point_iteration(x, t), p+1)  # т.к. нужен ещё один знак после запятой
    while (abs(x_next - x) >= epsilon):
        x = x_next
        x_next = round(fixed_point_iteration(x, t), p+1)
        i += 1
        print(f"i = {i}\tx = {format(x, f'.{p+1}f')}")
    
    return (x, i, error_eval(x, a))


def convert_to_output(answer, p):  # чтобы ничего лишнего не выводить
    solution = format(answer[0], f'.{p}f')  # добавляет нули вплоть до p знака после запятой
    iter_count = str(answer[1])  
    error = f'{answer[2]:.1g}'  # округляет вплоть до первого ненулевого знака после запятой
    return (solution, iter_count, error)


def main():
    a = 0  # т.к. нужен положительный корень
    b = 10
    p = 7  # до какого знака после запятой округлять

    print("Функция: 2*exp(-x)-(x+1)^2")    
    print(f'Промежуток: [{a}, {b}]')
    print(f'Точность: до {p} знака после запятой')

    print("\nТаблица значений функции:")
    print_values_table(a, b, 10, p)

    print("\nМетод Ньютона:")
    newton_answer = convert_to_output(newton_method(a, b, p), p+1)
    print(f"Решение: x = {newton_answer[0]}\tИтерации: {newton_answer[1]}\tПогрешность: {newton_answer[2]}")

    print("\nМетод Хорд:")
    chord_answer = convert_to_output(chord_method(a, b, p), p+1)
    print(f"Решение: x = {chord_answer[0]}\tИтерации: {chord_answer[1]}\tПогрешность: {chord_answer[2]}")
    
    print("\nМетод секущих:")
    secant_answer = convert_to_output(secant_method(a, b, p), p+1)
    print(f"Решение: x = {secant_answer[0]}\tИтерации: {secant_answer[1]}\tПогрешность: {secant_answer[2]}")

    print("\nКонечноразностный метод Ньютона:")
    finite_difference_answer = convert_to_output(finite_difference_method(a, b, p), p+1)
    print(f"Решение: x = {finite_difference_answer[0]}\tИтерации: {finite_difference_answer[1]}\tПогрешность: {finite_difference_answer[2]}")

    print("\nМетод простых итераций:")
    fixed_point_iteration_answer = convert_to_output(fixed_point_iteration_method(a, b, p), p+1)
    print(f"Решение: x = {fixed_point_iteration_answer[0]}\tИтерации: {fixed_point_iteration_answer[1]}\tПогрешность: {fixed_point_iteration_answer[2]}")

    print("\nВывести график? (y/N)")
    if input() == 'y':
        plot_function(a, b, 300)


if __name__ == "__main__":
    main()
