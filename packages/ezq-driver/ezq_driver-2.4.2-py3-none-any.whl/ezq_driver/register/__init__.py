# coding: utf-8

"""
ez-Q2.0设备控制驱动电子学单元模块，该模块包含四个电子学控制单元:

- `cmu_register.py`: 用于实现ez-Q2.0产品通信管理单元寄存器常量存储及查询功能
- `awg_register.py`: 用于实现ez-Q2.0产品调控子单元寄存器常量存储及查询功能
- `daq_register.py`: 用于实现ez-Q2.0产品读取子单元寄存器常量存储及查询功能
- `mix_register.py`: 用户实现ez-Q2.0产品混频子单元寄存器常量存储及查询功能

"""

from ..error.comm_error import RegisterMapKeyError
from .awg_register import _AWG_REGISTER_TABLE
from .cmu_register import _CMU_REGISTER_TABLE
from .daq_register import _DAQ_REGISTER_TABLE
from .mix_register import _MIX_REGISTER_TABEL


class RegisterMap:
    DEVICE_TYPE = ['CMU', 'AWG', 'DAQ', 'MIX']

    def __init__(self, cmu_register_table, awg_register_table,
                 daq_register_table, mix_register_table):
        self.init_map(cmu_register_table, awg_register_table,
                      daq_register_table, mix_register_table)

    def init_map(self, cmu_register_table, awg_register_table,
                 daq_register_table, mix_register_table):
        registers_tables = [cmu_register_table, awg_register_table,
                            daq_register_table, mix_register_table]
        name_map = {}
        addr_map = {}
        permission_map = {}
        for idx, device in enumerate(self.DEVICE_TYPE):
            m_name_map = {}
            m_addr_map = {}
            m_permission_map = {}
            registers_table = registers_tables[idx]
            for module in registers_table:
                module_name = module['name']
                base_addr = module['base_addr']
                registers = module['registers']
                for addr, name, permission in registers:
                    reg_item = dict(
                        base_addr=base_addr,
                        addr=addr,
                        name=name,
                        permission=permission)
                    m_name_map[f'{module_name}.{name}'] = reg_item
                    if base_addr is not None:
                        m_addr_map[base_addr, addr] = reg_item
                        m_permission_map[base_addr, addr] = permission
                    else:
                        m_addr_map[addr] = reg_item
                        m_permission_map[addr] = reg_item
            addr_map[device] = m_addr_map
            permission_map[device] = m_permission_map
            name_map[device] = m_name_map
        self.name_map = name_map
        self.addr_map = addr_map
        self.permission_map = permission_map

    def get_addr_by_name(self, device_type, name):
        if name in self.name_map[device_type]:
            reg = self.name_map[device_type][name]
            return reg['base_addr'], reg['addr']
        else:
            raise RegisterMapKeyError(name, device_type)

    def get_name_by_addr(self, device_type, *reg):
        addr_map = self.addr_map[device_type]
        name_map = self.name_map[device_type]
        idx = list(addr_map.keys()).index(reg)
        name = list(name_map.keys())[idx]
        return name

    def writable(self, device_type, *reg):
        permission_map = self.permission_map[device_type]
        if reg in permission_map:
            return 'w' in permission_map[reg]
        else:
            raise RegisterMapKeyError(reg, device_type)

    def readable(self, device_type, *reg):
        permission_map = self.permission_map[device_type]
        if reg in permission_map:
            return 'r' in permission_map[reg]
        else:
            raise RegisterMapKeyError(reg, device_type)


_REG_MAP = RegisterMap(
    _CMU_REGISTER_TABLE,
    _AWG_REGISTER_TABLE,
    _DAQ_REGISTER_TABLE,
    _MIX_REGISTER_TABEL
    )
