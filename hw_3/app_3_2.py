import numpy as np


class NDArrayOperatorsMixin:
    def __add__(self, other):
        return self.__class__(self.data + other.data)
    
    def __mul__(self, other):
        return self.__class__(self.data * other.data)
    
    def __matmul__(self, other):
        return self.__class__(self.data @ other.data)
    
    def __sub__(self, other):
        return self.__class__(self.data - other.data)
    
    def __truediv__(self, other):
        return self.__class__(self.data / other.data)


class WriteToFileMixin:
    def write_to_file(self, filename: str):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(str(self))


class PrettyPrintMixin:
 def __str__(self):
        rows, cols = self.data.shape
        result = []
        
        for i in range(min(rows, 10)):
            row_str = []
            for j in range(min(cols, 10)):
                val = self.data[i, j]
                row_str.append(f"{val:6.1f}" if isinstance(val, float) else f"{val:6}")
            result.append(" ".join(row_str))
            if cols > 10:
                result[-1] += " ..."
        
        if rows > 10:
            result.append("...")
        
        return f"Matrix {self.data.shape}:\n" + "\n".join(result)


class GetterSetterMixin:
    @property
    def shape(self):
        return self.data.shape
    
    @property
    def rows(self):
        return self.data.shape[0]
    
    @property
    def cols(self):
        return self.data.shape[1]
    
    def get_element(self, i: int, j: int):
        return self.data[i, j]
    
    def set_element(self, i: int, j: int, value):
        self.data[i, j] = value


class MatrixMixin(
    NDArrayOperatorsMixin,
    WriteToFileMixin,
    PrettyPrintMixin,
    GetterSetterMixin
):
    def __init__(self, data: np.ndarray):
        self.data = np.array(data, dtype=np.float64)
    
    def __repr__(self):
        return f"MatrixMixin({self.rows}x{self.cols})"


def main():
    np.random.seed(0)
    
    np_matrix1 = np.random.randint(0, 10, (10, 10))
    np_matrix2 = np.random.randint(0, 10, (10, 10))

    matrix1 = MatrixMixin(np_matrix1)
    matrix2 = MatrixMixin(np_matrix2)

    result_add = matrix1 + matrix2
    print(f"+ {result_add}")

    result_mul = matrix1 * matrix2
    print(f"* {result_mul}")

    result_matmul = matrix1 @ matrix2
    print(f"@ {result_matmul}")

    result_sub = matrix1 - matrix2
    print(f"- {result_sub}")

    result_div = matrix1 / matrix2
    print(f"/ {result_div}")
    
    result_add.write_to_file("./artifacts/matrix_plus_2.txt")
    result_mul.write_to_file("./artifacts/matrix_mul_2.txt")
    result_matmul.write_to_file("./artifacts/matrix_at_2.txt")
    
    
    print(f"\nA[0, 0]={matrix1.get_element(0, 0)}")
    matrix1.set_element(0, 0, 100)
    print(f"A[0, 0]={matrix1.get_element(0, 0)}")
    
    matrix1.set_element(0, 0, np_matrix1[0, 0])

if __name__ == "__main__":
    main()