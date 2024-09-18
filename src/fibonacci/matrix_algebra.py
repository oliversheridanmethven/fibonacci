from fibonacci.type_hints import Square2x2Matrix, PositiveInt
import numpy as np



class MatrixAlgebra:
    """We do some matrix stuff by hand because numpy holds fixed size data types,
    but we want to exploit the arbitrary precision nature that python integers use
    by default."""

    @staticmethod
    def _matrix_mul(X: Square2x2Matrix, Y: Square2x2Matrix, /) -> Square2x2Matrix:
        """Multiplies X * Y for 2*2 matrices."""
        [[a, b], [c, d]] = X
        [[e, f], [g, h]] = Y
        return [[a * e + b * g, a * f + b * h],
                [c * e + d * g, c * f + d * h]]

    @classmethod
    def power_by_repeated_multiplication(cls, *, matrix: Square2x2Matrix, power: PositiveInt) -> Square2x2Matrix:
        if not isinstance(power, int) or power < 0:
            raise ValueError(f"{power = } must be a positive integer.")
        if power == 0:
            return [[1, 0], [0, 1]]
        if power == 1:
            return matrix

        new_matrix = matrix
        for multiplication in range(1, power):
            new_matrix = cls._matrix_mul(new_matrix, matrix)
        assert np.array(new_matrix).shape == (2, 2), f"The new matrix is not a 2x2, {new_matrix = }"
        return new_matrix

    @classmethod
    def power_by_repeated_squaring(cls, *, matrix: Square2x2Matrix, power: PositiveInt) -> Square2x2Matrix:
        if not isinstance(power, int) or power < 0:
            raise ValueError(f"{power = } must be a positive integer.")
        I = [[1, 0], [0, 1]]
        if power == 0:
            return I
        if power == 1:
            return matrix

        new_matrix = I
        largest_matrix = matrix
        remaining_exponent = power
        while remaining_exponent > 0:
            last_bit = remaining_exponent & 1
            if last_bit:
                new_matrix = cls._matrix_mul(new_matrix, largest_matrix)
            remaining_exponent = remaining_exponent >> 1
            if not remaining_exponent:
                break
            largest_matrix = cls._matrix_mul(largest_matrix, largest_matrix)

        assert np.array(new_matrix).shape == (2, 2), f"The new matrix is not a 2x2, {new_matrix = }"
        return new_matrix

