"""Windows 启动器：准备 CUDA DLL 后运行官方 llama_cpp.server。

命令行参数会原样交给官方 server 模块。本文件不实现 HTTP 路由、模型接口或
生成逻辑，只解决 Windows 在导入 llama_cpp 前需要预加载动态库的问题。
"""

from __future__ import annotations

import runpy

from windows_cuda_runtime import prepare_cuda_dll_search


# 先补齐 Windows DLL 搜索路径，再把 start_local_api.ps1 提供的命令行参数
# 原样交给官方 llama_cpp.server 模块处理。
prepare_cuda_dll_search()
runpy.run_module("llama_cpp.server", run_name="__main__")
