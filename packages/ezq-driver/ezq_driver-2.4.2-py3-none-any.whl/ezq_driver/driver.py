# coding: utf-8
# ezq_driver/driver.py

__all__ = ['connect',
           're_connect',
           'turn_on_off_slot',
           'platform_self_check',
           'remote_config', 
           'config_platform_params']

import re
import os
import time
import progressbar
from .units.awg_unit import AWGUnit
from .units.daq_unit import DAQUnit
from .units.mix_unit import MIXUnit
from .units.cmu_unit import CmuUnit
from .constant import const
from typing import Union, Literal
from .utils import (
    bytes_to_int,
    get_bit,
    ip_to_int,
    ProgressBar,
    DAStatusParser
)
from .error.comm_error import RecvTimeoutError
from .error.hardware_error import (
    InitDeviceFail,
    RebootFail,
    ConnectFail,
    ReConnectFail,
    BinFileNotFoundError,
    WriteDDRTimeoutError,
    WriteFlashTimeoutError,
    ReadFlashTimeoutError,
    FlashDataNotMatch,
    DDRDataNotMatch,
    WriteEepromTimeoutError,
    ReadEepromTimeoutError,
    EepromDataNotMatch,
    IllegalIpAddressError,
    SlotPowerStatusError
)

class EzqDevice(AWGUnit, DAQUnit, MIXUnit):
    """
    该单元是ez-Q2.0产品硬件驱动主模块, 实现硬件模块管理功能并集成电子学单元模块功能接口.

    Examples:
        >>> from ezq_driver.driver import EzqDevice
        >>> ezq = EzqDevice(ip = '10.0.9.11', slot = 23, console_log = True, batch_mode = False)
        >>> ezq.connect()
        >>> ezq.turn_on_off_slot(on_off='on', slot = 16)
        0

    该模块包含以下函数:

    - <a href="#driver1">***connect()***</a> - connect device.
    - <a href="#driver2">***turn_on_off_slot(on_off, delay, slot)***</a> - Turn on or turn off slot.
    - <a href="#driver3">***platform_self_check()***</a> - platform self check.
    - <a href="#driver4">***remote_config(file_path, slot)***</a> - Remote update of FPGA logic.
    - <a href="#driver5">***config_platform_params(file_path, slot)***</a> - Device parameter configuration.
    </br>
    *****************************************************************************************************************************************
    
    """
    def __init__(
        self, ip, port=10000, slot=23, name='', logger=None,console_log=False, dev_mode=False, batch_mode=True,wave_type='i2',
        sample_depth=2000,sample_start=0, sample_count=1, demod_freqs=[],demod_weights=None,demod_window_start=[0],demod_window_width=[1000],
        point_list=[],sync_mode=1
    ):
        if slot in const.DAQ_SLOTS:
            DAQUnit.__init__(
                self, ip, port, slot, name, logger, console_log, dev_mode,
                batch_mode,sample_depth, sample_start, sample_count, demod_freqs, 
                demod_weights,demod_window_start,demod_window_width,point_list,sync_mode
            )
        elif slot in const.MIX_SLOTS:
            MIXUnit.__init__(self, ip, port, slot, name, logger, console_log, dev_mode, batch_mode)
        else:
            AWGUnit.__init__(
                self, ip, port, slot, name, logger, console_log, dev_mode,
                batch_mode, wave_type
            )

        self.connect_status = 0
        self.active_slot = []
        self.power_slot = []
        self.RESPONSE_TIMEOUT = const.RESPONSE_TIMEOUT

    def connect(self) -> int:
        """
        <a id="driver1">connect device</a>

        Raises:
            InitDeviceFail: Fail to init device
            ConnectFail: Fail to connect device

        Returns:
            The program ends normally with return value `0`, otherwise abnormal.
        """
        slot = const.CMU_SLOT
        self.connect_status = 0
        try_count = 0
        max_tries = 5
        while try_count < max_tries:
            try:
                self[slot, 'CPU.FUNCTION'] = 0x08
                self[slot, 'CPU.PERMISSION'] = 0x01
                if bytes_to_int(self[slot, 'CPU.PERMISSION']) != 0x01:
                    raise InitDeviceFail(slot)
                else:
                    # 1.机箱槽位是否存在刀片
                    # 2.读取CMU固件CMU_FUNC模块SLOT_MONITOR寄存器([0x30000, 0x30])
                    # 3.返回值为32bit位宽，[20:0]标识前面板0-20槽位，最低位对应0槽: 1 -> 存在板卡, 0 -> 槽位无硬件
                    slot_info_bytes = self[slot, 'FUNC.SLOT_MONITOR'] 
                    slot_info = bytes_to_int(slot_info_bytes)
                    for i in range(21):
                        active = get_bit(slot_info, i)
                        if active:
                            self.active_slot.append(i)
                    # TODO: get CMU AWG DAQ parameters from CMU DDR
                self.connect_status = 1
                return 0
            except RecvTimeoutError:
                self.connect_status = 0
            try_count += 1
            self.logger.warn(f'Try to connect {self.name} for {try_count} times')
        if not self.connect_status:
            self.logger.error(f'{self.name} connect failed')
            raise ConnectFail()
        return 0

    def turn_on_off_slot(self, on_off: Literal['on','off'] = 'on', delay: float = 1.0, slot: Union[int, None] = None) -> int:
        """
        <a id="driver2">Turn on or turn off slot.</a>

        Args:
            on_off (str): On or Off of slot. Value is `on` or `off`,`on -> turn on slot` and `off -> turn off slot`.
            delay (float): Delay time, it is not necessary to set normally. Defaults to 1.0s
            slot (int, optional): The slot of the DAQ, AWG, MIX. Defaults to 0.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal.
        """
        cmu_slot = const.CMU_SLOT
        # slot = self.slot_check(slot)
        # 此处不改变当前对象的slot值
        slot = self.slot if slot is None else slot 
        slot_status = bytes_to_int(self[cmu_slot,'FUNC.SLOT_POWER_MONITOR'])
        if on_off == 'on':
            self[cmu_slot, 'FUNC.POWER_CTRL'] = (~(1 << slot)) & slot_status
        elif on_off == 'off':
            self[cmu_slot, 'FUNC.POWER_CTRL'] = (1 << slot) | slot_status
        time.sleep(delay)
        return 0
    
    def platform_selfcheck(self, slot: Union[int, None] = None) -> int:
        """
        <a id="driver3">platform self check.</a>

        Returns:
            The program ends normally with return value `0`, otherwise abnormal.
        """

        slot = self.slot_check(slot)
        # 1.CMU对象因为机箱上电后默认cum槽位上电故在对象初始时就完成自检
        # 但是因为机箱上电后除CMU外其他板卡均需要用户手动上下电
        if slot == const.CMU_SLOT:
            # 系统上电后默认CMU槽位上电因此在CMU初始化的时候进行寄存器&内存自检
            self._CmuUnit__fix_reg_rw_selfcheck(fix_reg_list=['CPU.TESTREG', 'UDP.TESTREG'], slot=23) #, 'FUNC.TESTREG'
            self._CmuUnit__ddr_selfcheck(test_type_dict={0:'常规'}, data_type_dict = {0:'全0', 1:'全1'}, addr_list=[0x00000000], slot=23)
        # 2.AWG对象自检
        if slot in const.AWG_SLOTS:
            # 如果该槽位存在刀片 且 该槽位已上电
            # slot in self.active_slot and 
            if not self.__get_slot_power(slot=slot):
                # 'FEEDBACK.TESTREG',功能暂时还没有开发好 该寄存器暂不使用
                self._CmuUnit__fix_reg_rw_selfcheck(fix_reg_list=['CPU.TESTREG','PIPELINE.TESTREG','TRIG.TESTREG',
                                                'AWG_A_1.TESTREG','AWG_A_2.TESTREG','AWG_B_1.TESTREG','AWG_B_2.TESTREG',
                                                'AWG_B_3.TESTREG','AWG_B_4.TESTREG','AWG_B_5.TESTREG','CHIP_CONFIG.TESTREG'], slot=slot)
                self._CmuUnit__ddr_selfcheck(test_type_dict={0:'常规'}, data_type_dict = {0:'全0', 1:'全1'}, addr_list=[0x00000000], slot=slot)
            else:
                raise SlotPowerStatusError(slot=slot)
        # 3.DAQ对象自检
        if slot in const.DAQ_SLOTS:
            # 如果该槽位存在刀片 且 该槽位已上电
            if not self.__get_slot_power(slot=slot):
                self._CmuUnit__fix_reg_rw_selfcheck(fix_reg_list=['DAC_WAVE_0.TESTREG','DAQ_0.WAVE_TRIG_COUNT'], slot=slot)
                self._CmuUnit__ddr_selfcheck(test_type_dict={0:'常规'}, data_type_dict = {0:'全0', 1:'全1'}, addr_list=[0x100000000], slot=slot)
            else:
                raise SlotPowerStatusError(slot=slot)
        # 4.MIX对象自检
        if slot in const.MIX_SLOTS:
            self._MIXUnit__reg_selfcheck(slot=slot)
        return 0
    
    def __write_emmc(self, data: bytes, emmc_addr: int = 0x1400000, ddr_address: int = 0xF0000000, timeout: int = 500, slot: Union[int, None] = None) -> int:
        """
        Write EMMC accroding to 1. Write data to DDR 2. Move data from DDR to EMMC.

        Args:
            data (bytes): bytes data.
            emmc_addr (hexadecimal): EMMC address data written to.
            slot (int): The slot of the crate.
            ddr_address (hexadecimal, optional): DDR address data written to.Defaults to 0x58000000.
            timeout (int, optional): Timeout for write flash. Defaults to 500.

        Raises:
            WriteDDRTimeoutError: Write data to DDR timeout.
            WriteFlashTimeoutError: Move DDR data to flash timeout.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal.
        """
        slot = self.slot_check(slot)
        try_times = 0
        max_times = 5
        while try_times < max_times:
            try:
                self.write_mem(ddr_address, data)
                readback_data = self.read_mem(ddr_address, len(data))[:len(data)]
                if readback_data == data:
                    break
            except RecvTimeoutError:
                self.logger.error(f'Slot {slot} WRITE MEM TO DDR FAIL FOR {try_times+1} time.')
            try_times += 1
            if try_times == max_times:
                raise WriteDDRTimeoutError(slot, max_times)

        self[slot, 'CPU.DDR_ADDR'] = ddr_address
        self[slot, 'CPU.EMMC_ADDR'] = emmc_addr
        self[slot, 'CPU.DATA_LEN'] = len(data)
        self[slot, 'CPU.FUNCTION'] = 0x05
        op_status = self.__check_op_status('CPU.OP_STATUS', 0x00, timeout, slot=slot, console=True)
        if op_status:
            raise WriteFlashTimeoutError(slot, timeout, op_status)
        return 0

    def __read_emmc(self, emmc_addr: int = 0x1400000, length: int = 1024, ddr_address: int = 0xF0000000, timeout: int = 500, slot: Union[int, None] = None) -> bytes:
        """
        Read EMMC data accroding to 1. Move data from EMMC to DDR. 2. Read EMMC data from DDR.

        Args:
            emmc_addr (hexadecimal): Flash address data read from.Defaults to 0x1400000.
            length (int): The length of flash data.Defaults to 1024.
            slot (int): The slot of the crate.
            ddr_address (hexadecimal, optional): The DDR address flash data in.Defaults to 0x58000000.
            timeout (int, optional): Timeout of read flash. Defaults to 1000.

        Raises:
            ReadFlashTimeoutError: Read flash timeout.

        Returns:
            EMMC data.
        """
        slot = self.slot_check(slot)
        self[slot, 'CPU.EMMC_ADDR'] = emmc_addr
        self[slot, 'CPU.DATA_LEN'] = length
        self[slot, 'CPU.DDR_ADDR'] = ddr_address
        self[slot, 'CPU.FUNCTION'] = 0x06
        op_status = self.__check_op_status('CPU.OP_STATUS', 0x00, timeout, slot=slot, console=True)
        if op_status:
            raise ReadFlashTimeoutError(slot, timeout, op_status)
        time.sleep()
        data = self.read_mem(ddr_address, length, slot=slot)[:length]
        return data
    
    def __write_flash(self, addr: int, data: bytes, ddr_address: int = 0xF0000000, timeout: int = 500, slot: Union[int, None] = None) -> int:
        """
        Write flash accroding to 1. Write data to DDR 2. Move data from DDR to flash.

        Args:
            addr (hexadecimal): Flash address data written to.
            data (bytes): bytes data.
            slot (int): The slot of the crate.
            ddr_address (hexadecimal, optional): DDR address data written to.Defaults to 0x58000000.
            timeout (int, optional): Timeout for write flash. Defaults to 500.

        Raises:
            WriteDDRTimeoutError: Write data to DDR timeout.
            WriteFlashTimeoutError: Move DDR data to flash timeout.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal.
        """
        slot = self.slot_check(slot)
        try_times = 0
        max_times = 5
        while try_times < max_times:
            try:
                self.write_mem(ddr_address, data)
                readback_data = self.read_mem(ddr_address, len(data))[:len(data)]
                if readback_data == data:
                    break
            except RecvTimeoutError:
                self.logger.error(f'Slot {slot} WRITE MEM TO DDR FAIL FOR {try_times+1} time.')
            try_times += 1
            if try_times == max_times:
                raise WriteDDRTimeoutError(slot, max_times)
        ddr_addr_reg = 'CPU.DDR_ADDR'
        ddr_len_reg = 'CPU.DATA_LEN'
        flash_addr_reg = 'CPU.FLASH_ADDR'
        func_reg = 'CPU.FUNCTION'

        self[slot, ddr_addr_reg] = ddr_address
        self[slot, flash_addr_reg] = addr
        self[slot, ddr_len_reg] = len(data)
        self[slot, func_reg] = 0x01
        op_status = self.__check_op_status('CPU.OP_STATUS', 0x00, timeout, slot=slot, console=True)
        if op_status:
            raise WriteFlashTimeoutError(slot, timeout, op_status)
        return 0

    def __read_flash(self, addr: int, length: int, ddr_address: int = 0xF0000000, timeout: int = 500, slot: Union[int, None] = None) -> bytes:
        """
        Read flash data accroding to 1. Move data from flash to DDR. 2. Read flash data from DDR.

        Args:
            addr (hexadecimal): Flash address data read from.
            length (int): The length of flash data.
            slot (int): The slot of the crate.
            ddr_address (hexadecimal, optional): The DDR address flash data in.Defaults to 0x58000000.
            timeout (int, optional): Timeout of read flash. Defaults to 1000.

        Raises:
            ReadFlashTimeoutError: Read flash timeout.

        Returns:
            Flash data.
        """
        slot = self.slot_check(slot)
        flash_addr_reg = 'CPU.FLASH_ADDR'
        flash_len_reg = 'CPU.DATA_LEN'
        ddr_addr_reg = 'CPU.DDR_ADDR'
        func_reg = 'CPU.FUNCTION'

        self[slot, flash_addr_reg] = addr
        self[slot, flash_len_reg] = length
        self[slot, ddr_addr_reg] = ddr_address
        self[slot, func_reg] = 0x02
        op_status = self.__check_op_status('CPU.OP_STATUS', 0x00, timeout, slot=slot, console=True)
        if op_status:
            raise ReadFlashTimeoutError(slot, timeout, op_status)
        data = self.read_mem(ddr_address, length, slot=slot)[:length]
        return data

    def __write_eeprom(self, data: bytes, ddr_address: int = 0xD0000000, timeout: int = 500, slot: Union[int, None] = None) -> int:
        slot = self.slot_check(slot)
        try_times = 0
        max_times = 5
        while try_times < max_times:
            try:
                self.write_mem(ddr_address, data)
                readback_data = self.read_mem(ddr_address, len(data))[:len(data)]
                if readback_data == data:
                    break
            except RecvTimeoutError:
                self.logger.error(f'Slot {slot} WRITE MEM TO DDR FAIL FOR {try_times+1} time.')
            try_times += 1
            if try_times == max_times:
                raise WriteDDRTimeoutError(slot, max_times)
        self[slot, 'CPU.DDR_ADDR'] = ddr_address
        self[slot, 'CPU.DATA_LEN'] = len(data)
        self[slot, 'CPU.FUNCTION'] = 0x05
        op_status = self.__check_op_status('CPU.EEPROM_STATUS', 0x00, timeout, slot, console=True)
        if op_status:
            raise WriteEepromTimeoutError(slot, timeout, op_status)
        return 0

    def __read_eeprom(self, length: int, ddr_address: int = 0xD0000000, timeout: int = 500, slot: Union[int, None] = None) -> list:
        slot = self.slot_check(slot)
        self[slot, 'CPU.DDR_ADDR'] = ddr_address
        self[slot, 'CPU.DATA_LEN'] = length
        self[slot, 'CPU.FUNCTION'] = 0x06
        op_status = self.__check_op_status('CPU.EEPROM_STATUS', 0x00, timeout, slot=slot, console=True)
        if op_status:
            raise ReadEepromTimeoutError(slot, timeout, op_status)
        data = self.read_mem(ddr_address, length, slot=slot)[:length]
        return data

    def remote_config(self, file_path: str, slot: Union[int, None] = None) -> int:
        """
        <a id="driver4">Remote update of FPGA logic</a>

        Args:
            file_path (str): Bin file path
            slot (int, optional): The slot number of the CMU,AWG,DAQ,MIX board. Defaults to `None`.

        Raises:
            BinFileNotFoundError: The bin file not found error
            FlashDataNotMatch: The Flash Data not match

        Returns:
            The program ends normally with return value `0`, otherwise abnormal.
        """
        slot = self.slot_check(slot)
        if not os.path.exists(file_path):
            raise BinFileNotFoundError
        with open(file_path, 'rb') as f:
            bin_data = f.read()

        if slot in const.AWG_SLOTS or slot == const.CMU_SLOT:
            config_addr = 0x00000000
            pad_cnt = (1024 - (len(bin_data) & 0x3FF)) & 0x3FF
            bin_data += b'0' * pad_cnt
            self.__write_flash(addr = config_addr, data = bin_data, slot = slot)
            flash_data = self.__read_flash(addr = config_addr, length = len(bin_data), slot = slot)
            if flash_data != bin_data:
                raise FlashDataNotMatch(slot)
        elif slot in const.DAQ_SLOTS:
            ddr_address = 0x100000000
            pad_cnt = (1024 - (len(bin_data) & 0x3FF)) & 0x3FF
            bin_data += b'0' * pad_cnt
            try_times = 0
            max_times = 5
            while try_times < max_times:
                try:
                    self.write_mem(ddr_address, bin_data)
                    readback_data = self.read_mem(ddr_address, len(bin_data))[:len(bin_data)]
                    if readback_data == bin_data:
                        break
                    else:
                        raise DDRDataNotMatch(slot)
                except RecvTimeoutError:
                    self.logger.error(f'Slot {slot} WRITE MEM TO DDR FAIL FOR {try_times+1} time.')
                except DDRDataNotMatch:
                    self.logger.error(f'Slot {slot} WRITE MEM TO DDR FAIL FOR {try_times+1} time.')
                try_times += 1
                if try_times == max_times:
                    raise WriteDDRTimeoutError(slot, max_times)
            self._DAQUnit__config_fpga_update(ddr_addr=ddr_address,flash_addr=0x00000000,length=len(bin_data),direct=0,slot=slot)
            self._DAQUnit__set_interrupt(slot=slot)
            self.__update_process(status_reg='STATUS.UPDATE_PROCESS', target_status=100, max_value=100, slot=slot, console=True)
        return 0
    
    def config_platform_params(self, slot: Union[int, None] = None, **kwargs) -> int:
        """
        Config platform paramters

        Args:
            slot (int, optional): The slot number of the CMU,AWG,DAQ,MIX board. Defaults to `None`.

        Raises:
            BinFileNotFoundError: Bin File Not Found Error
            EepromDataNotMatch: Eeprom Data Not Match
            IllegalIpAddressError: Illegal Ip Address Error

        Returns:
            The program ends normally with return value `0`, otherwise abnormal.
        """

        if 'file_path' in kwargs.keys():
            if not os.path.exists(kwargs.get('file_path')):
                raise BinFileNotFoundError
            with open(kwargs.get('file_path'), 'rb') as f:
                bin_data = f.read()
            pad_cnt = (1024 - (len(bin_data) & 0x3FF)) & 0x3FF
            bin_data += b'0' * pad_cnt
            self.__write_eeprom(data = bin_data, slot = slot)
            eeprom_data = self.__read_eeprom(length = len(bin_data), slot = slot)
            if eeprom_data != bin_data:
                raise EepromDataNotMatch(slot)

        if 'monitor_ip' in kwargs.keys() and 'monitor_port' in kwargs.keys():
            self.__set_monitor_ip(monitor_ip=kwargs.get('monitor_ip'),port=kwargs.get('monitor_port'))

        return 0

    def re_connect(self, wait_time: int = 15) -> int:
        """
        reconnect device

        Args:
            wait_time (int, optional): reconnect device wait time. Defaults to 15.

        Raises:
            InitDeviceFail: Fail to init device
            ConnectFail: Fail to connect device

        Returns:
            The program ends normally with return value `0`, otherwise abnormal.
        """
        slot = const.CMU_SLOT
        time.sleep(wait_time)
        self.connect_status = 0
        try:
            self[slot, 'CPU.PERMISSION'] = 1
            if bytes_to_int(self[slot, 'CPU.PERMISSION']) != 1:
                raise InitDeviceFail(slot)
        except RecvTimeoutError or InitDeviceFail:
            raise ReConnectFail
        self.connect_status = 1
        return 0

    def __get_slots_power(self) -> list:
        """
        Gets the status of the specified slot up and down

        Args:
            slot (int): The slot of the create

        Returns:
            whether the slot is powered up(0) and down(1)
        """
        # 1.机箱各槽位板卡上下电状态信息
        # 2.读取CMU硬件固件CMU_FUNC模块SLOT_POWER_MONITOR寄存器（[0x30000, 0x4C]）
        # 3.bit[22:0]板卡槽位编号: 0-20:槽位0-20,21：时钟,22：反馈,[23]上下电信息:1 -> 板卡未上电,0 -> 板卡上电,上下电命令操作间隔至少1s，防止后续上下电指令过快，导致电源冲击
        cmu_slot = const.CMU_SLOT
        # 此处由FUNC.POWER_CTRL改为FUNC.SLOT_POWER_MONITOR
        power_monitor_reg = 'FUNC.SLOT_POWER_MONITOR'
        slots_power_status = bytes_to_int(self[cmu_slot, power_monitor_reg])
        return [get_bit(slots_power_status, i) for i in range(21)]

    def __get_slot_power(self, slot: int) -> int:
        """
        Gets the status of the specified slot up and down

        Args:
            slot (int): The slot of the create

        Returns:
            whether the slot is powered up(0) and down(1)
        """
        cmu_slot = const.CMU_SLOT
        # 此处由FUNC.POWER_CTRL改为FUNC.SLOT_POWER_MONITOR
        power_monitor_reg = 'FUNC.SLOT_POWER_MONITOR'
        slots_power_status = bytes_to_int(self[cmu_slot, power_monitor_reg])
        slot_power_status = get_bit(slots_power_status, slot)
        return slot_power_status

    def __set_slot_power(self, power_status: int, slot: Union[int, None]=None) -> int:
        """
        slot power turn on / turn off

        Args:
            power_status : turn on value in(1,True,'on') or turn off(1,False,'off')
            slot (int, optional): The slot of the crate. Defaults to 0.
        Raises:
            ChannelWrongError: Input the wrong channel number.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal.
        """
        time.sleep(1)
        cmu_slot = const.CMU_SLOT
        slot = self.slot_check(slot)
        slot_status = bytes_to_int(self[cmu_slot,'FUNC.SLOT_POWER_MONITOR'])
        power_dict = {1:(~(1 << slot)) & slot_status,
                      True:(~(1 << slot)) & slot_status,
                      'on':(~(1 << slot)) & slot_status,
                      0:(1 << slot) | slot_status,
                      False:(1 << slot) | slot_status,
                      'off':(1 << slot) | slot_status}
        if power_status in power_dict.keys():
            self[cmu_slot, 'FUNC.POWER_CTRL'] = power_dict.get(power_status)
        return 0

    def __turn_on_slot(self, slot=None, delay: float = 1.0) -> int:
        """turn on slot

        Args:
            slot (int, optional): The slot of the create. Defaults to 0.
            delay (float): Delay time. Defaults to 1.0s
        Raises:
            ChannelWrongError: Input the wrong channel number.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal.
        """
        cmu_slot = const.CMU_SLOT
        slot = self.slot_check(slot)
        slot_status = bytes_to_int(self[cmu_slot,'FUNC.SLOT_POWER_MONITOR'])
        self[cmu_slot, 'FUNC.POWER_CTRL'] = (~(1 << slot)) & slot_status
        time.sleep(delay)
        return 0

    def __turn_off_slot(self, slot: Union[int, None] = None, delay: float = 1.0) -> int:
        """
        turn off slot

        Args:
            slot (int, optional): The slot of the create. Defaults to 0.
            delay (float): Delay time. Defaults to 1.0s
        Raises:
            ChannelWrongError: Input the wrong channel number.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal.
        """
        cmu_slot = const.CMU_SLOT
        slot = self.slot_check(slot)
        slot_status = bytes_to_int(self[cmu_slot,'FUNC.SLOT_POWER_MONITOR'])
        self[cmu_slot, 'FUNC.POWER_CTRL'] = (1 << slot) | slot_status
        time.sleep(delay)
        return 0  

    def __slot_reset(self, slot: Union[int, None] = None) -> int:
        reset_reg = 'CPU.FUNCTION'
        slot = self.slot_check(slot)
        self[slot, reset_reg] = 0x09
        if slot != const.CMU_SLOT:
            hardwave_ready_bytes = self[slot, 'CPU.HARDWARE_RDY']
            hardware_ready = bytes_to_int(hardwave_ready_bytes)
        else:
            self[slot, 'CPU.PERMISSION'] = 1
            permission_bytes = self[slot, 'CPU.PERMISSION']
            hardware_ready = bytes_to_int(permission_bytes)
        if hardware_ready != 1:
            raise RebootFail(slot)
        return 0

    def __init_slot(self, slot: Union[int, None] = None) -> int:
        init_reg = 'CPU.FUNCTION'
        slot = self.slot_check(slot)
        self[slot, init_reg] = 0x08
        hardware_ready = 0
        if slot != const.CMU_SLOT:
            hardwave_ready_bytes = self[slot, 'CPU.HARDWARE_RDY']
            hardware_ready = bytes_to_int(hardwave_ready_bytes)
        else:
            self[slot, 'CPU.PERMISSION'] = 1
            permission_bytes = self[slot, 'CPU.PERMISSION']
            hardware_ready = bytes_to_int(permission_bytes)
        if hardware_ready != 1:
            raise InitDeviceFail(slot)
        return 0
    
    def __check_op_status(self, status_reg, target_status, timeout: int, slot: Union[int, None] = None, console: bool = False) -> int:
        """
        Check cpu op_status register.

        Args:
            slot (int): The slot of the crate.
            timeout (float): Timeout for check cpu op_status.

        Returns:
            Cpu op status register value.
        """
        waited_time = 0
        time_interval = 1
        op_status = None
        slot = self.slot_check(slot)
        response_timeout = self.RESPONSE_TIMEOUT
        self.RESPONSE_TIMEOUT = 60
        if console:
            pbar = ProgressBar(max=timeout, hint=f'{self.name} CHECK OP STATUS')
            pbar.start()
        while waited_time < timeout:
            op_status = bytes_to_int(self[slot, status_reg])
            if op_status == target_status:
                if console:
                    pbar.update(timeout-waited_time)
                self.RESPONSE_TIMEOUT = response_timeout
                break
            time.sleep(time_interval)
            waited_time += time_interval
            if console:
                pbar.update(time_interval)
        return op_status
    
    def __update_process(self, status_reg, target_status, max_value: int, slot: Union[int, None] = None, console: bool = False) -> int:
        """
        DAQ update process.

        Args:
            slot (int): The slot of the crate.
            timeout (float): Timeout for check cpu op_status.

        Returns:
            Cpu op status register value.
        """
        cur_value = 0
        time_interval = 1
        slot = self.slot_check(slot)
        if console:
            pbar = progressbar.ProgressBar(maxval=max_value, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
            pbar.start()

        while True:
            cur_value = bytes_to_int(self[slot, status_reg])
            if cur_value != 0xffffffff:
                break
            time.sleep(1)

        while cur_value <= max_value:
            cur_value = bytes_to_int(self[slot, status_reg])
            if cur_value == target_status:
                if console:
                    pbar.update(cur_value)
                break

            time.sleep(time_interval)
            if console:
                pbar.update(cur_value)

        pbar.finish()
        return cur_value

    def __fan_control(self,fan1_speed: int = 30,fan2_speed: int = 30) -> int:
        """
        Upper and lower fan control of the chassis

        Args:
            fan1_speed (int): Upper fan speed ratio, value in 0-100.Default 30.
            fan2_speed (int): Upper fan speed ratio, value in 0-100.Default 30.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal.
        """
        fan1_register = 'FUNC.FAN_CTRL1'
        fan2_register = 'FUNC.FAN_CTRL2'
        self[const.CMU_SLOT, fan1_register] = int(fan1_speed)
        self[const.CMU_SLOT, fan2_register] = int(fan2_speed)
        return 0

    def __temperature_control(self, temperature: float) -> int:
        """
        Thermal management control

        Args:
            temperature (float): User setting temperature

        Returns:
            The program ends normally with return value `0`, otherwise abnormal.
        """
        slot = const.CMU_SLOT
        temp_control_reg = 'FUNC.TEMP_CONTROL'
        self[slot, temp_control_reg] = float(temperature)
        return 0

    def __read_hardware_info(self, slot: Union[int, None] = None) -> int:
        """
        Read device parameters

        Args:
            slot (int, optional): The slot number of the CMU,AWG,DAQ,MIX board. Defaults to `None`.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal.
        """
        start_address = 0xD0000000
        # TODO: document is not completed yet
        pass

    def __load_hardware_info(self, slot: Union[int, None] = None) -> int:
        """
        Load device parameters

        Args:
            slot (int, optional): The slot number of the CMU,AWG,DAQ,MIX board. Defaults to `None`.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal.
        """
        slot = self.slot_check(slot)
        self[slot, 'CPU.LOAD_CONFIG'] = 0x01
        return 0

    def __set_hardware_info(self, file_path: str, slot: Union[int, None] = None) -> int:
        """
        Device parameter configuration

        Args:
            file_path (str): Bin file path
            slot (int, optional): The slot number of the CMU,AWG,DAQ,MIX board. Defaults to `None`.

        Raises:
            BinFileNotFoundError: The bin file not found error
            EepromDataNotMatch: The eeprom data not match error

        Returns:
            The program ends normally with return value `0`, otherwise abnormal.
        """
        if not os.path.exists(file_path):
            raise BinFileNotFoundError
        with open(file_path, 'rb') as f:
            bin_data = f.read()
        pad_cnt = (1024 - (len(bin_data) & 0x3FF)) & 0x3FF
        bin_data += b'0' * pad_cnt
        self.__write_eeprom(bin_data, slot)
        eeprom_data = self.__read_eeprom(len(bin_data), slot)
        if eeprom_data != bin_data:
            raise EepromDataNotMatch(slot)
        # print(f'Slot {slot} REMOTE CONFIG PROCESS END, SUCCESS!')
        return 0

    def __set_monitor_ip(self, monitor_ip: str, port: int = 7000, slot: Union[int, None]=None) -> int:
        """
        Set da monitor ip address

        Args:
            monitor_ip (str): Da monitor ip address.
            port (int): Da monitor port.
            slot (int, optional): The slot of the crate. Defaults to 0.

        Raises:
            IllegalIpAddressError: Ip address is illegal.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal.
        """
        compile_ip = re.compile(r'^(172|10)\.'
                                r'(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.'
                                r'(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.'
                                r'(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
        if not compile_ip.match(monitor_ip):
            raise IllegalIpAddressError(monitor_ip)
        monitor_address_reg = 'CPU.MONITOR_IP'
        port_reg = 'CPU.MONITOR_PORT'
        enable_reg = 'CPU.STATUS_EN'

        slot = self.slot_check(slot)
        self[slot, monitor_address_reg] = ip_to_int(monitor_ip)
        self[slot, port_reg] = port
        self[slot, enable_reg] = 1
        return 0

    def __monitor_enable(self, enable_status, slot=None):
        enable_reg = 'CPU.STATUS_EN'
        slot = self.slot_check(slot)
        self[slot, enable_reg] = enable_status
        return 0
