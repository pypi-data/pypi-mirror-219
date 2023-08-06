import sys
from subprocess import Popen, PIPE, check_output
import subprocess
import torch


def get_os_name():
    p = Popen(["lsb_release", "-d"], stdout=PIPE)
    rst = check_output(["cut", "-d:", "-f2"], stdin=p.stdout)
    return rst.decode("utf-8").strip()


def get_gpu_driver():
    p = Popen(
        ["nvidia-smi", "--query-gpu=driver_version", "--format=csv", "-i", "0"],
        stdout=PIPE,
    )
    rst = check_output(["tail", "-n1"], stdin=p.stdout)
    return rst.decode("utf-8").strip()


def get_linux_kernel():
    return subprocess.check_output(["uname", "-r"]).decode("utf-8").strip()


def show():
    def ver2str(x):
        return ".".join(map(str, x))

    print("python     ver|", ver2str(sys.version_info[:3]))
    print("pytorch    ver|", torch.__version__)
    print("CUDA       ver|", torch.version.cuda)
    print("cuDNN      ver|", torch.backends.cudnn.version() / 1000)
    print("nccl       ver|", ver2str(torch.cuda.nccl.version()))
    print("GPU Driver ver|", get_gpu_driver())
    print("Kernel     ver|", get_linux_kernel())
    print("Device Name   |", torch.cuda.get_device_name(0))
    print("OS name       |", get_os_name())
    print("num GPUs      |", torch.cuda.device_count())
