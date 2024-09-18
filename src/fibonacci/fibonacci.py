#!/usr/bin/env python3
"""
A Fibonacci number generator.
"""

import numpy as np
from abc import ABC, abstractmethod
from fibonacci.matrix_algebra import MatrixAlgebra
from fibonacci.type_hints import PositiveInt


class FibonacciGenerator(ABC):
    """Generates Fibonacci numbers."""

    @abstractmethod
    def _fibonacci(self, n: PositiveInt, /) -> PositiveInt: ...

    def __call__(self, n: PositiveInt, /) -> PositiveInt:
        """
        Calculates the n-th fibonacci number F(n) defined by the
        relation F(n) = F(n-1) + F(n-2) with the convention
        F(0) = 0 and F(1) = 1. The first few terms are:

            n   |   0   1   2   3   4   5   6   7   8   9   10
            ---------------------------------------------------
            F(n)|   0   1   1   2   3   5   8   13  21  34  55

        Parameters
        ----------
        n :
            The desired term in the Fibonacci sequence.

        Returns
        -------
        PositiveInt :
            The n-th Fibonacci number.
        """
        if not isinstance(n, int) or n < 0:
            raise ValueError(f"{n = } must be a positive integer.")
        return self._fibonacci(n)


class NaiveRecursion(FibonacciGenerator):

    def _fibonacci(self, n: PositiveInt, /) -> PositiveInt:
        if n == 0:
            return 0
        elif n == 1:
            return 1
        return self(n - 1) + self(n - 2)


class TailRecursion(FibonacciGenerator):

    def _fibonacci_tail_recursion(self, *, remaining_terms: PositiveInt, second_last: PositiveInt = 0,
                                  last: PositiveInt = 1) -> PositiveInt:
        if remaining_terms == 0:
            return second_last
        if remaining_terms == 1:
            return last
        return self._fibonacci_tail_recursion(remaining_terms=remaining_terms - 1, second_last=last,
                                              last=second_last + last)

    def _fibonacci(self, n: PositiveInt, /) -> PositiveInt:
        return self._fibonacci_tail_recursion(remaining_terms=n)


class Sequential(FibonacciGenerator):

    def _fibonacci(self, n: PositiveInt, /) -> PositiveInt:
        values = [0, 1]
        if n <= 1:
            return values[n]
        m = 1
        while m <= n:
            m += 1
            values = [values[1], sum(values)]
        return values[0]


class MatricesNumpy(FibonacciGenerator):

    def _fibonacci(self, n: PositiveInt, /) -> PositiveInt:
        M = np.array([[1, 1],
                      [1, 0]], dtype=int)
        v_1 = np.array([[1],
                        [0]], dtype=int)
        v_n = np.linalg.matrix_power(M, n) @ v_1
        return v_n[1, 0]


class MatricesManuallyRepeatedMultiplication(FibonacciGenerator):

    def _fibonacci(self, n: PositiveInt, /) -> PositiveInt:
        M = [[1, 1],
             [1, 0]]
        return MatrixAlgebra.power_by_repeated_multiplication(matrix=M, power=n)[1][0]


class MatricesManuallyRepeatedSquaring(FibonacciGenerator):

    def _fibonacci(self, n: PositiveInt, /) -> PositiveInt:
        M = [[1, 1],
             [1, 0]]
        return MatrixAlgebra.power_by_repeated_squaring(matrix=M, power=n)[1][0]


class MatricesEigenValue(FibonacciGenerator):

    def _fibonacci(self, n: PositiveInt, /) -> PositiveInt:
        phi = 0.5 * (1.0 + np.sqrt(5.0))
        psi = 0.5 * (1.0 - np.sqrt(5.0))
        D = np.array([[phi ** n, 0.0],
                      [0.0, psi ** n]], dtype=float)
        U = np.array([[phi, psi],
                      [1.0, 1.0]], dtype=float)
        V = (1.0 / np.sqrt(5.0)) * np.array([[1.0, psi],
                                             [-1.0, phi]], dtype=float)
        v_1 = np.array([[1],
                        [0]], dtype=float)
        v_n = U @ D @ V @ v_1
        return v_n[1, 0]


class MatricesLargestEigenValue(FibonacciGenerator):

    def _fibonacci(self, n: PositiveInt, /) -> PositiveInt:
        phi = 0.5 * (1.0 + np.sqrt(5.0))
        return phi ** n / np.sqrt(5.0)
