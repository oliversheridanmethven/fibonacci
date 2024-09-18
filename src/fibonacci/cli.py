#!/usr/bin/env python3
"""
A Fibonacci number generator CLI.
"""
from typing import Any
import argparse
import logging
import sys
from fibonacci.fibonacci import PositiveInt
from fibonacci.fibonacci import (FibonacciGenerator,
                                 NaiveRecursion,
                                 TailRecursion,
                                 Sequential,
                                 MatricesNumpy,
                                 MatricesManuallyRepeatedMultiplication,
                                 MatricesManuallyRepeatedSquaring,
                                 MatricesEigenValue,
                                 MatricesLargestEigenValue, )


def cli_positive_integer(n: Any) -> PositiveInt:
    value = int(n)
    if value < 0:
        raise argparse.ArgumentTypeError(f"Must be positive ({n = })")
    return value


available_methods = {method.__name__: method() for method in [NaiveRecursion,
                                                              TailRecursion,
                                                              Sequential,
                                                              MatricesNumpy,
                                                              MatricesManuallyRepeatedMultiplication,
                                                              MatricesManuallyRepeatedSquaring,
                                                              MatricesEigenValue,
                                                              MatricesLargestEigenValue,
                                                              ]}


def cli_choose_fibonacci_method(desired_method: Any) -> FibonacciGenerator:
    desired_method = str(desired_method).lower()
    matches = [v for k, [n, v] in enumerate(available_methods.items()) if desired_method in [str(k), n.lower()]]
    if not matches:
        raise argparse.ArgumentTypeError(
            f"Could not match {desired_method = } with any of the available methods: {dict(enumerate(available_methods.keys()))}")
    assert len(matches) == 1, f"Too many matches found: {matches = }"
    return matches[0]


def cli_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--method",
                        help=f"Use any of the following methods (specify key or string): {dict(enumerate(available_methods.keys()))}",
                        type=cli_choose_fibonacci_method, default=MatricesManuallyRepeatedSquaring())
    parser.add_argument("--hide", help=f"Hide the answer (suitable for huge numbers).", action="store_true")
    parser.add_argument("--n", help="The n-th Fibonacci number to compute.", type=cli_positive_integer, default=0)
    return parser


def main(*args, n: PositiveInt, method: FibonacciGenerator, hide: bool, **kwargs) -> None:
    fibonacci_generator = method
    logging.info(f"Using the {fibonacci_generator = }")
    value = fibonacci_generator(n)
    if not hide:
        sys.set_int_max_str_digits(0)
        print(f"Fibonacci number {n} = {value}")


if __name__ == "__main__":
    parser = cli_arg_parser()
    args = parser.parse_args()
    kwargs = dict(vars(args))
    main(**kwargs)
