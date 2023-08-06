from typing import Callable, Iterable, Tuple, List
import numpy as np


class Stats:
    def __init__(self):
        self.avg = []
        self.std = []

    def update(self, output):
        tmp = np.asarray(output)
        self.avg.append(tmp.mean())
        self.std.append(tmp.std())


def scaling_study(func: Callable, cache: List, inputs: Iterable) -> Tuple:
    r"""study how a func performs regarding different size of inputs

    func : Callable
        a function under study that has been decorated by `perf`.
        The function can only take one argument. Consider using `partial` or a
        wrapper function to work around this limitation.
    cache : List
        the same list object passed as `o` in the decorator.
    inputs : Iterable
        an iterable of inputs. Sometimes inputs can be of large sizes. One
        should consider using a generator, e.g.
        `(torch.rand(1<<x,1<<x) for x in range(10, 15))`.
    return : Tuple
        averages and standard deviations. Both lists have the same length
        as the one of inputs.
    """

    rst = Stats()
    for input in inputs:
        cache.clear()
        _ = func(input)
        rst.update(cache)
    return rst.avg, rst.std


def comparison_study(
    funcs: List[Callable], cache: List, inputs: Iterable
) -> List[Tuple]:
    r"""study how different functions scales regarding different size of inputs
    funcs : List[Callable]
        a list of functions under study that has been decorated by `perf`.
        The function can only take one argument. Consider using `partial` or a
        wrapper function to work around this limitation. All the functions
        should share the same `cache`.
    cache : List
        the same list object passed as `o` in the decorator.
    inputs : Iterable
        an iterable of inputs. Sometimes inputs can be of large sizes. One
        should consider using a generator, e.g.
        `(torch.rand(1<<x,1<<x) for x in range(10, 15))`.
    return : List[Tuple]
        a list of the same size as the one of `func`. Each element in the list
        is a tuple of two lists: averages and standard deviations, which have
        the same length as the one of inputs.
    """

    rsts = [Stats() for _ in range(len(funcs))]

    # note: the order of the following nested for-loop cannot be reverted as
    # `inputs` could be a generator
    for input in inputs:
        for i, func in enumerate(funcs):
            cache.clear()
            _ = func(input)
            rsts[i].update(cache)

    rsts = [(stat.avg, stat.std) for stat in rsts]
    return rsts
