# -*- coding: utf-8 -*-
import timeit
from statistics import mean


def timer(func, *args, repeat=5, number=100_000) -> float:
    """Measure the average execution time of a function.

    Parameters:
        func: The function to be measured.
        *args: The arguments of the function.
        repeat: The times number to repeat the measurement.
        number: The times number to execute the function.

    Returns:
        The average execution time of the function.
    """
    args_str = ', '.join(*args)
    stmt = f'{func.__name__}({args_str})'
    setup = f'from __main__ import {func.__name__}'
    return mean(timeit.repeat(stmt=stmt, setup=setup, repeat=repeat, number=number))
