import torch
from functools import wraps, partial


def perf(_func=None, *, o=None, n=1, w=1):
    r"""performance measurement decorator

    o : List, optional [=None]
        "output" elapsed times per run are stored in the list.
        If `o` is `None`, an averaged result is printed.
    n : int, optional [=1]
        "number of runs"
    w : int, optional [=1]
        "warmup", number of warmup runs.
    """

    if not _func:
        return partial(perf, o=o, n=n, w=w)

    @wraps(_func)
    def measure_time(*args, **kwargs):
        # warmup
        for _ in range(w):
            rst = _func(*args, **kwargs)

        # recording
        tot, cnt = 0.0, 0
        stt = torch.cuda.Event(enable_timing=True)
        end = torch.cuda.Event(enable_timing=True)
        for _ in range(n):
            stt.record()
            rst = _func(*args, **kwargs)
            end.record()
            torch.cuda.synchronize()
            tim = stt.elapsed_time(end)
            if o is None:
                tot += tim
                cnt += 1
            else:
                o.append(tim)
        if o is None:
            print(tot / cnt)
        return rst

    return measure_time
