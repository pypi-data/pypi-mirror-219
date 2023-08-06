# PyTorch Perf

<p align="left">
<a href="https://opensource.org/licenses/BSD-3-Clause"><img alt="License" src="https://img.shields.io/badge/License-BSD_3--Clause-blue.svg"></a>
<a href="https://pypi.org/project/pytorch-perf/"><img alt="PyPI" src="https://img.shields.io/pypi/v/pytorch-perf"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://colab.research.google.com/drive/1g2U51MqC-MjO1zeCg9X5koWLYuzt4aFr?usp=sharing"><img alt="Colab Demo" src="https://colab.research.google.com/assets/colab-badge.svg"></a>
</p>


## Install

```
pip install -U pytorch-perf
```

To verify a successful installation:
```
python -c "from torchperf import info; info.show()"
```

## Usage

```python
import torch
from torchperf import perf, info

info.show()

N = 100
x = torch.rand(N, N, device="cuda")
results = []
repeats = 100

@perf(o=results, n=repeats)
def mul(x, y):
    return x * y

z = mul(x, x)
print(results[:5])
print("avg:", sum(results)/len(results))


@perf(n=repeats)
def mul(x, y):
    return x * y

z = mul(x, x)

```

