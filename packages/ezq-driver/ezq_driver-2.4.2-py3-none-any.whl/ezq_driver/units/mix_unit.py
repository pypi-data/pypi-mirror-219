# coding: utf-8
# ezq_driver/units/cmu_unit.py


__all__ = ['set_pump_params',
           'set_pump_on_off']

from ..utils import bytes_to_int
from .cmu_unit import CmuUnit
from ..constant import const
from ..error import mix_error
import time
import warnings
from typing import Union, List, Literal

class MIXUnit(CmuUnit):
    """
    该单元是ez-Q2.0产品混频子模块, 允许用户直接控制混频模块的各项功能.

    Examples:
        >>> from ezq_driver.driver import EzqDevice
        >>> pump = EzqDevice(ip = '10.0.9.11', slot = 23, console_log = True, batch_mode = False)
        >>> pump.connect()
        >>> pump.set_pump_params(channel = 1, frequency = 8e9, amplitude = 15, mix_type = 'mix1', slot = 16)
        0
        >>> set_pump_on_off(channel = 1, on_off='on', slot = 16)
        0

    该模块包含以下函数:

        - <a href="#pump1">***set_pump_params(channel, frequency, amplitude, mix_type, slot)***</a> - Configure Mr. Chen Lin's mix or Mr. Zhang Qingyuan's board pump 
        - <a href="#pump2">***set_pump_on_off(channel, on_off, slot)***</a> - Enable or disable mix
        </br>
        *****************************************************************************************************************************************
        
    """

    def __init__(self, ip, port=10000, slot=5, name='', logger=None, console_log=False, dev_mode=False, batch_mode=True):
        super().__init__(ip, port, slot, name, logger, console_log, dev_mode, batch_mode)

        self.Mix_Daq_Bind = {5:4,16:15}
        self.Mix_Board_Select = None

    def __channel_check(self, channel: int):
        if channel < const.MIX_MIN_CHANNEL_AMOUNT or channel > const.MIX_MAX_CHANNEL_AMOUNT:
            raise mix_error.MixChannelWrongError(self.slot, channel)

    def __check_params(func):
        """
        User input parameter validation

        Note:
        We have defined a decorator function called check_params that accepts a function as input. Within the decorator, a wrapper function is defined to implement the logic for parameter validation. 
        The wrapper function takes variable-length parameters *args and compares them with the previous set of parameters. If the parameters are different, the decorated function func is executed. 
        Otherwise, a message indicating that the parameters are the same is warning.

        Args:
            func (Callable): The decorated function `func`.
        """
        last_params = None # 全局变量，记录上一次的参数
        def wrapper(*args):
            nonlocal last_params
            if last_params is None or args != last_params:
                last_params = args
                return func(*args)
            else:
                warnings.warn(f"The current set of parameters is the same as the historical parameters:{args}")
        return wrapper
    
    def __reg_selfcheck(self, slot: Union[int, None] = None) -> int:
        slot = self.slot_check(slot)
        if self.Mix_Board_Select == 'mix1':
            try:
                reg = 'MIX.WORK_STATUS'
                status = bytes_to_int(self[slot, reg])
            except:
                self.logger.error(f"Slot:{slot}, self-check failed, write and read communication abnormally!")
                raise mix_error.MixRegisterWriteAndReadError(slot)
            
            reference_bit = status & 1
            pump_l1_bit = (status >> 1) & 1
            pump_l2_bit = (status >> 2) & 1
            mix_bit = (status >> 3) & 1
            if not reference_bit:
                raise mix_error.MixSelfCheckError(slot,'基准源工作状态:故障!')
            if not pump_l1_bit:
                raise mix_error.MixSelfCheckError(slot,'泵浦源一本振工作状态:故障!')
            if not pump_l2_bit:
                raise mix_error.MixSelfCheckError(slot,'泵浦源二本振工作状态:故障!')
            if not mix_bit:
                raise mix_error.MixSelfCheckError(slot,'变频本振工作状态:故障!')
        elif self.Mix_Board_Select == 'mix2': 
            try:
                reg = 'MIX2.TEMP'
                temp = bytes_to_int(self[slot, reg])
                if temp <= 0 or temp >= 100:
                   raise mix_error.MixSelfCheckError(slot,'温度读取值异常!')
            except:
                raise mix_error.MixRegisterWriteAndReadError(slot)
        else:
            raise mix_error.MixTypeWrongError(self.name, self.Mix_Board_Select)
        return 0   

    @__check_params # 与历史参数校验，如果相同则不运行函数，否则运行程序
    def set_pump_params(self, channel: int, frequency: float, amplitude: Union[int,float], mix_type: Literal['mix1','mix2'] = 'mix1',amplitude_type:Literal['norm','dbm','code'] = 'norm', slot: Union[int, None] = None) -> int:
        """
        <a id="pump1">Set mix board paramters</a>

        Notes:
            For mix1(张清远), the DDS output amplitude adopts 14-bit bit coding and the coding range is 0~16383, 
            so we establish a linear relationship between the amplitude encoding and the absolute output power 0 ~ 15dBm.
            For amplitude_type is `norm`, The formula is : value = int(16383 * amplitude), the user input power range in `0 ~ 1`, 
            and the linear output is 0 ~ 16383 
            For amplitude_type is `dbm`, The formula is : value = 16383 * amplitude / 15, Among them, the user input power range in `0 ~ 15dBm`, 
            and the linear output is 0 ~ 16383.
            For amplitude_type is `code`, The user directly inputs the power encoding value range in `0 ~ 16383`.

            For mix2(陈林), we establish a linear relationship between the absolute output amplitude with the register decimal setpoint of `-1100 ~ -300`, 
            For amplitude_type is `norm`, The formula is : value = int(-1100 + 800 * power), the user input power range in `0 ~ 1`, the linear output is `-1100 ~ -300`.
            For amplitude_type is `dbm`,The formula is : value = -1100 + 800 * power / 15, the user input power amplitude in `0 ~ 15dBm`, the linear output is `-1100 ~ -300`.
            For amplitude_type is `code`, The user directly inputs the power encoding value range in `-1100 ~ -300`.
            Of course, in later versions, we will establish accurate numerical mapping relationship between absolute power and output.

        Args:
            channel (int): The channel number that is actually marked on the MIX board. Value range in `1 - 4`.
            frequency (int): The frequency is the user's actual expectation that the output frequency exceeds the mix frequency range, the unit is Hz.
            amplitude (int,float): The output power amplitude. value range in `0 ~ 15` and unit is dBm.
            slot (int, optional): The slot number of the MIX board. Value in list `[5, 16]`. Defaults to `None`.
            amplitude_type (str): The amplitude type. If the value is `norm`, the amplitude range is `0 ~ 1`,If the value is `dbm`, the amplitude range is `0 ~ 15`,If the value is `norm`, the amplitude range is `0 ~ 16383` or `-1100 ~ -300`.Defaults to `norm`.
            mix_type (str): The mix type that user select. The value in `['mix1', 'mix2']` and `mix1 -> 张清远` or `mix2 -> 陈琳`.

        Raises:
            MixChannelWrongError: Mix channel wrong error.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal
        """

        self.__channel_check(channel)
        mix_slot = self.slot_check(slot)
        # MIX和DAQ对应板卡绑定MIX:5 -> DAQ:4, MIX:16 -> DAQ:15
        daq_slot = self.Mix_Daq_Bind[mix_slot]
        if mix_type == 'mix1': # mix1 张清远
            # self.__daq_dds_channel_sel(channel, slot = daq_slot)
            # self.__daq_dds_freq(frequency, slot = daq_slot)
            # self.__daq_dds_amp(amplitude, 0, amplitude_type, daq_slot)
            if frequency <= 1.25e9: # 根据用户输入频率确定为普通模式
                # self.__daq_dds_mode(mode = 0, slot = daq_slot)
                self.__set_dds_output(channel=channel, mode=0, frequency=frequency, amplitude=amplitude, slot=slot)
            elif frequency > 1.25e9: # 根据用户输入频率确定为混频模式
                # self.__daq_dds_mode(mode = 1, slot = daq_slot)
                self.__set_dds_output(channel=channel, mode=1, frequency=frequency, amplitude=amplitude, slot=slot)
            # 设置张清远混频频率，该槽位号是混频板子的槽位号[5,16]
            self.__set_mix_frequency(frequency, mix_slot)
            self.Mix_Board_Select = 'mix1'
        else: # mix2 陈琳
            self.__set_pump_freq(channel, frequency, mix_slot)
            self.__set_pump_power(channel, amplitude , amplitude_type, mix_slot)
            self.Mix_Board_Select = 'mix2'
        return 0
    
    @__check_params # 与历史参数校验，如果相同则不运行函数，否则运行程序
    def set_pump_on_off(self, channel: int, on_off: Literal['on','off'] = 'on', slot: Union[int, None] = None) -> int:
        """
        <a id="mix2">Enable or disable mix board</a>

        Args:
            channel (int): The channel number that is actually marked on the MIX board. Value range in `1 - 4`.
            on_off (str): The Flag of enable / disable mix. Value is `on` or `off`,`on -> start` and `off -> stop`.
            slot (int, optional): The slot number of the MIX board. Value in list `[5, 16]`. Defaults to `None`.

        Raises:
            MixTypeWrongError: Mix type wrong error.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal
        """

        if on_off == 'on':
            self.__set_mix_enable(channel, slot)
        else:
            self.__set_mix_disable(channel, slot)
        return 0
    
    def __set_mix_enable(self, channel: int, slot: Union[int, None] = None) -> int:
        """
        Enable mix

        Args:
            channel (int): The channel number that is actually marked on the MIX board. Value range in `1 - 4`.
            slot (int, optional): The slot number of the MIX board. Value in list `[5, 16]`. Defaults to `None`.

        Raises:
            MixTypeWrongError: Mix type wrong error.
            MixChannelWrongError: Mix channel wrong error.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal
        """
        self.__channel_check(channel)
        mix_slot = self.slot_check(slot)
        # MIX和DAQ对应板卡绑定MIX:5 -> DAQ:4, MIX:16 -> DAQ:15
        daq_slot = self. Mix_Daq_Bind[mix_slot]
        if self.Mix_Board_Select == 'mix1':
            # self.__daq_dds_update(daq_slot)
            self.__set_interrupt(slot=daq_slot)
        elif self.Mix_Board_Select == 'mix2':
            self.__enable_pump(channel,True,mix_slot)
        else:
            raise mix_error.MixTypeWrongError(self.name, self.Mix_Board_Select)
        return 0
    
    def __set_mix_disable(self, channel: int, slot: Union[int, None] = None) -> int:
        """
        Disable mix

        Args:
            channel (int): The channel number that is actually marked on the MIX board. Value range in `1 - 4`.
            slot (int, optional): The slot number of the MIX board. Value in list `[5, 16]`. Defaults to `None`.

        Raises:
            MixTypeWrongError: Mix type wrong error.
            MixChannelWrongError: Mix channel wrong error.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal
        """
        self.__channel_check(channel)
        mix_slot = self.slot_check(slot)
        # MIX和DAQ对应板卡绑定MIX:5 -> DAQ:4, MIX:16 -> DAQ:15
        daq_slot = self. Mix_Daq_Bind[mix_slot]  
        if self.Mix_Board_Select == 'mix1':
            # self.__daq_dds_mode(mode = 2, slot = daq_slot)
            # self.__daq_dds_update(slot = daq_slot)
            self.__set_dds_output(channel=channel, mode=2, frequency=0, amplitude=0, slot=slot)
            self.__set_interrupt(slot=daq_slot)
        elif self.Mix_Board_Select == 'mix2': 
            self.__enable_pump(channel,False,mix_slot)
        else:
            raise mix_error.MixTypeWrongError(self.name, self.Mix_Board_Select)
        return 0  

    def __set_mix_frequency(self, frequency: int, slot: Union[int, None] = None) -> int:
        """
        Set the output frequency of Mr. Zhang Qingyuan's mix board

        Note:
            Because Mr. Zhang Qingyuan's mixing board uses KHz as the basic input unit, 
            the user input Hz unit data needs to be converted to KHz units, 
            so user input data need to dividing by 1000 within the program

        Args:
            frequency (int): Frequency is 32-bit, data type is int, value range is `5.4e9Hz~5.7e9Hz`, minimum frequency step is `1KHz`
            slot (int, optional): The slot number of the MIX board. Value in list `[5, 16]`. Defaults to `None`.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal
        """
        slot = self.slot_check(slot)
        frequency = int(frequency / 1000)
        reg = f'MIX.FREQ'
        self.set_reg(slot, reg, frequency)
        return 0

    def __get_mix_work_status(self, slot: Union[int, None] = None) -> int:
        """
        Get work status of Mr. Zhang Qingyuan's mix board

        Args:
            slot (int, optional): The slot number of the MIX board. Value in list `[5, 16]`. Defaults to `None`.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal
        """
        slot = self.slot_check(slot)
        reg = 'MIX.WORK_STATUS'
        status = bytes_to_int(self[slot, reg])
        reference_bit = status & 1
        pump_l1_bit = (status >> 1) & 1
        pump_l2_bit = (status >> 2) & 1
        mix_bit = (status >> 3) & 1
        status_info = {}
        status_info['基准源工作状态'] = '正常' if reference_bit == 1 else '故障'
        status_info['泵浦源一本振工作状态'] = '正常' if pump_l1_bit == 1 else '故障'
        status_info['泵浦源二本振工作状态'] = '正常' if pump_l2_bit == 1 else '故障'
        status_info['变频本振工作状态'] = '正常' if mix_bit == 1 else '故障'
        return status_info
    
    def __daq_dds_update(self, slot: Union[int, None] = None) -> int:
        """
        Generate DDS configuration interrupt.Set the lowest bit to 1 to enable DDS configurations

        Args:
            slot (int, optional): The slot number of the MIX board. Value in list `[5, 16]`. Defaults to `None`.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal
        """
        slot = self.slot_check(slot)
        reg = 'DDS.REG2MICR_INTR'
        self.set_reg(slot, reg, 0x0000)
        time.sleep(1)
        self.set_reg(slot, reg, 0x0001)
        return 0

    def __daq_dds_channel_sel(self, channel: int, slot: Union[int, None] = None) -> int:
        """
        Set DDS effective channel

        Args:
            channel (int): The channel number that is actually marked on the MIX board. Value range in `1 - 4`.
            slot (int, optional): The slot number of the MIX board. Value in list `[5, 16]`. Defaults to `None`.
        
        Raises:
            MixChannelWrongError: Mix channel wrong error.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal
        """
        self.__channel_check(channel)
        slot = self.slot_check(slot)
        reg = 'DDS.CHANNEL_SEL'
        if channel >= 1 and channel <= 4:
            self.set_reg(slot,reg,(1 << (channel + 3)))
        else:
            self.set_reg(slot, reg, 0xF0) 
        return 0

    def __daq_dds_mode(self, mode:int = 0, slot: Union[int, None] = None) -> int:
        """
        Set DDS working mode

        Args:
            mode (int): 0 means normal mode=0x000000C (output frequency<1.25GHZ), 1 means mixing mode=0x00050C (output frequency>1.25GHZ), 2 means closing channel=0x02000C0
            slot (int, optional): The slot number of the MIX board. Value in list `[5, 16]`. Defaults to `None`.
        
        Raises:
            ValueError: Input the wrong mode number.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal
        """
        slot = self.slot_check(slot)
        reg = 'DDS.CHANNEL_FUNCL'
        if mode == 0:
            self.set_reg(slot, reg, 0x00000C)
        elif mode == 1:
            self.set_reg(slot, reg, 0x00050C)
        elif mode == 2:
            self.set_reg(slot, reg, 0x02000C)
        else:
            raise ValueError("设置DDS工作模式参数错误(0:普通模式,1:混频模式,2:关闭通道)")
        return 0

    def __daq_dds_freq(self, frequency: int, slot: Union[int, None] = None) -> int:
        """
        Set DDS output frequency

        Args:
            frequency (int): frequency is the user's actual expectation that the output frequency exceeds the DDS frequency range, the unit is Hz.
            slot (int, optional): The slot number of the MIX board. Value in list `[5, 16]`. Defaults to `None`.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal
        """
        slot = self.slot_check(slot)
        freq = frequency % 100e6 + 1.9e9 # frequency为用户实际期望输出频率超过DDS频率范围，故操作保留MHz数据并加入DDS的1.9GHz~2.0GHz范围中作为激励输出给mix
        freq_int = int(freq / 2.5e9*2**48)
        reg_high = 'DDS.FREQ_TUNING_WORD_H'
        reg_low = 'DDS.FREQ_TUNING_WORD_L'
        freq_low = freq_int & 0xFFFFFFFF
        freq_high = (freq_int >> 32) & 0xFFFF
        self.set_reg(slot, reg_high, freq_high)
        self.set_reg(slot, reg_low, freq_low)
        return 0

    def __daq_dds_amp(self, amplitude:float, phase:int = 0, amplitude_type: Literal['norm','dbm','code'] = 'norm', slot: Union[int, None] = None) -> int:
        """
        Set DDS output amplitude

        Note:
            In this drive, the DDS output amplitude adopts 14-bit bit coding and the coding range is 0~16383, 
            so we establish a linear relationship between the amplitude encoding and the absolute output power `0 ~ 15dBm`.
            The formula is : value = 16383 * amplitude / 15, Among them, the user input power range in 0 ~ 15 and unit is dBm, 
            and the linear output is 0 ~ 16383.

        Args:
            amplitude (float): Output power amplitude range in 0 ~ 15dBm
            phase (int): phase
            slot (int, optional): The slot number of the MIX board. Value in list `[5, 16]`. Defaults to `None`.

        Raises:
            PumpPowerOutOfRange: Pump power out of range.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal
        """
        slot = self.slot_check(slot)

        if amplitude_type=='norm' and (amplitude < 0 or amplitude > 1):
            raise mix_error.PumpPowerOutOfRange(self.name,0,1,amplitude)
        elif amplitude_type=='dbm' and (amplitude < 0 or amplitude > 15):
            raise mix_error.PumpPowerOutOfRange(self.name,0,15,amplitude)
        elif amplitude_type=='code' and (amplitude < 0 or amplitude > 16383):
            raise mix_error.PumpPowerOutOfRange(self.name,0,15,amplitude)
        reg = 'DDS.PHASE_AMPLITUDE_CTRL'
        phase = int(phase)
        if amplitude_type == 'norm':
            value = int(16383 * amplitude)
            amp = (phase << 16) | value
            self.set_reg(slot, reg, amp)
        elif amplitude_type == 'dbm':
            value = int(16383 * amplitude / 15)
            amp = (phase << 16) | value
            self.set_reg(slot, reg, amp)
        elif amplitude_type == 'code':
            value = int(amplitude)
            amp = (phase << 16) | value
            self.set_reg(slot, reg, amp)

        return 0

    def set_pump_LO_frequency(self, frequency: int, slot: Union[int, None] = None, delay: float = 0.02) -> int:
        """
        Set up and down Mr. Chen Lin's mix frequency local oscillator

        Note:
            Because Mr. Chen Lin's mix board uses KHz as the basic input unit, the user input Hz unit data needs to 
            be converted to KHz units, so user input data need to dividing by 1000 within the program

        Args:
            frequency (int): Frequency is 32-bit, data type is int, decimal value range is `5.4e9Hz~5.7e9Hz`, minimum frequency step is `1KHz`
            slot (int, optional): The slot number of the MIX board. Value in list `[5, 16]`. Defaults to `None`.
            delay (float, optional) : Set the delay parameter to ensure normal transmission and response
        Raises:
            PumpFrequencyOutOfRange: Pump frequency out of range.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal
        """
        slot = self.slot_check(slot)
        self.value_validate(value = frequency, v_min = 5.4e9, v_max = 5.7e9, 
                            error_class = mix_error.PumpFrequencyOutOfRange)
        reg = f'MIX2.FREQ'
        value = int(frequency / 1000)
        self.set_reg(slot,reg,value)
        time.sleep(delay)
        return 0

    def __set_pump_freq(self, channel: int, frequency: int = 7e9, slot: Union[int, None] = None, delay: float = 0.02) -> int:
        """
        Set Mr. Chen Lin's mix frequency of the PUMP signal

        Note:
            Because Mr. Chen Lin's mixing board uses KHz as the basic input unit, 
            the user input Hz unit data needs to be converted to KHz units, 
            so user input data need to dividing by 1000 within the program

        Args:
            channel (int) : The value of channel is 1~4, representing the corresponding channel of PUMP
            frequency (int) : Frequency is 32-bit, data type is int, decimal value range is `7e9Hz~9e9Hz` and `12e9Hz~14e9Hz`
            slot (int, optional): The slot number of the MIX board. Value in list `[5, 16]`. Defaults to `None`.
            delay (float, optional) : Set the delay parameter to ensure normal transmission and response

        Raises:
            PumpFrequencyOutOfRange: Pump frequency out of range.
            MixChannelWrongError: Mix channel wrong error.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal
        """
        self.__channel_check(channel)
        slot = self.slot_check(slot)
        if frequency < 7e9 or frequency > 9e9 and frequency < 12e9 or frequency > 14e9:
            raise mix_error.PumpFrequencyOutOfRange(self.name, 7e9, 9e9, frequency)
        reg = f'MIX2.PUMP_FREQ_{channel}'
        value = int(frequency / 1000)
        self.set_reg(slot,reg,value)
        time.sleep(delay)
        return 0

    def __set_pump_power(self,channel: int, power: int = 0,power_type: Literal['norm','dbm','code'] = 'norm', slot: Union[int, None] = None, delay: float = 0.02) -> int:
        """
        Set Mr. Chen Lin's mix power of the PUMP signal
        
        Note:
            In this driver, we establish a linear relationship between the absolute output power value of 0 ~ 15dBm with 
            the register decimal setpoint of -1100 ~ -300, The formula is : value = -1100 + 800 * power / 15, Among them, 
            the user input power range in 0 ~ 15 and unit is dBm, the linear output is -1100 ~ -300.
            Of course, in later versions, we will establish accurate numerical mapping relationship between absolute power and output!

        Args:
            channel (int): The channel number that is actually marked on the MIX board. Value range in `1 - 4`.
            power (int): Power is 32-bit data type, int, decimal value range in `0dBm ~ 15dBm` power output value step 5, about 0.1dB power gain step, and the minimum value step is 1
            slot (int, optional): The slot number of the MIX board. Value in list `[5, 16]`. Defaults to `None`.
            delay (float, optional): Set the delay parameter to ensure normal transmission and response

        Raises:
            PumpPowerOutOfRange: Pump power out of range.
            MixChannelWrongError: Mix channel wrong error.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal
        """
        self.__channel_check(channel)
        slot = self.slot_check(slot)
        reg = f'MIX2.PUMP_POWER_{channel}'
        if power_type == 'norm':
            self.value_validate(value = power, v_min = 0, v_max = 1, error_class = mix_error.PumpPowerOutOfRange)
            value = int(-1100 + 800 * power)
            self.set_reg(slot,reg,value) 
        elif power_type == 'dbm':
            self.value_validate(value = power, v_min = 0, v_max = 15, error_class = mix_error.PumpPowerOutOfRange)
            value = int(-1100 + 800 * power / 15)
            self.set_reg(slot,reg,value)  
        elif power_type == 'code':
            self.value_validate(value = power, v_min = -1100, v_max = -300,error_class = mix_error.PumpPowerOutOfRange)
            value = int(power)
            self.set_reg(slot,reg,value)
        time.sleep(delay)
        return 0

    def __enable_pump(self,channel: int,flag: bool = True,slot: Union[int, None] = None, delay: float = 0.02) -> int:
        """
        Mr. Chen Lin's mix Channel closing and opening control

        Args:
            channel (int): The channel number that is actually marked on the MIX board. Value range in `1 - 4`.
            flag (bool): The lower 2 bits of the data bits are 11 to open the channel, and 00 to close the channel
            slot (int, optional): The slot number of the MIX board. Value in list `[5, 16]`. Defaults to `None`.
            delay (float, optional): Set the delay parameter to ensure normal transmission and response

        Raises:
            MixChannelWrongError: Mix channel wrong error.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal
        """
        self.__channel_check(channel)
        slot = self.slot_check(slot)
        reg = f'MIX2.PUMP_ENABLE_{channel}'
        if flag:
            self.set_reg(slot,reg,0x11)
        else:
            self.set_reg(slot,reg,0x00)
        time.sleep(delay)
        return 0

    def __get_temperature(self, slot: Union[int, None] = None, delay: float = 0.02) -> int:
        """
        Read Mr. Chen Lin's mix board temperature
        The returned temperature value is the local ambient temperature value measured by ADM1032 on the board 
        (ADM1032 temperature register data), and the temperature accuracy is 1 ℃

        Args:
            slot (int, optional): The slot number of the MIX board. Value in list `[5, 16]`. Defaults to `None`.
            delay (float, optional): Set the delay parameter to ensure normal transmission and response. Defaults to 0.1.
            
        Returns:
            The program ends normally with return value `0`, otherwise abnormal
        """
        slot = self.slot_check(slot)
        reg = 'MIX2.TEMP'
        temp = bytes_to_int(self[slot, reg])
        time.sleep(delay)
        return temp & 0xFFFFFF
    
    def __set_dds_output(self, channel:int, frequency: int, amplitude: int, mode: int, slot: Union[int, None] = None) -> int:
        """
        Real time DDS chip configuration

        Args:
            channel (int): channel (int): The channel number that is actually marked on the DAQ board. Value range in `1 - 4`.
            frequency (int): 48bit frequency data, 16bit high and low 32bit.
            amplitude (int): Amplitude control.
            mode (int): channel control register.
            slot (int, optional): The slot number of the DAQ board. Value in list `[4, 15]`. Defaults to `None`.

        Raises:
            ValueError: Value Error.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal
        """
        slot = self.slot_check(slot)
        self.__channel_check(channel)
        self.set_reg(slot, 'MULT_FUNC.MUL_FUNC_PARAM1', 1)
        self.set_reg(slot, 'MULT_FUNC.MUL_FUNC_PARAM2', 0)
        self.set_reg(slot, 'MULT_FUNC.MUL_FUNC_PARAM3', 0)
        # DDS通道选择
        if channel >= 1 and channel <= 4:
            self.set_reg(slot,'MULT_FUNC.MUL_FUNC_PARAM4',(1 << (channel + 3)))
        else:
            self.set_reg(slot, 'MULT_FUNC.MUL_FUNC_PARAM4', 0xF0)
        freq_int = int(frequency / 2.5e9*2**48)
        freq_high = (freq_int >> 32) & 0xFFFF
        self.set_reg(slot,'MULT_FUNC.MUL_FUNC_PARAM5',freq_high)
        freq_low = freq_int & 0xFFFFFFFF
        self.set_reg(slot,'MULT_FUNC.MUL_FUNC_PARAM6',freq_low)
        self.set_reg(slot,'MULT_FUNC.MUL_FUNC_PARAM7',int(amplitude))
        if mode == 0:
            self.set_reg(slot, 'MULT_FUNC.MUL_FUNC_PARAM8', 0x00000C)
        elif mode == 1:
            self.set_reg(slot, 'MULT_FUNC.MUL_FUNC_PARAM8', 0x00050C)
        elif mode == 2:
            self.set_reg(slot, 'MULT_FUNC.MUL_FUNC_PARAM8', 0x02000C)
        else:
            raise ValueError("设置DDS工作模式参数错误(0:普通模式,1:混频模式,2:关闭通道)")
        return 0

    def __set_interrupt(self, slot: Union[int, None] = None) -> int:
        """
        Set DAQ interrupt register data.

        Note:
        The interrupt handling function uses the same interrupt number, and reads registers in the interrupt handling function to 
        distinguish specific functions. The interrupt function number is defined as follows

        |      中断说明     | 中断功能编号 | 寄存器使用数量 |
        | :--------------: |:------------:|:-------------:|
        | DDS芯片配置(实时) | 1            | 8             |
        | DDS芯片配置       | 2            | 7             |
        | DAC9164芯片配置   | 3            | 4             |
        | ADC芯片校准       | 4            | 3             |
        | lmk04821         | 5            | 4             |
        | 远程更新          | 10           | 4             |
        | 硬件板卡信息修改  | 0             | 9             |

        Args:
            value (int): interrupt function number.
            slot (int, optional): The slot number of the DAQ board. Value in list `[4, 15]`. Defaults to `None`.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal
        """
        slot = self.slot_check(slot)
        reg = 'MULT_FUNC.REG2MICR_INTR'
        self.set_reg(slot, reg, 0)
        time.sleep(1)
        self.set_reg(slot, reg, 1)
        return 0