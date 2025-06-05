import numpy as np
import copy
import time
from random import uniform
ms = np.iinfo(np.int32).max


class Branch: # Класс, который будет хранить каждую ветвь
    def __init__(self, mat, path, bound):
        self._path = copy.deepcopy(path)  # нужно именно полностью скопировать
        self._mat = np.zeros(mat.shape, dtype=np.int32)
        np.copyto(self._mat, mat)
        self._bound = bound

    @property
    def mat(self):
        return self._mat

    @mat.setter
    def mat(self, value):
        self._mat = value

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


def print_mat(mat):  # для отладок
    for i in range(mat.shape[0]):
        output = ""

        for j in range(mat.shape[1]):
            value = mat[i][j]

            if value < 10:
                output += " " + str(value) + " "

            elif value < ms:
                output += str(value) + " "

            else:
                output += " ∞ "

        print(output)

    print()


def calculate_bound(mat):
    values_mat = mat[1:, 1:]

    # Редукция строк

    min_rows = np.min(values_mat, axis=1)

    for i in range(1, mat.shape[0]):
        for j in range(1, mat.shape[1]):
            if mat[i][j] != ms:
                mat[i][j] -= min_rows[i-1]
    
    # Редукция столбцов

    min_cols = np.min(values_mat, axis=0)

    for i in range(1, mat.shape[0]):
        for j in range(1, mat.shape[1]):
            if mat[i][j] != ms:
                mat[i][j] -= min_cols[j-1]

    # Верхняя грань

    if ms in min_rows or ms in min_cols:
        return ms

    row_sum = np.sum(min_rows)
    col_sum = np.sum(min_cols)

    if row_sum >= ms or col_sum >= ms:
        return ms

    total_sum = row_sum + col_sum
    
    if total_sum >= ms:
        return ms

    return total_sum


def calculate_loss(mat):
    # Проводим оценки для нулевых клеток и выбираем ту, которая будет НАИБОЛЬШЕЙ
    
    src, dst, max_loss = 0, 0, 0
    
    for i in range(1, mat.shape[0]):
        for j in range(1, mat.shape[1]):
            if mat[i][j] == 0:
                # Не считаем сам элемент при подсчёте минимумов

                mat[i][j] = ms

                min_in_row = np.min(mat[i, 1:])
                min_in_col = np.min(mat[1:, j])

                loss = 0

                if min_in_col >= ms or min_in_row >= ms:
                    loss = ms

                else:
                    loss = min_in_col + min_in_row

                if loss >= max_loss:
                    max_loss = loss
                    src, dst = i, j

                mat[i][j] = 0

    return src, dst, max_loss


def sort_path(unsorted_path):  # сортировка путей
    sorted_path = []
    n = len(unsorted_path)

    # Пример: был путь [[(A, B), (B, C)], [(D, E), (E, F), (F, G)]]. Добавили элемент [(C, D)]. Стало [[(A, B), (B, C)], [(D, E), (E, F), (F, G)], [(C, D)]]. По итогу должно получиться [[(A, B), (B, C), (C, D), (D, E), (E, F), (F, G)]]

    while n > 0:
        full_path = unsorted_path[0]
        start, end = full_path[0][0], full_path[-1][1]
        unsorted_path.pop(0)
        n -= 1 
        i = 0

        while i < n:
            cur_path = unsorted_path[i]
            cur_start, cur_end = cur_path[0][0], cur_path[-1][1]

            if cur_end == start:
                full_path = cur_path + full_path
                start = cur_start
                unsorted_path.pop(i)
                n -= 1 
                i = 0

            elif cur_start == end:
                full_path = full_path + cur_path
                end = cur_end
                unsorted_path.pop(i)
                n -= 1 
                i = 0

            else:
                i += 1

        sorted_path.append(full_path)

    return sorted_path


