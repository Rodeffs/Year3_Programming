import numpy as np
import time
from random import uniform
ms = np.iinfo(np.int32).max


def ant_compute(ant, mat, pheromones, a, b):
    n = mat.shape[0]
    
    ant_city = ant
    ant_path = [ant_city]
    ant_length = 0

    while True:
        total_want = 0
        available_cities = []

        for adjacent_city in range(1, n):
            distance = mat[ant_city][adjacent_city]
            
            if distance != ms:
                # Критерий остановки, если все города обошли и следующий путь ведёт в начало, то идём по нему

                if len(ant_path) == n-1 and adjacent_city == ant:
                    ant_path.append(adjacent_city)
                    ant_length += distance
                    return ant_path, ant_length

                # Иначе же, если по этому городу не шли, то добавляем этот город к доступным и заодно просчитываем суммарное желание муравья
                
                elif adjacent_city not in ant_path:
                    probability = pheromones[ant_city][adjacent_city]**a + (1/distance)**b
                    total_want += probability
                    available_cities.append([adjacent_city, probability])
        
        available_count = len(available_cities)

        # Если из этого города больше нет путей, то муравей зашёл в тупик и его не считаем

        if available_count == 0:
            return 0, []
        
        # Вероятность муравья пойти в доступный город

        for i in range(available_count):
            available_cities[i][1] /= total_want

        available_cities.sort(key=lambda x: x[1])

        # Случайно выбираем следующий город для муравья, опираясь на вероятность

        random_value = uniform(0,1)
        prev_probability = 0

        for i in range(available_count):
            if (random_value <= available_cities[i][1] + prev_probability) or (i == available_count - 1):
                ant_path.append(available_cities[i][0])
                ant_length += mat[ant_city][available_cities[i][0]]
                ant_city = available_cities[i][0]
                break

            else:
                prev_probability += available_cities[i][1]


def ant_colony(mat, a, b, p, count_it):
    pheromones = np.zeros(mat.shape, dtype=np.float32)

    final_path, final_length = [], ms
    n = mat.shape[0]

    for it in range(count_it):
        new_pheromones = np.zeros(mat.shape, dtype=np.float32)

        # Всего муравьёв столько же, сколько и вершин. Каждый муравей начинает путь из своей вершины

        for ant in range(1, n):
            ant_path, ant_length = ant_compute(ant, mat, pheromones, a, b)

            # Если муравей зашёл в тупик не обойдя все вершины или не вернувшись в начальную, то ничего не делаем
            
            if not ant_path:
                continue

            # Если дошёл, то добавляем в буфер обновления феромонов величину q/L, где L - длина пройденного пути
            
            for i in range(n-1):
                new_pheromones[ant_path[i]][ant_path[i+1]] += 1/ant_length
            
            # Если путь оказался наикратчайшим, то сохраняем его

            if ant_length < final_length:
                final_path = ant_path
                final_length = ant_length

        # Обновление феромонов

        for j in range(1, n):
            local_pheromones_sum = 0
            
            # Сумма обновления всех феромонов из этой вершины

            for i in range(1, n):
                local_pheromones_sum += new_pheromones[i][j]
            
            # Испарение феромонов

            for i in range(1, n):
                pheromones[i][j] = (1-p)*pheromones[i][j] + local_pheromones_sum

    return final_path, final_length
            

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

    # Эвристики:
    a = 1.0  # коэф. влияния феромона (a >= 0)
    b = 2.0  # коэф. влияния расстояния (b >= 1)
    p = 0.7  # коэф. испарения феромона (0 <= p <= 1)
    count_it = 50  # количество итераций

    final_path, final_length = ant_colony(mat, a, b, p, count_it)

    cities = ['/', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    print("Optimal path:")

    for i in range(len(final_path) - 1):
        print(cities[final_path[i]], "->", cities[final_path[i+1]])

    print("\nTotal cost:", final_length)


if __name__ == "__main__":
    start = time.time()
    main()
    print("\nSearch time:", time.time() - start, "seconds")

