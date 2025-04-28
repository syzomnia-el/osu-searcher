# -*- coding: utf-8 -*-
import logging
import timeit
from collections.abc import Callable
from concurrent.futures import ProcessPoolExecutor
from functools import partial, wraps
from statistics import mean
from typing import Any, NamedTuple

type Function = Callable[..., ...]
TimerResult = NamedTuple('TimerResult', [('func', Function), ('time', float)])
type InnerTimer = Callable[[Function, int, int, bool], TimerResult]
type Timer = partial[TimerResult]


def _timer(
        func: Function,
        /,
        *args: Any,
        repeat: int = 10,
        number: int = 1000,
        silent: bool = True,
        **kwargs: Any
) -> TimerResult:
    """
    Measures the average execution time of a function.

    :param func: The function to be measured.
    :param args: The arguments to be passed to the function.
    :param repeat: The times the measurement is repeated.
    :param number: The times function is executed per measurement.
    :param silent: Whether to print the measurement result.
    :param kwargs: The keyword arguments to be passed to the function.
    :return: The measurement result of the function.
    """
    if not isinstance(repeat, int) or repeat <= 0:
        raise TypeError('`repeat` must be a positive integer.')
    if not isinstance(number, int) or number <= 0:
        raise TypeError('`number` must be a positive integer.')
    if not isinstance(silent, bool):
        raise TypeError('`silent` must be a boolean.')
    if not callable(func):
        raise TypeError('`func` must be a callable object.')

    curried_func = partial(func, *args, **kwargs)
    times = timeit.repeat(curried_func, repeat=repeat, number=number)
    mean_time = mean(times)
    if not silent:
        print(f'{func.__name__}: {mean_time:.6f} ms')
    return TimerResult(func=func, time=mean_time)


def generate_timer(repeat: int = 10, number: int = 1000, silent: bool = True) -> Timer:
    """
    Generates a timer function with default parameters.

    :param repeat: The times the measurement is repeated.
    :param number: The times function is executed per measurement.
    :param silent: Whether to print the measurement result.
    :return: A timer function with default parameters.
    """
    return partial(_timer, repeat=repeat, number=number, silent=silent)


def add_timer(
        func: Function = None,
        /,
        repeat: int = 10,
        number: int = 1000,
        silent: bool = False,
) -> partial[Function] | Function:
    """
    A decorator that measures the execution time of a function.

    :param func: The function to be measured.
    :param repeat: The times the measurement is repeated.
    :param number: The times function is executed per measurement.
    :param silent: Whether to print the measurement result.
    :return: A decorator that measures the execution time of a function.
    """
    if func is None:
        return partial(add_timer, repeat=repeat, number=number, silent=silent)

    @wraps(func)
    def wrapper(*args, **kwargs):
        _timer(func, *args, repeat=repeat, number=number, silent=silent, **kwargs)
        return func(*args, **kwargs)

    return wrapper


def execute_timer(funcs: set[Function], /, timer: Timer = None) -> list[TimerResult]:
    """
    Execute the timer for each function in parallel as a benchmark.

    :param funcs: The functions to be measured.
    :param timer: The timer function to be used.
    :return: The measurement results of each function
    """
    if not isinstance(funcs, set) or any(not callable(i) for i in funcs):
        raise TypeError('`funcs` must be a set of no-argument callable objects.')
    if timer is None:
        timer = generate_timer()
    elif not callable(timer):
        raise TypeError('`timer` must be a callable object.')

    with ProcessPoolExecutor() as executor:
        try:
            results = list(executor.map(timer, funcs))
            return results
        except Exception as e:
            logging.error('an error occurred while measuring the execution time.')
            logging.exception(e)
    return []


def print_timer_results(results: list[TimerResult]) -> None:
    """ Prints the timer results as a table with readable format. """
    if not isinstance(results, list) or any(not isinstance(i, TimerResult) for i in results):
        raise TypeError('`results` must be a list of `TimerResult` objects.')
    if not results:
        print('nothing to print.')
        return

    max_func_name_length = max(len(result.func.__name__) for result in results)
    results.sort(key=lambda x: x.time)
    baseline = results[0].time

    print('# Timer Results')
    print(f'No. | {'Function Name':<{max_func_name_length}} | Total Cost  | Rate')
    print(f'----|-{'-' * max_func_name_length}-|-------------|--------')
    for index, result in enumerate(results):
        print(
            f'{index:<3} | '
            f'{result.func.__name__:<{max_func_name_length}} | '
            f'{result.time:<.6f} ms | '
            f'{(result.time / baseline):.2%}'
        )
