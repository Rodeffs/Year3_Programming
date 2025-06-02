#from sys import maxsize as ms
ms = 100

import numpy as np


class Branch:
    def __init__(self, mat, n, parent, bound, x, y):
        self._parent = parent
        self._left = None
        self._right = None
        self._path = ()
        self._n = n

        self._mat = np.zeros((n, n), dtype=np.int64)

        if n > 0:
            np.copyto(self._mat, mat)

        self._bound = bound
        self._x = [name for name in x]
        self._y = [name for name in y]
        self._loss = 0

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
    def path(self):
        return self._path

    @property
    def loss(self):
        return self._loss

    @property
    def size(self):
        return self._n

    def __calculate_bound(self):
        # Редукция строк

        min_rows = np.min(self._mat, axis=1)

        for i in range(self._n):
            for j in range(self._n):
                if self._mat[i][j] != ms:
                    self._mat[i][j] -= min_rows[i]

        # Редукция столбцов

        min_cols = np.min(self._mat, axis=0)

        for i in range(self._n):
            for j in range(self._n):
                if self._mat[i][j] != ms:
                    self._mat[i][j] -= min_cols[j]

        if ms in min_rows or ms in min_cols:
            return ms

        sum_rows = np.sum(min_rows)
        sum_cols = np.sum(min_cols)

        if sum_rows >= ms or sum_cols >= ms or (sum_rows+sum_cols) >= ms:
            return ms

        return sum_cols + sum_rows

    def __calculate_loss(self):
        # Проводим оценки для нулевых клеток и выбираем ту, которая будет НАИБОЛЬШЕЙ

        src, dst = 0, 0
        
        for i in range(self._n):
            for j in range(self._n):
                if self._mat[i][j] == 0:
                    # Минимум по строке, не считая самого элемента

                    self._mat[i][j] = ms

                    min_row = np.min(self._mat[i])
                    min_col = np.min(self._mat.transpose()[j])

                    loss = 0

                    if min_col == ms or min_row == ms:
                        loss = ms

                    else:
                        loss = min_col + min_row

                    if loss > self._loss:
                        self._loss = loss
                        src = i
                        dst = j

                    self._mat[i][j] = 0

        return src, dst

    def branching(self):
        if self._n == 0:
            return None, None

        bound = self.__calculate_bound()

        if bound == ms:
            self._bound = ms

        else:
            self._bound += bound

        print(self._mat)
         
        src, dst = self.__calculate_loss()

        print(self._bound, self._loss)
       
        # Ветвь, где этот маршрут не включён

        self._mat[src][dst] = ms

        if self._loss == ms:
            self._left = None

        else:
            self._left = Branch(self._mat, self._n, self, self._bound+self._loss, self._x, self._y)

        # Ветвь, где этот маршрут включён
        
        y, x = self._y[src], self._x[dst]
        self._path = (y, x)

        try:
            reverse_src = self._y.index(x)
            reverse_dst = self._x.index(y)
            self._mat[reverse_src][reverse_dst] = ms

        except:
            pass
        
        self._y.pop(src)
        self._mat = np.delete(self._mat, src, 0)
        
        self._x.pop(dst)
        self._mat = np.delete(self._mat, dst, 1)

        self._right = Branch(self._mat, self._n-1, self, self._bound, self._x, self._y)

        return self._left, self._right


def main():
    n = 5

    mat = np.array([
        [ms, 20, 18, 12, 8],
        [5, ms, 14, 7, 11],
        [12, 18, ms, 6, 11],
        [11, 17, 11, ms, 12],
        [5, 5, 5, 5, ms]
        ], dtype=np.int64)

    titles = ['A', 'B', 'C', 'D', 'E']

    root = Branch(mat, n, None, 0, titles, titles)
    final_branch = root
    queue = [root]

    while True:
        selected = min(queue, key=lambda x: x.bound)
        left, right = selected.branching()

        if selected.size == 0:
            final_branch = selected
            break

        if left is not None:
            queue.append(left)

        if right is not None:
            queue.append(right)

        queue.remove(selected)

    print("Длина оптимального пути:", final_branch.bound)
    print("Оптимальный путь:")
    
    cur_branch = final_branch
    while True:
        print(cur_branch.path)

        if cur_branch.parent is not None:
            cur_branch = cur_branch.parent

        else:
            break


if __name__ == "__main__":
    main()
