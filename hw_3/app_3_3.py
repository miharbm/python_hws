from functools import lru_cache
from time import perf_counter_ns

import numpy as np


class HashMixin:
    def __hash__(self):
        """
        Алгоритм:
        1. Суммируем все элементы матрицы
        2. Умножаем на количество строк
        3. Добавляем количество столбцов
        4. XOR с суммами по строкам и столбцам
        """

        data = self.data

        total_sum = sum(sum(row) for row in data)
        rows = len(data)
        cols = len(data[0])

        row_sums = [sum(row) for row in data]
        col_sums = [sum(data[i][j] for i in range(rows)) for j in range(cols)]

        h = total_sum * rows + cols
        for rs in row_sums:
            h ^= (rs << 4)
        for cs in col_sums:
            h ^= (cs << 8)
        
        return h % (2**31 - 1)


class MatrixWithHash(HashMixin):
    def __init__(self, data):
        if not data or not isinstance(data[0], list):
            raise ValueError("Матрица должна быть двумерным списком")
        
        self.rows = len(data)
        self.cols = len(data[0])
        
        for row in data:
            if len(row) != self.cols:
                raise ValueError("Все строки матрицы должны иметь одинаковую длину")
        
        self.data = data
        self._hash = None
    
    def __repr__(self):
        return f"Matrix({self.rows}x{self.cols}, hash={hash(self)})"
    
    def __eq__(self, other):
        if not isinstance(other, MatrixWithHash):
            return False
        
        if self.rows != other.rows or self.cols != other.cols:
            return False
        
        for i in range(self.rows):
            for j in range(self.cols):
                if self.data[i][j] != other.data[i][j]:
                    return False
        return True
    
    def __hash__(self):
        if self._hash is None:
            self._hash = super().__hash__()
        return self._hash
    
    @lru_cache(maxsize=128)
    def __matmul__(self, other):
        if not isinstance(other, MatrixWithHash):
            raise TypeError("Матричное умножение определено только для матриц")
        
        if self.cols != other.rows:
            raise ValueError(
                f"Несовместимые размеры: {self.rows}x{self.cols} @ {other.rows}x{other.cols}"
            )
        
        result = []
        for i in range(self.rows):
            row = []
            for j in range(other.cols):
                sum_val = 0
                for k in range(self.cols):
                    sum_val += self.data[i][k] * other.data[k][j]
                row.append(sum_val)
            result.append(row)
        
        return MatrixWithHash(result)

