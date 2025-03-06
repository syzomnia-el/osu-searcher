# -*- coding: utf-8 -*-
import timeit
from collections.abc import Callable
from concurrent.futures import ProcessPoolExecutor
from statistics import mean
from typing import NamedTuple

type Function = Callable[[], None]
TimerResult = NamedTuple('TimerResult', [('func', Function), ('time', float)])
type Timer = Callable[[Function, int, int, bool], TimerResult]
type TimerWrapper = Callable[[Function], TimerResult]


def timer(func: Function, repeat: int = 10, number: int = 1000, silent: bool = True) -> TimerResult:
    """
    Measures the average execution time of a function.

    :param func: The function to be measured.
    :param repeat: The times the measurement is repeated.
    :param number: The times function is executed per measurement.
    :param silent: Whether to print the measurement result.
    :return: The timer result of the function.
    """
    if not isinstance(repeat, int) or repeat <= 0:
        raise TypeError('`repeat` must be a positive integer.')
    if not isinstance(number, int) or number <= 0:
        raise TypeError('`number` must be a positive integer.')
    if not isinstance(silent, bool):
        raise TypeError('`silent` must be a boolean.')
    if not callable(func):
        raise TypeError('`func` must be a no-argument callable object.')

    if not silent:
        print(f'measuring {func.__name__}...')
    times = timeit.repeat(func, repeat=repeat, number=number)
    mean_time = mean(times)
    if not silent:
        print(
            f'measurement completed ({func.__name__}),'
            f'the average execution time is {mean_time:.6f} ms'
        )
    return TimerResult(func=func, time=mean_time)


def default_timer(func: Function) -> TimerResult:
    """ Measures the average execution time of a function using the default parameters. """
    return timer(func)


def execute_timer(funcs: set[Function], /, timer_wrapper: TimerWrapper = default_timer) -> list[TimerResult]:
    """
    Executes the timer for each function in parallel.

    :param funcs: The functions to be measured.
    :param timer_wrapper: The timer function to be used.
    :return: The timer results of each function
    """
    if not isinstance(funcs, set) or any(not callable(i) for i in funcs):
        raise TypeError('`funcs` must be a set of no-argument callable objects.')
    elif not callable(timer_wrapper):
        raise TypeError('`timer` must be a callable object.')

    with ProcessPoolExecutor() as executor:
        try:
            results = list(executor.map(timer_wrapper, funcs))
            return results
        except Exception as e:
            print('an error occurred while measuring the execution time.')
            print(f'{e.__class__.__name__}: {e}')
    return []


def print_timer_results(results: list[TimerResult]) -> None:
    """ Prints the timer results as a table with readable format. """
    if not isinstance(results, list) or any(not isinstance(i, TimerResult) for i in results):
        raise TypeError('`results` must be a list of `TimerResult` objects.')
    if not results:
        print('nothing to print.')
        return

    results.sort(key=lambda x: x.time)
    baseline = results[0].time
    print('## Timer Results')
    print('No.| Function Name             | Total Cost  | Rate')
    print('---|-------------------------- |-------------|---------')
    for index, result in enumerate(results):
        print(
            f'{index:<2} | '
            f'{result.func.__name__:<25.25} | '
            f'{result.time:<.6f} ms | '
            f'{(result.time / baseline) * 100:.2f} %'
        )
