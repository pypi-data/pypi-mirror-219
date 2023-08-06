"""
ez-Q2.0设备控制驱动错误码模块，该模块包含以下单元:

- `comm_error.py`: 用于定义通用异常错误码及错误信息
- `awg_error.py`: 用于定义调控单元异常错误码及错误信息
- `daq_error.py`: 用于定义读取单元异常错误码及错误信息
- `mix_error.py`: 用于定义混频单元异常错误码及错误信息
- `hardware_error.py`: 用于定义硬件驱动单元异常错误码及错误信息
"""

class StandardEzqError(Exception):
    msg = ''

    def __init__(self, msg='', code=0):
        self.msg = msg
        self.code = int(code)

    def __str__(self):
        return f'[{self.code}] {self.msg}'
