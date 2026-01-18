import numpy as np


class Matrix:
    def __init__(self, data):
        if not data or not isinstance(data[0], list):
            raise ValueError("Матрица должна быть двумерным списком")
        
        self.rows = len(data)
        self.cols = len(data[0])

        for row in data:
            if len(row) != self.cols:
                raise ValueError("Все строки матрицы должны иметь одинаковую длину")
        
        self.data = data
    
    def __add__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError("Можно складывать только матрицы")
        
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError(
                f"Несовместимые размеры: {self.rows}x{self.cols} + {other.rows}x{other.cols}"
            )
        
        result = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                row.append(self.data[i][j] + other.data[i][j])
            result.append(row)
        
        return Matrix(result)
    
    def __mul__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError("Поэлементное умножение определено только для матриц")
        
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError(
                f"Несовместимые размеры: {self.rows}x{self.cols} * {other.rows}x{other.cols}"
            )
        
        result = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                row.append(self.data[i][j] * other.data[i][j])
            result.append(row)
        
        return Matrix(result)
    
    def __matmul__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError("Матричное умножение определено только для матриц")
        
        if self.cols != other.rows:
            raise ValueError(
                f"Несовместимые размеры для умножения: "
                f"{self.rows}x{self.cols} @ {other.rows}x{other.cols}"
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
        
        return Matrix(result)
    
    def __str__(self) -> str:
        return self.__repr__()
    
    def __repr__(self) -> str:
        rows = len(self.data)
        cols = len(self.data[0])
        
        if rows <= 10 and cols <= 10:
            rows_str = []
            for row in self.data:
                row_str = "  ".join(f"{x:6.2f}" if isinstance(x, float) else f"{x:6}" for x in row)
                rows_str.append(f"[{row_str}]")
            return f"Matrix({rows}x{cols}):\n" + "\n".join(rows_str)
        else:
            return f"Matrix({rows}x{cols})"


def save_matrix_to_file(matrix, filename):
    with open(filename, 'w+', encoding='utf-8') as f:
        for row in matrix.data:
            row_str = ' '.join(str(x)for x in row)
            f.write(row_str + '\n')


def main():
    np.random.seed(0)

    np_matrix1 = np.random.randint(0, 10, (10, 10))
    np_matrix2 = np.random.randint(0, 10, (10, 10))

    matrix1 = Matrix(np_matrix1.tolist())
    matrix2 = Matrix(np_matrix2.tolist())
    print(matrix1, "\n", matrix2)
    result_add = matrix1 + matrix2
    print(f"Сложение: {result_add}")

    result_mul = matrix1 * matrix2
    print(f"Поэлементное умножение: {result_mul}")

    result_matmul = matrix1 @ matrix2
    print(f"Матричное умножение: {result_matmul}")
    

    save_matrix_to_file(result_add, "./artifacts/matrix_plus.txt")
    save_matrix_to_file(result_mul, "./artifacts/matrix_mul.txt")
    save_matrix_to_file(result_matmul, "./artifacts/matrix_at.txt")

if __name__ == "__main__":
    main()