# -*- coding: utf-8 -*-
import timeit
from multiprocessing import Process, Queue
from statistics import mean
from typing import Callable


def timer(func: Callable, *args, repeat: int = 10, number: int = 1000) -> float:
    """
    Measures the average execution time of a function.

    Parameters:
        func: The function to be measured.
        *args: The arguments of the function.
        repeat: The times number to repeat the measurement.
        number: The times number to execute the function.

    Returns:
        The average execution time of the function in milliseconds.
    """
    if not callable(func):
        raise TypeError(f'{func.__name__} is not callable.')
    if not isinstance(repeat, int):
        raise TypeError(f'{repeat=} is not an integer.')
    if not isinstance(number, int):
        raise TypeError(f'{number=} is not an integer.')
    if repeat <= 0:
        raise ValueError(f'{repeat=} is invalid.')
    if number <= 0:
        raise ValueError(f'{number=} is invalid.')

    args_str = None
    if args:
        args_str = ', '.join(*args) if len(*args) > 1 else str(*args)

    class_name = func.__qualname__.split('.')[0]

    stmt = f'{func.__qualname__}({args_str})' if args_str else f'{func.__qualname__}()'
    setup = f'from __main__ import {class_name}'

    return mean(timeit.repeat(stmt=stmt, setup=setup, repeat=repeat, number=number)) * 1000


def _get_timer_result(queue: Queue, func: Callable, *args, repeat: int = 10, number: int = 1000) -> None:
    """
    Gets the result of timing the execution of a function.

    Args:
        queue: A queue to store the timer result.
        func: The function to be measured.
        *args: The arguments of the function.
        repeat: The times number to repeat the measurement.
        number: The times number to execute the function.
    """
    queue.put(timer(func, *args, repeat=repeat, number=number))


def print_timer_result(funcs: list[Callable], *args, repeat: int = 10, number: int = 1000) -> None:
    """
    Prints the result of timing the execution of a function.

    Args:
        funcs: A list of functions to be measured.
        *args: The arguments of the function.
        repeat: The times number to repeat the measurement.
        number: The times number to execute the function.
    """
    process = []
    q = Queue()

    for index, value in enumerate(funcs):
        print(f'create Process-{index}: {value.__name__}')
        process.append(
            Process(target=_get_timer_result, args=(q, value, *args), kwargs={'repeat': repeat, 'number': number})
        )

    for p in process:
        p.start()

    for p in process:
        p.join()

    results = [q.get() for _ in range(len(funcs))]
    baseline = sorted(results)[0]

    print('No | Function Name            | Execution Time | Rate')
    print('---|--------------------------|----------------|--------')
    for index, (func, result) in enumerate(zip(funcs, results)):
        print(f'{index:<2} | {func.__name__:<24} | {result:.6f} ms  | {result / baseline:.4f}')

    for p in process:
        p.close()
