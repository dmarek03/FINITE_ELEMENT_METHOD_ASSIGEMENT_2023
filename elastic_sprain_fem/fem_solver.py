from dataclasses import dataclass
import numpy as np
from numpy import ndarray, dtype
from scipy import integrate


@dataclass
class FemSolver:
    domain = 2.0
    elem_number: int

    @staticmethod
    def E(x):
        return 2 if 0 <= x <= 1 else 6

    def basis(self, i: int, x: float) -> float:
        h = self.domain / self.elem_number
        if x < h * (i - 1) or x > h * (i + 1):
            return 0.0

        if x < h * i:
            return x / h - i + 1

        return -x / h + i + 1

    def basis_dx(self, i: int, x: float) -> float:
        h = self.domain / self.elem_number
        if x < h * (i - 1) or x > h * (i + 1):
            return 0.0

        if x < h * i:
            return 1 / h

        return -1 / h

    def B(self, i: int, j: int, lower_limit: float, upper_limit: float) -> float:

        def fun(x: float) -> float: return self.E(x) * self.basis_dx(i, x) * self.basis_dx(j, x)

        # W wersji po modyfiakcji należy jeszcze pierwszą część wyrażenia po niżej przemnożyć przez 2

        return self.E(0) * self.basis(i, 0) * self.basis(j, 0) - integrate.quad(fun, lower_limit, upper_limit)[0]

    def L(self, i: int, x: int) -> float:

        return 14 * self.basis(i, x)

    # Wersja po  dodaniu po prawej stronie równania funkcji -1000sin(πx) i zmienieniu warunku Robina

    def L2(self, i: int, x: int, lower_limit: float, upper_limit: float) -> float:
        def fun(y) -> float: return -1000 * np.sin(y * np.pi) * self.basis(i, y)

        return 8 * self.basis(i, x) - integrate.quad(fun, lower_limit, upper_limit)[0]

    def create_B_matrix(self) -> list[list[float]]:
        matrix = [[0.0] * self.elem_number for _ in range(self.elem_number)]

        for i in range(self.elem_number):
            for j in range(self.elem_number):

                if abs(i - j) <= 1:
                    lower_limit = self.domain * (max(max(i, j) - 1, 0)) / self.elem_number
                    upper_limit = self.domain * (min(min(i, j) + 1, self.elem_number)) / self.elem_number
                    matrix[i][j] = self.B(i, j, lower_limit, upper_limit)
        return matrix

    def create_x_interval_scale(self) -> list[float]:
        return [i * int(self.domain) / self.elem_number for i in range(self.elem_number+1)]

    def create_L_matrix(self) -> list[float]:
        matrix = [0.0] * self.elem_number
        for i in range(self.elem_number):

            matrix[i] = self.L(i, 0)

        return matrix

    def create_L_matrix2(self) -> list[float]:
        matrix = [0.0] * self.elem_number
        for i in range(self.elem_number):
            lower_limit = self.domain * max(0.0, (i - 1) / self.elem_number)
            upper_limit = self.domain * min(1.0, (i + 1) / self.elem_number)

            matrix[i] = self.L2(i, 0, lower_limit, upper_limit)

        return matrix

    def solve(self) -> tuple[ndarray[float, dtype[float]], ndarray[float, dtype[float]], ndarray[float, dtype[float]]]:
        B = np.array(self.create_B_matrix())
        L = np.array(self.create_L_matrix())
        L2 = np.array(self.create_L_matrix2())
        X = np.array(self.create_x_interval_scale())
        Y = np.append(np.linalg.solve(B, L), 0)
        Y2 = np.append(np.linalg.solve(B, L2), 0)
        return X, Y, Y2

