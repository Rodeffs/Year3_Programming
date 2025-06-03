#from sys import maxsize as ms
ms = 100

import numpy as np


class Branch:
    def __init__(self, mat, n, parent, bound):
        self._parent = parent
        self._path = ()
        self._n = n
        self._mat = np.zeros((n, n), dtype=np.int64)
        np.copyto(self._mat, mat)
        self._bound = bound
        self._loss = 0

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    @property
    def bound(self):
        return self._bound

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

        for i in range(1, self._n):
            for j in range(1, self._n):
                if self._mat[i][j] != ms:
                    self._mat[i][j] -= min_rows[i]

        # Редукция столбцов

        min_cols = np.min(self._mat, axis=0)

        for i in range(1, self._n):
            for j in range(1, self._n):
                if self._mat[i][j] != ms:
                    self._mat[i][j] -= min_cols[j]
        
        min_rows = np.delete(min_rows, 0)
        min_cols = np.delete(min_cols, 0)

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
        
        for i in range(1, self._n):
            for j in range(1, self._n):
                if self._mat[i][j] == 0:
                    # Минимум по строке, не считая самого элемента

                    self._mat[i][j] = ms

                    min_row = np.min(self._mat[i][1:])
                    min_col = np.min(self._mat.transpose()[j][1:])

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
        without_path, with_path = None, None

        if self._n <= 1:
            return without_path, with_path

        bound = self.__calculate_bound()

        if bound == ms:
            return without_path, with_path

        else:
            self._bound += bound

        print(self._mat)
         
        src, dst = self.__calculate_loss()
       
        # Ветвь, где этот маршрут не включён

        self._mat[src][dst] = ms
        print(self._mat)

        if self._loss != ms:
            without_path = Branch(self._mat, self._n, self, self._bound+self._loss)

        # Ветвь, где этот маршрут включён
        
        dst_cities = self._mat[0]
        src_cities = self._mat.transpose()[0]
        
        src_city = src_cities[src]
        dst_city = dst_cities[dst]

        self._path = (src_city, dst_city)

        # Если обратный маршрут есть, то помечаем его как недостижимый

        try:
            src_reverse = np.where(dst_cities == src_city)[0][0]
            dst_reverse = np.where(src_cities == dst_city)[0][0]
            self._mat[src_reverse][dst_reverse] = ms

        except:
            pass

        self._mat = np.delete(self._mat, src, 0)
        
        self._mat = np.delete(self._mat, dst, 1)

        with_path = Branch(self._mat, self._n-1, self, self._bound)

        return without_path, with_path


def main():
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
        ], dtype=np.int64)

    root = Branch(mat, mat.shape[0], None, 0)
    final_branch = root
    queue = [root]

    while True:
        selected = min(queue, key=lambda x: x.bound)
        left, right = selected.branching()

        if selected.size <= 1:
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
