from sys import maxsize as ms
from typing import final
import numpy as np


class Branch:
    def __init__(self, mat, n, parent, path, bound):
        self._parent = parent
        self._left = None
        self._right = None
        self._path = path
        self._n = n
        self._mat = np.zeros((n, n))
        self._bound = bound
        self._loss = 0
        np.copyto(self._mat, mat)

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, left):
        self._left = left

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, right):
        self._right = right

    @property
    def bound(self):
        return self._bound

    @bound.setter
    def bound(self, bound):
        self._bound = bound

    @property
    def mat(self):
        return self._mat

    @mat.setter
    def mat(self, mat):
        np.copyto(self._mat, mat)

    @property
    def path(self):
        return self._path

    @property
    def loss(self):
        return self._loss

    def __calculate_bound(self):
        # Редукция строк

        min_rows = self._mat.min(axis=0)

        for i in range(self._n):
            for j in range(self._n):
                if self._mat[i][j] != ms:
                    self._mat[i][j] -= min_rows[i]

        # Редукция столбцов

        min_cols = self._mat.min(axis=1)

        for i in range(self._n):
            for j in range(self._n):
                if self._mat[i][j] != ms:
                    self._mat[i][j] -= min_cols[j]

        return np.sum(min_rows) + np.sum(min_cols)

    def __calculate_loss(self):
        # Проводим оценки для нулевых клеток и выбираем ту, которая будет НАИБОЛЬШЕЙ

        src, dst = 0, 0
        
        for i in range(self._n):
            for j in range(self._n):
                if self._mat[i][j] == 0:
                    min_row, min_col = 0, 0

                    # Минимум по строке, не считая самого элемента

                    if j == 0:
                        min_row = np.min(self._mat[i][j+1:])

                    elif j == self._n-1:
                        min_row = np.min(self._mat[i][:j])

                    else:
                        min_row = min(np.min(self._mat[i][:j]), np.min(self._mat[i][j+1:]))

                    # Минимум по столбку, не считая самого элемента

                    if i == 0:
                        min_col = np.min(self._mat[i+1:][j])

                    elif i == self._n-1:
                        min_col = np.min(self._mat[:i][j])

                    else:
                        min_col = min(np.min(self._mat[i+1:][j]), np.min(self._mat[:i][j]))

                    loss = 0

                    if min_col > ms or min_row > ms:
                        loss = ms

                    else:
                        loss = min_col + min_row

                    if loss > self._loss:
                        self._loss = loss
                        src = i
                        dst = j

        return src, dst

    def branching(self):
        bound = self.__calculate_bound()

        if bound == ms:
            return None, None

        else:
            self._bound += bound

        src, dst = self.__calculate_loss()

        # Ветвь, где этот маршрут не включён

        self._mat[src][dst] = ms

        if self._loss == ms:
            self._left = None

        else:
            self._left = Branch(self._mat, self._n, self, self._path, self._bound+self._loss)

        # Ветвь, где этот маршрут включён

        self._mat[dst][src] = ms

        for i in range(self._n):
            self._mat[i][dst] = ms

        for j in range(self._n):
            self._mat[src][j] = ms

        self._path.append((src, dst))
        
        self._right = Branch(self._mat, self._n, self, self._path, self._bound)

        return self._left, self._right


def main():
    n = 20

    mat = np.array([
        [ms, 82, ms, 87, ms, ms, ms, ms, ms, ms, ms, ms, ms, ms, ms, ms, ms, ms,  2, 12],
        [82, ms, 70, 47, ms, ms, ms, ms, ms, ms, ms, ms, ms, ms, ms, 69, ms, ms, ms, 54],
        [ms, 70, ms, 37, 59,  2, ms, ms, ms, ms, ms, ms, ms, ms, ms, 15, 19, ms, ms, ms],
        [87, 47, 37, ms, 63, ms, ms, ms, ms, ms, ms, ms, ms, ms, ms, ms,  3, 83, ms, 43],
        [ms, ms, 59, 63, ms, 24, 58, ms, ms, ms, 32, ms, ms, 34, ms, 62, 24, ms, ms, ms],
        [ms, ms,  2, ms, 24, ms, 84, ms, 91, ms, ms, ms, ms, ms, ms, ms, ms, ms, ms, ms],
        [ms, ms, ms, ms, 58, 84, ms, ms, 27, ms, ms, ms, ms, 36, ms, 56, ms, ms, ms, ms],
        [ms, ms, ms, ms, ms, ms, ms, ms, 47, 80, ms, ms, ms, 21, ms, ms, ms, ms, ms, ms],
        [ms, ms, ms, ms, ms, 91, 27, 47, ms, 98, ms, ms, ms, 68, ms, ms, ms, ms, ms, ms],
        [ms, ms, ms, ms, ms, ms, ms, 80, 98, ms,  8, 46, ms, 22, ms, ms, ms, ms, ms, ms],
        [ms, ms, ms, ms, 32, ms, ms, ms, ms,  8, ms, 38, 66, 51, ms, 95, 22, ms, ms, ms],
        [ms, ms, ms, ms, ms, ms, ms, ms, ms, 46, 38, ms, ms, 86, ms, ms, ms, ms, ms, ms],
        [ms, ms, ms, ms, ms, ms, ms, ms, ms, ms, 66, ms, ms, ms, 94,  7, 99, ms, ms, ms],
        [ms, ms, ms, ms, 34, ms, 36, 21, 68, 22, 51, 86, ms, ms, ms, 76, ms, ms, ms, ms],
        [ms, ms, ms, ms, ms, ms, ms, ms, ms, ms, ms, ms, 94, ms, ms, ms, 79, 78, 39, 65],
        [ms, 69, 15, ms, 62, ms, 56, ms, ms, ms, 95, ms,  7, 76, ms, ms, 71, ms, ms, ms],
        [ms, ms, 19,  3, 24, ms, ms, ms, ms, ms, 22, ms, 99, ms, 79, 71, ms, ms, 81, 59],
        [ms, ms, ms, 83, ms, ms, ms, ms, ms, ms, ms, ms, ms, ms, 78, ms, ms, ms, 57,  1],
        [ 2, ms, ms, ms, ms, ms, ms, ms, ms, ms, ms, ms, ms, ms, 39, ms, 81, 57, ms, 46],
        [12, 54, ms, 43, ms, ms, ms, ms, ms, ms, ms, ms, ms, ms, 65, ms, 59,  1, 46, ms]
        ])

    root = Branch(mat, n, None, [], 0)

    final_path = []
    final_length = 0
    queue = [root]

    while len(queue) > 0:
        selected = min(queue, key=lambda x: x.bound)
        left, right = selected.branching()

        if left is None and right is None:
            final_path = selected.path
            final_length = selected.bound
            break

        if left is not None:
            queue.append(left)

        if right is not None:
            queue.append(right)

        queue.remove(selected)

    print("Длина оптимального пути:", final_length)
    print("Оптимальный путь:")

    cur_path = final_path[0]

    while len(cur_path) > 0:
        print(cur_path[0], "->", cur_path[1])

        final_path.remove(cur_path)

        for path in final_path:
            if path[0] == cur_path[1]:
                cur_path = path
                break


if __name__ == "__main__":
    main()
