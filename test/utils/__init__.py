# -*- coding: utf-8 -*-
import timeit
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from statistics import mean
from typing import Callable

DEFAULT_REPEAT: int = 10
DEFAULT_NUMBER: int = 1000

type Function = Callable[[], None]
type TimerWrapperFunction = Callable[[Function], TimerResult]


@dataclass(frozen=True)
class TimerResult:
    """
    The timer result type.

    Attributes:
        func: The function to be measured.
        time: The average execution time of the function in milliseconds.
    """
    func: Function
    time: float


def timer(func: Function, repeat: int = DEFAULT_REPEAT, number: int = DEFAULT_NUMBER) -> TimerResult:
    """
    Measures the average execution time of a function.

    :param func: The function to be measured.
    :param repeat: The times number to repeat the measurement.
    :param number: The times number to execute the function.
    :return: The average execution time of the function in milliseconds.
    """
    global DEFAULT_REPEAT, DEFAULT_NUMBER
    if not callable(func):
        raise TypeError('func must be a callable object.')
    if not isinstance(repeat, int) or repeat <= 0:
        raise TypeError('repeat must be a positive integer.')
    if not isinstance(number, int) or number <= 0:
        raise TypeError('number must be a positive integer.')

    print(f'Measuring the execution time of {func.__name__}...')
    times = timeit.repeat(func, repeat=repeat, number=number)
    print(f'Measurement completed of {func.__name__}, the average execution time is {mean(times):.6f} ms')
    return TimerResult(func=func, time=mean(times))


def default_timer_wrapper(func: Function) -> TimerResult:
    """
    The default timer wrapper function.

    :param func: The function to be measured.
    :return: The timer result.
    """
    return timer(func)


def print_formatted_timer_results(
        funcs: set[Function],
        timer_wrapper: TimerWrapperFunction = default_timer_wrapper
) -> None:
    """
    Prints the formatted timer results of functions.

    :param funcs: The functions to be measured.
    :param timer_wrapper: The timer wrapper function.
    """
    with ProcessPoolExecutor() as executor:
        try:
            results = list(executor.map(timer_wrapper, funcs))
        except Exception as e:
            print('An error occurred while measuring the execution time.')
            print(e)

    baseline = min(results, key=lambda x: x.time).time

    print('## Timer Results')
    print('No.| Function Name            | Execution Time | Rate')
    print('---|--------------------------|----------------|--------')
    for index, result in enumerate(results):
        print(f'{index:<2} | {result.func.__name__:<25.25}  | {result.time:<.6f} ms | {result.time / baseline:.4f}')
