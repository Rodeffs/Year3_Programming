import numpy as np
import time
from random import uniform
ms = np.iinfo(np.int32).max


class Ant: # Класс, который будет хранить каждого муравья
    def __init__(self, mat, pheros):
        self._path = []
        self._mat = mat
        self._pheros = np.zeros(pheros.shape, dtype=np.int32)
        np.copyto(self._pheros, pheros)


    @property
    def mat(self):
        return self._mat

    @mat.setter
    def mat(self, value):
        self._mat = value

    @property
    def pheros(self):
        return self._pheros

    @pheros.setter
    def bound(self, value):
        self._pheros = value

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value


def randomly_choose(i, j, mat, pheromones):
    a = 0.5  # коэф. влияния феромона, определяется эврестически
    b = 0.5  # коэф. влияния расстояния, определяется эврестически



def ant_colony(mat):
    count_it = 1000  # количество итераций
    
    pheromones = np.zeros(mat.shape, dtype=np.int32)

    np.copyto(pheromones[0], mat[0])
    np.copyto(pheromones[:, 0], mat[:, 0])

    


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
        ], dtype=np.int32)


    final_path, final_bound = ant_colony(mat)

    print("\nOptimal path:")

    for path in final_path:
        print(path[0], "->", path[1])

    print("\nTotal cost:", final_bound)



if __name__ == "__main__":
    start = time.time()
    main()
    print("\nSearch time:", time.time() - start, "seconds")

