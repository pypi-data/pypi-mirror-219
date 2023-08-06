from torchperf.recipe import scaling_study, comparison_study
from torchperf import perf
import torch


def test_scaling_study():
    cache = []

    @perf(o=cache, n=10)
    def mul(x):
        return x * x

    sizes = list(range(3, 6))
    inputs = (torch.rand(sz, sz, device="cuda") for sz in sizes)
    avg, std = scaling_study(mul, cache, inputs)
    assert len(avg) == len(std) == len(sizes)
    assert sum(avg) > 0 and sum(std) > 0


def test_comparison_study():
    cache = []

    @perf(o=cache, n=10)
    def mul(x):
        return x * x

    @perf(o=cache, n=10)
    def add(x):
        return x + x

    # note: add and mul share the same `rst` as output cache.

    sizes = list(range(3, 6))
    funcs = [mul, add]
    inputs = (torch.rand(sz, sz, device="cuda") for sz in sizes)
    rsts = comparison_study(funcs, cache, inputs)
    [(mul_avg, mul_std), (add_avg, add_std)] = rsts

    assert len(rsts) == len(funcs)
    assert len(mul_avg) == len(mul_std) == len(sizes)
    assert len(add_avg) == len(add_std) == len(sizes)
    assert sum(mul_avg) > 0 and sum(mul_std) > 0
    assert sum(add_avg) > 0 and sum(add_std) > 0
