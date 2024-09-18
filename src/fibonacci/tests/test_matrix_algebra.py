import unittest
from fibonacci.matrix_algebra import MatrixAlgebra
import numpy as np


class TestMatrixAlgebra(unittest.TestCase):

    def setUp(self):
        self.I = [[1, 0], [0, 1]]
        self.M = [[1, 2], [3, 4]]
        self.matrix_power_methods = [MatrixAlgebra.power_by_repeated_multiplication, MatrixAlgebra.power_by_repeated_squaring]

    def test_matrix_multiplication(self):
        np.random.seed(10)
        for trial in range(100):
            A, B = [np.random.randint(low=0, high=10, size=(2, 2)).tolist() for i in range(2)]
            self.assertEqual(np.matmul(A, B).tolist(), MatrixAlgebra._matrix_mul(A, B))

    def test_matrix_power_negative_exponent(self):
        for matrix_power_method in self.matrix_power_methods:
            with self.assertRaises(ValueError, msg=f"Negative exponents should raise errors for {matrix_power_method = }"):
                matrix_power_method(matrix=self.I, power=-1)

    def test_matrix_zero_power(self):
        for matrix_power_method in self.matrix_power_methods:
            self.assertEqual(self.I, matrix_power_method(matrix=self.M, power=0), f"{matrix_power_method = }")

    def test_matrix_identity_power(self):
        for matrix_power_method in self.matrix_power_methods:
            self.assertEqual(self.M, matrix_power_method(matrix=self.M, power=1), f"{matrix_power_method = }")

    def test_matrix_modest_power(self):
        for matrix_power_method in self.matrix_power_methods:
            for power in range(10):
                self.assertEqual(np.linalg.matrix_power(np.array(self.M), power).tolist(), matrix_power_method(matrix=self.M, power=power), f"Matrix powers did not match for {power = } for {matrix_power_method = }")



if __name__ == '__main__':
    unittest.main()