def save_matrix(matrix, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for row in matrix.data:
            row_str = ' '.join(str(int(x)) for x in row)
            f.write(row_str + '\n')


def find_collision():
    print("Поиск коллизий в хэш-функции")

    found = False
    attempts = 0
    max_attempts = 10000

    A = None
    C = None
    
    while not found and attempts < max_attempts:
        attempts += 1

        np.random.seed(attempts)

        A_data = np.random.randint(0, 3, (2, 2)).tolist()
        A = MatrixWithHash(A_data)

        for delta in range(1, 10):
            C_data = [[A_data[i][j] + delta if (i+j) % 2 == 0 else A_data[i][j] 
                      for j in range(2)] for i in range(2)]
            C = MatrixWithHash(C_data)
            
            if hash(A) == hash(C) and A != C:
                print(f"Найдена коллизия на попытке {attempts}:")
                print(f"A = {A.data}, hash = {hash(A)}")
                print(f"C = {C.data}, hash = {hash(C)}")
                found = True
                break
    
    if not found:
        print("Создаем коллизию явно")

        A = MatrixWithHash([
            [1, 2],
            [3, 4]
        ])

        C = MatrixWithHash([
            [2, 1],
            [4, 3]
        ])
        
        print(f"Создана коллизия:")
        print(f"A = {A.data}, hash = {hash(A)}")
        print(f"C = {C.data}, hash = {hash(C)}")

    if hash(A) == hash(C) and A != C:
        print(f"Коллизия подтверждена")
        print(f"  hash(A) = hash(C) = {hash(A)}")
        print(f"  A != C: {A.data} != {C.data}")
    else:
        print("Не удалось найти коллизию")
        return None, None
    
    return A, C


def find_equal_matrices(A, C):
    B = MatrixWithHash([
        [1, 0],
        [0, 1]
    ])
    D = MatrixWithHash([
        [1, 0],
        [0, 1]
    ])
    if B == D:
        print(f"B = D = {B.data}")
        
        AB = A @ B
        CD = C @ D
        
        print(f"A @ B = {AB.data}")
        print(f"C @ D = {CD.data}")
        
        if AB != CD:
            print(f"A @ B != C @ D")
            return B, D, AB, CD

    B = MatrixWithHash([
        [1, 1],
        [1, 1]
    ])
    D = MatrixWithHash([
        [1, 1],
        [1, 1]
    ])
    
    AB = A @ B
    CD = C @ D
    
    if AB != CD:
        print(f"B = D = {B.data}")
        print(f"A @ B = {AB.data}")
        print(f"C @ D = {CD.data}")
        return B, D, AB, CD
    
    A = MatrixWithHash([[1, 2], [3, 4]])
    C = MatrixWithHash([[2, 1], [4, 3]])
    B = MatrixWithHash([[1, 0], [0, 1]])
    D = MatrixWithHash([[1, 0], [0, 1]])
    
    AB = A @ B
    CD = C @ D
    
    print(f"Созданы матрицы:")
    print(f"A = {A.data}, C = {C.data}")
    print(f"B = D = {B.data}")
    print(f"A @ B = {AB.data}")
    print(f"C @ D = {CD.data}")
    
    return B, D, AB, CD


def main():
    print("Задача 3.3: Коллизии в хэш-функции матриц")

    A, C = find_collision()
    
    if A is None or C is None:
        print("Не удалось найти коллизию")
        return

    B, D, AB, CD = find_equal_matrices(A, C)

    print("Сохранение матриц в файлы:")
    
    save_matrix(A, "./artifacts/A.txt")
    save_matrix(B, "./artifacts/B.txt")
    save_matrix(C, "./artifacts/C.txt")
    save_matrix(D, "./artifacts/D.txt")
    save_matrix(AB, "./artifacts/AB.txt")
    save_matrix(CD, "./artifacts/CD.txt")
    
    with open("./artifacts/hash.txt", 'w', encoding='utf-8') as f:
        f.write(f"hash(A) = hash(C) = {hash(A)}\n")
        f.write(f"hash(AB) = {hash(AB)}\n")
        f.write(f"hash(CD) = {hash(CD)}\n")
    print("hash.txt сохранен")

    print("Проверка всех условий:")
    
    condition1 = hash(A) == hash(C)
    condition2 = A != C
    condition3 = B == D
    condition4 = AB != CD
    
    print(f"1. hash(A) == hash(C): {condition1} (hash = {hash(A)})")
    print(f"2. A != C: {condition2}")
    print(f"   A = {A.data}")
    print(f"   C = {C.data}")
    print(f"3. B == D: {condition3}")
    print(f"   B = {B.data}")
    print(f"   D = {D.data}")
    print(f"4. A @ B != C @ D: {condition4}")
    print(f"   A @ B = {AB.data}")
    print(f"   C @ D = {CD.data}")
    
    if condition1 and condition2 and condition3 and condition4:
        print("\nВсе условия выполнены")
    else:
        print("\nНе все условия выполнены")
    
    print("Первый вызов A @ B:")
    start = perf_counter_ns()
    AB1 = A @ B
    time1 = perf_counter_ns() - start
    print(f"Время: {time1} наносекунд")
    
    print("Второй вызов A @ B (должен быть из кэша):")
    start = perf_counter_ns()
    AB2 = A @ B
    time2 = perf_counter_ns() - start
    print(f"Время: {time2} наносекунд")
    
    if time2 < time1:
        print(f"Кэширование работает: {time2} < {time1}")

    print("Артефакты сохранены:")
    print("1. ./artifacts/A.txt - матрица A")
    print("2. ./artifacts/B.txt - матрица B")
    print("3. ./artifacts/C.txt - матрица C (коллизия с A)")
    print("4. ./artifacts/D.txt - матрица D (равна B)")
    print("5. ./artifacts/AB.txt - результат A @ B")
    print("6. ./artifacts/CD.txt - результат C @ D")
    print("7. ./artifacts/hash.txt - хэши матриц")


if __name__ == "__main__":
    main()