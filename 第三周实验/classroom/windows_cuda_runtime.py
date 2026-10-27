# 教学说明：本文件用于让 Windows 在导入 llama_cpp 前找到 Conda 环境中的 CUDA DLL。
# 阅读时先确认输入与路径，再观察核心处理和输出；修改后应重新运行对应步骤。

"""让 Windows 在导入 llama_cpp 前找到 Conda 环境中的 CUDA DLL。

llama-cpp-python 的 CUDA wheel 自带 llama.cpp 动态库；本课程环境中的
PyTorch 又提供 CUDA 12.4 运行库。Windows 不一定会自动搜索这两个目录，
所以课堂脚本在导入 llama_cpp 前调用 prepare_cuda_dll_search()。
"""

from __future__ import annotations

import ctypes
import os
import sys
from pathlib import Path


# os.add_dll_directory 和 ctypes.CDLL 返回的对象必须一直存活，不能只放在局部变量里。
_DLL_HANDLES: list[object] = []


def prepare_cuda_dll_search() -> None:
    """在 Windows 上添加并预加载 llama.cpp 所需的 CUDA 动态库。"""

    if os.name != "nt":
        return

    # sys.prefix 指向当前 Conda 环境，避免误用 base 或系统 Python 中的 DLL。
    site_packages = Path(sys.prefix) / "Lib" / "site-packages"
    torch_lib = site_packages / "torch" / "lib"
    llama_lib = site_packages / "llama_cpp" / "lib"

    # 先把 PyTorch 的 CUDA 运行库目录和 llama.cpp 自己的 DLL 目录加入搜索路径。
    for directory in (torch_lib, llama_lib):
        if directory.is_dir():
            _DLL_HANDLES.append(os.add_dll_directory(str(directory)))

    # 再按依赖顺序预加载核心 DLL，避免 Windows 报“找不到指定的模块”。
    for filename in (
        "ggml-base.dll",
        "ggml-cpu.dll",
        "ggml-cuda.dll",
        "ggml.dll",
        "llama.dll",
    ):
        dll_path = llama_lib / filename
        if dll_path.is_file():
            _DLL_HANDLES.append(ctypes.CDLL(str(dll_path)))
