from torchperf import perf
import torch

x = torch.rand(1000, 1000, device="cuda")
y = torch.rand(1000, 1000, device="cuda")


def test_device():
    assert torch.cuda.is_available()


def test_base():
    @perf
    def mul(x, y):
        return x * y

    _ = mul(x, y)


def test_output():
    rst = []

    @perf(o=rst)
    def mul(x, y):
        return x * y

    _ = mul(x, y)
    assert len(rst) > 0


def test_repeat():
    @perf(n=10)
    def mul(x, y):
        return x * y

    _ = mul(x, y)


def test_output_repeat():
    rst = []

    @perf(o=rst, n=10)
    def mul(x, y):
        return x * y

    _ = mul(x, y)
    assert len(rst) > 0


def test_output_repeat_warmup():
    rst = []

    @perf(o=rst, n=10, w=3)
    def mul(x, y):
        return x * y

    _ = mul(x, y)
    assert len(rst) > 0
