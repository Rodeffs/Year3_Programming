class LinearSolve:

    def __init__(self, A, b):
        self._coef = A  # матрица коэффициентов
        self._mat = A  # будет использоваться в качестве временной при преобразованиях
        self._size = len(A)
        self._vec = b

    @property
    def coef(self):
        return self._coef

    @coef.setter
    def coef(self, M):
        self._coef = M

    @property
    def vec(self):
        return self._vec

    @vec.setter
    def vec(self, V):
        self._vec = V

    def linear_operation(self, i, j, a):  # прибавляет к j строке элементы из i строки, домноженные на a
        for k in range(self._size):
            self._mat[j][k] += self._mat[i][k]*a

    def swap_rows(self, i, j):  # меняем местами i и j строки
        for k in range(self._size):
            self._mat[i][k], self._mat[j][k] = self._mat[j][k], self._mat[i][k]

    def reset(self):  # чтобы не было сомнений, что решение получено разными методами
        self._mat = self._coef

    def print_mat(self):  # вывести преобразованную матрицу
        for i in range(self._size):
            output = ""
            for j in range(self._size):
                output += str(round(self._mat[i][j], 2)) + "\t"
            print(output)
    
    def gauss_method(self):
        x = [0] * self._size

        # Приведение к треугольному виду:

        for col in range(self._size):
            cur_max, max_index = 0, 0
            
            # Нахождение максимального по модулю элемента в каждом столбце

            for row in range(col, self._size):
                cur_elem = self._mat[row][col]

                if abs(cur_elem) > abs(cur_max):
                    cur_max = cur_elem
                    max_index = row
            
            # Затем меняем местами строки

            self.swap_rows(col, max_index)

            # И приводим к 0 остальные элементы в столбце, не меняя при этом значения в строках выше

            for i in range(col+1, self._size):
                mult = -self._mat[i][col]/cur_max
                self.linear_operation(col, i, mult)

        # Потом из треугольной матрицы легко получаем решение

        for i in range(self._size-1, -1, -1):
            x[i] = self._vec[i]

            for j in range(i+1, self._size):
                x[i] -= self._mat[i][j]*x[j]

            x[i] /= self._mat[i][i]
        
        print("Треугольная матрица:")
        self.print_mat()

        self.reset()
        return x
    
    def seidel_method(self):
        x = []
        return x


def main():
    
    A = [[3.82, 1.02, 0.75, 0.81],
         [1.05, 4.53, 0.98, 1.53],
         [0.73, 0.85, 4.71, 0.81],
         [0.88, 0.81, 1.28, 3.50]]

    b = [10.34,
         10.24,
         0.03,
         11.79]

    mat = LinearSolve(A, b)

    gauss_method_answer = mat.gauss_method()
    print("\nРешение методом Гаусса с выбором главного элемента:")
    for i in gauss_method_answer:
        print(i)

    
if __name__ == "__main__":
    main()
