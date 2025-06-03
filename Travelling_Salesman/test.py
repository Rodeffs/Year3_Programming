#from sys import maxsize as ms
ms = 100

import numpy as np


# Класс, который будет хранить каждую ветвь

class Branch:
    def __init__(self, mat, path, bound):
        self._path = path

        self._mat = np.zeros(mat.shape, dtype=np.int64)
        np.copyto(self._mat, mat)

        self._bound = bound

    @property
    def mat(self):
        return self._mat

    @property
    def bound(self):
        return self._bound

    @bound.setter
    def bound(self, value):
        self._bound = value

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value


def calculate_bound(mat):
    n = mat.shape[0]
    values_mat = mat[1:, 1:]

    # Редукция строк

    min_rows = np.min(values_mat, axis=1)

    for i in range(1, n):
        for j in range(1, n):
            if mat[i][j] != ms:
                mat[i][j] -= min_rows[i-1]

    # Редукция столбцов

    min_cols = np.min(values_mat, axis=0)

    for i in range(1, n):
        for j in range(1, n):
            if mat[i][j] != ms:
                mat[i][j] -= min_cols[j-1]

    # Верхняя грань
    
    if ms in min_rows or ms in min_cols:
        return ms

    else:
        return np.sum(min_rows) + np.sum(min_cols)


def calculate_loss(mat):
    # Проводим оценки для нулевых клеток и выбираем ту, которая будет НАИБОЛЬШЕЙ
    
    n = mat.shape[0] 
    src, dst, max_loss = 0, 0, 0
    
    for i in range(1, n):
        for j in range(1, n):
            if mat[i][j] == 0:

                mat[i][j] = ms

                # Минимум по строке, не считая самого элемента

                min_row = np.min(mat[i, 1:])

                # Минимум по столбцу, не считая самого элемента

                min_col = np.min(mat[1:, j])

                loss = 0

                if min_col == ms or min_row == ms:
                    loss = ms

                else:
                    loss = min_col + min_row

                if loss > max_loss:
                    max_loss = loss
                    src, dst = i, j

                print(f"Element {i}, {j}, loss = {loss}")

                mat[i][j] = 0

    return src, dst, max_loss


def main():
    mat = np.array([
        [ 0,  1,  2,  3,  4,  5],
        [ 1, ms, 20, 18, 12,  8],
        [ 2,  5, ms, 14,  7, 11],
        [ 3, 12, 18, ms,  6, 11],
        [ 4, 11, 17, 11, ms, 12],
        [ 5,  5,  5,  5,  5, ms]
        ], dtype=np.int64)

    city_names = ['', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']
    
    final_path, final_bound = [], 0

    # Корень дерева решения

    root = Branch(mat, [], 0)
    
    # Сразу делаем редукцию и находим нижнюю грань

    root.bound = calculate_bound(root.mat)
    
    # Очередь на обработку
    
    queue = [root]

    while True:
        # Из очереди берём ту ветвь, у которой нижняя грань наименьшая

        selected = min(queue, key=lambda x: x.bound)
        queue.remove(selected)

        print(selected.mat)
        print(selected.bound, "\n")

        dst_cities = selected.mat[0]
        src_cities = selected.mat[:, 0]

        # Условие остановки - если остался единственный маршрут

        if selected.mat.shape[0] <= 2:
            selected.path.append((src_cities[1], dst_cities[1]))
            final_path, final_bound = selected.path, selected.bound
            break

        # Делаем оценки и находим маршрут
        
        src, dst, loss = calculate_loss(selected.mat)
        src_city = src_cities[src]
        dst_city = dst_cities[dst]

        # Ветвь, где этот маршрут включён
        
        print("Path", city_names[src_city], "->", city_names[dst_city], "\n")

        # Если обратный маршрут есть, то сразу помечаем его как недостижимый

        try:
            dst_reverse = np.where(dst_cities == src_city)[0][0]
            src_reverse = np.where(src_cities == dst_city)[0][0]
            selected.mat[src_reverse][dst_reverse] = ms

        except:
            pass

        # Делаем редукцию матрицы

        mat = np.zeros(selected.mat.shape, dtype=np.int64)
        np.copyto(mat, selected.mat)

        mat = np.delete(mat, src, 0)
        mat = np.delete(mat, dst, 1)

        # Делаем редукцию строк и столбцов

        new_bound = selected.bound + calculate_bound(mat)

        # Добавляем в очередь ветку, где включили маршрут
        # Здесь нижняя грань - это сумма старой грани и минимумов из редукции

        queue.append(Branch(mat, selected.path + [(src_city, dst_city)], new_bound))

        # Теперь ветвь, где этот маршрут не включён

        # Сначала помечаем маршрут как недостижимый

        selected.mat[src][dst] = ms

        # Затем делаем редукцию строк и столбцов

        calculate_bound(selected.mat)

        print(selected.mat, "\n")

        # Добавляем в очередь ветку, где не включили маршрут
        # Здесь нижняя грань - это сумма старой грани и потери, когда не взяли маршрут

        queue.append(Branch(selected.mat, selected.path, selected.bound + loss))

    print("Длина оптимального пути:", final_bound)
    print("Оптимальный путь:")

    for path in final_path:
        print(city_names[path[0]], "->", city_names[path[1]])


if __name__ == "__main__":
    main()