def remove_cycle(branch):  # избегание подциклов
    # Иными словами, делаем недостижимым путь, ведущий из конечного города пути в начальный

    dst_cities = branch.mat[0]
    src_cities = branch.mat[:, 0]

    if branch.mat.shape[0] <= 2:
        return

    for path in branch.path:
        cycle_start, cycle_end = path[0][0], path[-1][1]

        try:
            dst_reverse = np.where(dst_cities == cycle_start)[0][0]
            src_reverse = np.where(src_cities == cycle_end)[0][0]
            branch.mat[src_reverse][dst_reverse] = ms

        except:
            pass


def bounds_branches(mat):
    final_path, final_bound = [], 0
        
    # Корень дерева решения

    root = Branch(mat, [], 0)
    
    # Сразу делаем редукцию и находим нижнюю грань

    root.bound = calculate_bound(root.mat)
    
    queue = [root]

    while True:
        # Из очереди берём ту ветвь, у которой нижняя грань наименьшая

        selected = min(queue, key=lambda x: x.bound)
        queue.remove(selected)

        dst_cities = selected.mat[0]
        src_cities = selected.mat[:, 0]

        # Условие остановки - если остался единственный маршрут

        if selected.mat.shape[0] <= 2:
            selected.path.append([(src_cities[1], dst_cities[1])])
            selected.path = sort_path(selected.path)
            final_path, final_bound = selected.path[0], selected.bound
            break

        # Делаем оценки и находим маршрут
        
        src, dst, loss = calculate_loss(selected.mat)

        # Рассмотрим ветвь, где этот маршрут включён

        with_path = Branch(selected.mat, selected.path, selected.bound)

        # Добавляем этот путь
        
        with_path.path.append([(src_cities[src], dst_cities[dst])])
        with_path.path = sort_path(with_path.path)

        # Делаем редукцию матрицы

        with_path.mat = np.delete(with_path.mat, src, 0)
        with_path.mat = np.delete(with_path.mat, dst, 1)

        # Проверяем на подциклы и удаляем их, если они есть

        remove_cycle(with_path)

        # Делаем редукцию строк и столбцов
        # Здесь нижняя грань - это сумма старой грани и минимумов из редукции
        
        new_bound = calculate_bound(with_path.mat)
        
        if new_bound >= ms or selected.bound >= ms:
            with_path.bound = ms

        else:
            with_path.bound = selected.bound + new_bound

        # Добавляем в очередь ветку, где включили маршрут

        queue.append(with_path)

        # Теперь рассмотрим ветвь, где этот маршрут не включён

        without_path = Branch(selected.mat, selected.path, selected.bound)

        # Сначала помечаем маршрут как недостижимый

        without_path.mat[src][dst] = ms

        # Затем делаем редукцию строк и столбцов
        # Здесь нижняя грань - это сумма старой грани и потери, когда не взяли маршрут

        calculate_bound(without_path.mat)

        if selected.bound >= ms or loss >= ms:
            without_path.bound = ms

        else:
            without_path.bound = selected.bound + loss

        # Добавляем в очередь ветку, где не включили маршрут

        queue.append(without_path)

    return final_path, final_bound


def main():

    """
    # Асимметричная задача

    mat = np.array([
        [ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10],
        [ 1, ms, 16, 93, 82, 59, 17, 72, 84, 43, 28],
        [ 2, 91, ms, 78, 92, 84, 35, 55, 57, 11, 25],
        [ 3, 79, 96, ms, 69, 53, 85, 24,  5, 32, 43],
        [ 4, 92, 43, 62, ms, 33, 99, 81, 46, 34, 39],
        [ 5, 23, 83, 93, 80, ms, 36, 31, 94, 12, 28],
        [ 6, 82, 37, 19, 88,  2, ms, 14, 75, 67, 61],
        [ 7, 22,  6, 89, 64, 63, 33, ms, 34, 35, 99],
        [ 8, 31, 26, 78, 87, 42, 29, 35, ms, 40, 24],
        [ 9, 42, 54, 43, 45,  1, 61, 32, 99, ms, 60],
        [10, 33, 24, 15,  6, 90, 20, 60,  7, 58, ms],
        ], dtype=np.int32)
    """

    # Исходная задача

    mat = np.array([
        [ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        [ 1, ms, 82, ms, 87, ms, ms, ms, ms, ms, ms, ms, ms, ms, ms, ms, ms, ms, ms,  2, 12],
        [ 2, 82, ms, 70, 47, ms, ms, ms, ms, ms, ms, ms, ms, ms, ms, ms, 69, ms, ms, ms, 54],
        [ 3, ms, 70, ms, 37, 59,  2, ms, ms, ms, ms, ms, ms, ms, ms, ms, 15, 19, ms, ms, ms],
        [ 4, 87, 47, 37, ms, 63, ms, ms, ms, ms, ms, ms, ms, ms, ms, ms, ms,  3, 83, ms, 43],
        [ 5, ms, ms, 59, 63, ms, 24, 58, ms, ms, ms, 32, ms, ms, 34, ms, 62, 24, ms, ms, ms],
        [ 6, ms, ms,  2, ms, 24, ms, 84, ms, 91, ms, ms, ms, ms, ms, ms, ms, ms, ms, ms, ms],
        [ 7, ms, ms, ms, ms, 58, 84, ms, ms, 27, ms, ms, ms, ms, 36, ms, 56, ms, ms, ms, ms],
        [ 8, ms, ms, ms, ms, ms, ms, ms, ms, 47, 80, ms, ms, ms, 21, ms, ms, ms, ms, ms, ms],
        [ 9, ms, ms, ms, ms, ms, 91, 27, 47, ms, 98, ms, ms, ms, 68, ms, ms, ms, ms, ms, ms],
        [10, ms, ms, ms, ms, ms, ms, ms, 80, 98, ms,  8, 46, ms, 22, ms, ms, ms, ms, ms, ms],
        [11, ms, ms, ms, ms, 32, ms, ms, ms, ms,  8, ms, 38, 66, 51, ms, 95, 22, ms, ms, ms],
        [12, ms, ms, ms, ms, ms, ms, ms, ms, ms, 46, 38, ms, ms, 86, ms, ms, ms, ms, ms, ms],
        [13, ms, ms, ms, ms, ms, ms, ms, ms, ms, ms, 66, ms, ms, ms, 94,  7, 99, ms, ms, ms],
        [14, ms, ms, ms, ms, 34, ms, 36, 21, 68, 22, 51, 86, ms, ms, ms, 76, ms, ms, ms, ms],
        [15, ms, ms, ms, ms, ms, ms, ms, ms, ms, ms, ms, ms, 94, ms, ms, ms, 79, 78, 39, 65],
        [16, ms, 69, 15, ms, 62, ms, 56, ms, ms, ms, 95, ms,  7, 76, ms, ms, 71, ms, ms, ms],
        [17, ms, ms, 19,  3, 24, ms, ms, ms, ms, ms, 22, ms, 99, ms, 79, 71, ms, ms, 81, 59],
        [18, ms, ms, ms, 83, ms, ms, ms, ms, ms, ms, ms, ms, ms, ms, 78, ms, ms, ms, 57,  1],
        [19,  2, ms, ms, ms, ms, ms, ms, ms, ms, ms, ms, ms, ms, ms, 39, ms, 81, 57, ms, 46],
        [20, 12, 54, ms, 43, ms, ms, ms, ms, ms, ms, ms, ms, ms, ms, 65, ms, 59,  1, 46, ms]
        ], dtype=np.int32)
    
    """
    # Тест

    test_size = 51
    mat = np.zeros((test_size, test_size), dtype=np.int32)

    for i in range(test_size):
        for j in range(test_size):
            if i == 0:
                mat[i][j] = j

            elif j == 0:
                mat[i][j] = i

            elif i == j:
                mat[i][j] = ms

            else:
                mat[i][j] = int(uniform(1, 100))
    """

    print("Initial matrix:")
    print_mat(mat)
    
    final_path, final_bound = bounds_branches(mat)

    print("Optimal path:")

    for path in final_path:
        print(path[0], "->", path[1])

    print("\nTotal cost:", final_bound)


if __name__ == "__main__":
    start = time.time()
    main()
    print("\nSearch time:", time.time() - start, "seconds")
