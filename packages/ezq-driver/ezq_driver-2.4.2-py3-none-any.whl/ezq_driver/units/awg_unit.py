# coding: utf-8
# ezq_driver/units/awg_unit.py

__all__ = ['send_inner_trig',
           'set_trig_select',
           'set_gain',
           'set_z_offset',
           'set_xy_nco_frequency',
           'download_qc_wave_seq', 
           'set_qc_on_off', 
           'init_pipeline',
           'get_ch_avail_circuit_num',
           'get_ch_avail_start_num',
           'set_ch_download_circuit_amount',
           'search_ch_circuit',
           'get_ch_ckt_analysis_result',
           'enable_ch_circuit',
           'get_ch_abandon_state',
           'abandon_ch_circuit']

import time
import numpy as np
from struct import pack
from .cmu_unit import CmuUnit
from ..constant import const
from ..utils import bytes_to_int
from ..protocol.pipeline_instruction import PipelineInstruction
from ..error.awg_error import *
from ..error import awg_error
from typing import Union,Tuple,Literal

class AWGUnit(CmuUnit):
    """
    该单元是ez-Q2.0产品调控子模块, 允许用户直接控制调控模块的各项功能.

    Examples:
        >>> from ezq_driver.driver import EzqDevice
        >>> awg = EzqDevice(ip = '10.0.9.11', slot = 12, console_log = True, batch_mode = False)
        >>> awg.connect()
        >>> awg.set_xy_nco_frequency(channel = 1, frequency = 3.8e9, slot = 12)
        0

    # 该模块包含以下函数:

    ## 波形输出模块:

    - <a href="#awg1">***send_inner_trig(self, count: int, interval: int, width: int = 2, slot: Union[int, None] = None)***</a> - Enable internal trigger.
    - <a href="#awg2">***set_trig_select(self, slot: Union[int, None] = None)***</a> - Enable external trigger.
    - <a href="#awg3">***set_gain(self, channel_type: str, channel: Union[int, list], gain: int, slot: Union[int, None] = None)***</a> - Set xy or z channel gain.
    - <a href="#awg4">***set_z_offset(self, channel: Union[int, list], offset_status: int, slot: Union[int, None] = None)***</a> - Z channel stability compensation control.
    - <a href="#awg5">***download_qc_wave_seq(self, channel_type: str, channel: Union[int, list], wave: list, seq: list, slot: Union[int, None] = None)***</a> - Write wave and sequnece to DDR then to AWG BRAM.
    - <a href="#awg6">***set_qc_on_off(self, channel_type: str, channel: Union[int, list], on_off: str, slot: Union[int, None] = None)***</a> - Start or Stop AWG output wave.
    - <a href="#awg7">***set_xy_nco_frequency(self, channel: Union[int, list], frequency: int, slot: Union[int, None] = None)***</a> - Set the XY-channel NCO frequency.

    ## 流水线模块:

    ### 流水线初始化:
    
    - <a href="#awg8">***init_pipeline(self, slot: Union[int, None] = None)***</a> - Pipeline initialization.
    
    ### 线路下发:
    
    - <a href="#awg9">***get_ch_avail_circuit_num(self, channel_type: str, channel: Union[int, list], slot: Union[int, None] = None)***</a> - Query the remaining space of channel line instructions.
    - <a href="#awg10">***get_ch_avail_start_num(self, channel_type: str, channel: Union[int, list], slot: Union[int, None] = None)***</a> - Query channel line issuing start number.
    - <a href="#awg11">***set_ch_download_circuit_amount(self, channel_type: str, channel: Union[int, list], download_amount: int, slot: Union[int, None] = None)***</a> - Set the number of channel lines issued.
    
    ### 线路执行:

    - <a href="#awg12">***search_ch_circuit(self, channel_type: str, channel: Union[int, list], circuit_num: int, slot: Union[int, None] = None)***</a> - Set query line number.
    - <a href="#awg13">***get_ch_ckt_analysis_result(self, channel_type: str, channel: Union[int, list], slot: Union[int, None] = None)***</a> - Query channel line analysis results.
    - <a href="#awg14">***enable_ch_circuit(self, channel_type: str, channel: Union[int, list], circuit_num: int, slot: Union[int, None] = None)***</a> - Enable line execution.
    ### 线路丢弃：
    - <a href="#awg15">***get_ch_abandon_state(self, channel_type: str, channel: Union[int, list], slot: Union[int, None] = None)***</a> - Querying channel line discard status.
    - <a href="#awg16">***abandon_ch_circuit(self, channel_type: str, channel: Union[int, list], circuit_num: int, slot: Union[int, None] = None)***</a> - Set discard line experiment ID.

    </br>
    *****************************************************************************************************************************************
    
    """
    
    def __init__(
        self, ip, port=10000, slot=0, name='', logger=None,console_log=False, dev_mode=False, batch_mode=True, wave_type='i2'):
        super().__init__(ip, port, slot, name, logger, console_log, dev_mode, batch_mode)

        self.pipline_inst = PipelineInstruction()
        self.wave_type = wave_type
        if self.wave_type == 'i2':
            self.min_volt_code = -32767
            self.max_volt_code = 32767
        else:
            self.min_volt_code = 0
            self.max_volt_code = 65535

    def __channel_check(self, channel: Union[int, list], v_min = const.AWG_MIN_CHANNEL_AMOUNT, v_max = const.AWG_MAX_CHANNEL_AMOUNT, error_class = AwgChannelOutOfRange) -> list:
        if isinstance(channel, int):
            channel = [channel]
        for ch in channel: 
            if ch < v_min or ch > v_max:
                raise error_class(self.slot, v_min, v_max, ch)
        return channel
    
    def send_inner_trig(self, count: int, interval: int, width: int = 2, slot: Union[int, None] = None) -> int:
        """
        <a id="awg1">Enable internal trigger</a>

        Args:
            count (int): Trigger number setting
            interval (int): Trigger interval setting
            width (int): Trigger width setting
            slot (int, optional): The slot number of the AWG board. Value in list `[0, 1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18, 19, 20]`. Defaults to `None`.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal
        """
        
        slot = self.slot_check(slot)
        trig_mode = 'TRIG.TRIG_SEL'
        self.set_reg(slot, trig_mode, 0)
        trig_clear = 'TRIG.TRIG_CLEAR'
        self.set_reg(slot, trig_clear, 0x01)
        trig_in_count = 'TRIG.TRIG_CNT_SET'
        self.set_reg(slot, trig_in_count, count) 
        trig_interval = 'TRIG.TRIG_INTERVAL_SET'
        self.set_reg(slot, trig_interval, interval)
        trig_width = 'TRIG.TRIG_WIDTH_SET'
        self.set_reg(slot, trig_width, width)
        trig_en_reg = 'TRIG.TRIG_START'
        self.set_reg(slot, trig_en_reg, 1)
        return 0

    def set_trig_select(self, slot: Union[int, None] = None) -> int:
        """
        <a id="awg2">Enable external trigger</a>

        Args:
            slot (int, optional): The slot number of the AWG board. Value in list `[0, 1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18, 19, 20]`. Defaults to `None`.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal
        """
        slot = self.slot_check(slot)
        trig_mode = 'TRIG.TRIG_SEL'
        self.set_reg(slot, trig_mode, 1)
        return 0

    def set_gain(self, channel_type: Literal['xy','z'], channel: Union[int, list], gain: Union[float,int] = 1.0, gain_type: Literal['norm','dbm','code','volt'] = 'norm', slot: Union[int, None] = None) -> int:
        """
        <a id="awg3">Set xy or z channel gain.</a>

        Note:
            For XY channel, we establish a linear relationship between the XY channel(channel number in 1 ~ 8) gain and the corresponding chip coded value range in 0 ~ 1023.
            For gain_type is `norm`, The formula is : value = int((const.XY_MAX_GAIN - const.XY_MIN_GAIN) * gain + const.XY_MIN_GAIN). the user setting gain is in 0 ~ 1, 
            and the linear output is const.XY_MIN_GAIN ~ const.XY_MAX_GAIN. 
            For gain_type is `dbm`, The formula is : value = int((const.XY_MAX_GAIN - const.XY_MIN_GAIN) * (gain + 25) / 10 + const.XY_MIN_GAIN), the user setting default gain is in -25dBm ~ -15dBm,
            and the linear output is const.XY_MIN_GAIN ~ const.XY_MAX_GAIN.
            For gain_type is `code`, the user setting default gain is in const.XY_MIN_GAIN ~ const.XY_MAX_GAIN, and the linear output is const.XY_MIN_GAIN ~ const.XY_MAX_GAIN.

            For Z channel, we establish a linear relationship between the Z channel(channel number in 1 ~ 20) gain and the corresponding chip coded value range in -512 ~ 512. 
            For gain_type is `norm`, The formula is : value = int((const.Z_MAX_GAIN - const.Z_MIN_GAIN) * gain + const.Z_MIN_GAIN). the user setting gain is in 0 ~ 1, 
            and the linear output is const.Z_MIN_GAIN ~ const.Z_MAX_GAIN. 
            For gain_type is `volt`, The formula is : value = int((const.Z_MAX_GAIN - const.Z_MIN_GAIN) * (gain + 1) / 2 + const.Z_MIN_GAIN), the user setting default gain is in -1.0 ~ 1.0V,
            and the linear output is const.Z_MIN_GAIN ~ const.Z_MAX_GAIN.
            For gain_type is `code`, the user setting default gain is in const.Z_MIN_GAIN ~ const.Z_MAX_GAIN, and the linear output is const.Z_MIN_GAIN ~ const.Z_MAX_GAIN.

        Args:
            channel_type (str): The channel type that is actually marked on the board. Value in `xy`, `z`.
            channel (int, list): The channel number that is actually marked on the AWG board. If channel_type='xy', Value range in `1 - 8`. If channel_type='z', Value range in `1 - 20`.
            gain (int,float): The xy and z channel gain. If the value is 'norm', the gain range is '0 ~ 1', If the value is 'dbm', the gain range is '-25 ~ -15',If the value is 'volt', the gain range is '-1.0 ~ 1.0', and if the value is code, the gain value range is '0 ~ 1023'.
            gain_type (str): Input gain type. If the value is 'norm', the gain range is '0 ~ 1', If the value is 'volt', the gain range is -1.0 ~ 1.0, and if the value is code, the gain range is '-512 ~ 512'. Default 'norm'.
            slot (int, optional): The slot number of the AWG board. Value in list `[0, 1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18, 19, 20]`. Defaults to `None`.

        Raises:
            AwgChannelOutOfRange: Awg channel out of range.
            SetGainChannelOutOfRange: Input the wrong channel.
            SetGainValueOutOfRange: Channel gain is out of range.
            SetGainFail: Set channel gain error
            SetGainChannelTypeWrongError: Set gain channel type wrong error.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal
        """

        slot = self.slot_check(slot)
        if channel_type == 'xy':
            real_channel = self.__channel_check(channel, v_min = 1, v_max = 8)
            # 建立增益与编码值之间的线性关系
            if gain_type=='norm':
                self.value_validate(value = gain, v_min = 0, v_max = 1, error_class = awg_error.SetGainValueOutOfRange)
                value = int((const.XY_MAX_GAIN - const.XY_MIN_GAIN) * gain + const.XY_MIN_GAIN)
            elif gain_type=='dbm':
                self.value_validate(value = gain, v_min = -25, v_max = -15, error_class = awg_error.SetGainValueOutOfRange)
                value = int((const.XY_MAX_GAIN - const.XY_MIN_GAIN) * (gain + 25) / 10 + const.XY_MIN_GAIN)
            elif gain_type=='code':
                self.value_validate(value = gain, v_min = const.XY_MIN_GAIN, v_max = const.XY_MAX_GAIN, error_class = awg_error.SetGainValueOutOfRange)
                value = int(gain)
            else:
                value = const.XY_MAX_GAIN
            
        elif channel_type == 'z':
            channel = self.__channel_check(channel, v_min = 1, v_max = 20)
            real_channel = [i+8 for i in channel]
            # 建立增益与编码值之间的线性关系
            if gain_type=='norm':
                self.value_validate(value = gain, v_min = 0, v_max = 1, error_class = awg_error.SetGainValueOutOfRange)
                value = int((const.Z_MAX_GAIN - const.Z_MIN_GAIN) * gain + const.Z_MIN_GAIN)
            elif gain_type=='volt':
                self.value_validate(value = gain, v_min = -1, v_max = 1, error_class = awg_error.SetGainValueOutOfRange)
                value = int((const.Z_MAX_GAIN - const.Z_MIN_GAIN) * (gain + 1) / 2 + const.Z_MIN_GAIN)
            elif gain_type=='code':
                self.value_validate(value = gain, v_min = const.Z_MIN_GAIN, v_max = const.Z_MAX_GAIN, error_class = awg_error.SetGainValueOutOfRange)
                value = int(gain)
            else:
                value = const.Z_MAX_GAIN
        else:
            raise SetChannelTypeWrongError(self.name, channel_type)

        if self.batch_mode:
            for ch in real_channel:
                register = f'CHIP_CONFIG.CH{ch}_GAIN'
                self.reg_packet[slot, register] = value
        else:
            for ch in real_channel:
                register = f'CHIP_CONFIG.CH{ch}_GAIN'
                self[slot, register] = value
        return 0

    def set_z_offset(self, channel: Union[int, list], offset: Union[int,float], offset_type:Literal['norm','code','volt'] ='norm', slot: Union[int, None] = None) -> int:
        """
        <a id="awg4">Set Z channel offset</a>

        Note:
            In this driver, we establish a linear relationship between channel offset and the corresponding chip code. 
            For offset_type is `norm`, The formula is : offset = int((self.max_volt_code - self.min_volt_code) * (offset + 1) / 2 + self.min_volt_code). 
            the user setting offset is in -1 ~ 1, and the linear output is -32767 ~ 32767. 
            For offset_type is `volt`, The formula is : value = (self.max_volt_code - self.min_volt_code) * offset / 2, the user setting default offset is in -1.0 ~ 1.0V,
            and the linear output is self.max_volt_code ~ self.min_volt_code.
            For offset_type is `code`, the user setting default offset is in self.max_volt_code ~ self.min_volt_code, and the linear output is self.max_volt_code ~ self.min_volt_code.

        Args:
            channel (int, list): The Z channel number that is actually marked on the AWG board. Value range in `1 - 20`.
            offset (int,float): The Z channel offset. If the value is 'norm', the offset range is '0 ~ 1', If the value is 'volt', the offset range is '-1.0 ~ 1.0', and if the value is code, the offset value range is '-32768 ~ 32767'.
            offset_type (str): Input offset type. If the value is 'norm', the offset range is '0 ~ 1', If the value is 'volt', the offset range is -1.0 ~ 1.0, and if the value is code, the offset range is '-32768 ~ 32767'. Default 'norm'.
            slot (int, optional): The slot number of the AWG board. Value in list `[0, 1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18, 19, 20]`. Defaults to `None`.

        Raises:
            AwgChannelOutOfRange: Awg channel out of range.
            SetDefaultVoltageValueOutOfRange: set channel default voltage error
            SetDefaultVoltageFail: set default voltage error

        Returns:
            The program ends normally with return value `0`, otherwise abnormal
        """
        if offset_type == 'norm':
            offset = int((self.max_volt_code - self.min_volt_code) * (offset + 1) / 2 + self.min_volt_code) # 建立电压与编码值之间的线性关系 
            self.__set_default_voltage(channel,offset,slot)
        elif offset_type == 'volt':
            offset = int((self.max_volt_code - self.min_volt_code) * (offset + 1) / 2 + self.min_volt_code) # 建立电压与编码值之间的线性关系
            self.__set_default_voltage(channel,offset,slot)
        elif offset_type == 'code':
            self.__set_default_voltage(channel,offset,slot)
        else:
            self.__set_default_voltage(channel,self.max_volt_code,slot)
        return 0
    
    def __set_default_voltage(self, channel: Union[int, list], codeValue: int, slot: Union[int, None] = None) -> int:
        """
        Set channel voltage.

        Args:
            channel (int, list): The channel number that is actually marked on the AWG board. Value range in `1 - 20`.
            codeValue (int): The channel default voltage. Value range in `0 - 65535`.
            slot (int, optional): The slot number of the AWG board. Value in list `[0, 1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18, 19, 20]`. Defaults to `None`.

        Raises:
            AwgChannelOutOfRange: Awg channel out of range.
            SetDefaultVoltageValueOutOfRange: set channel default voltage error
            SetDefaultVoltageFail: set default voltage error
        """
        channel = self.__channel_check(channel, v_min = 1, v_max = 20)
        slot = self.slot_check(slot)
        real_channel = [i+8 for i in channel]
        self.value_validate(codeValue, self.min_volt_code, self.max_volt_code, SetDefaultVoltageValueOutOfRange)
        if self.batch_mode: # 批量模式
            for ch in real_channel:
                register = f'AWG_B_{(ch - 9)//4+1}.DEFAULT_CODE{(ch - 9)%4+1}'
                self.reg_packet[slot, register] = codeValue
        else: # 直接模式
            for ch in real_channel:
                register = f'AWG_B_{(ch - 9)//4+1}.DEFAULT_CODE{(ch - 9)%4+1}'
                self[slot, register] = codeValue
        return 0

    def __bytes_completion(self, data: Union[np.ndarray,list], format_type: str) -> Tuple[bytes,int]:
        """
        Bytes completion.

        Args:
            data (np.ndarray, list): Wave data or wave sequence data.
            format_type (str, optional): Data format type.How to pack *data* to binary data, supported types includes 'wave' and 'seq'. Defaults to 'byte'.
        Returns:
            Bytes data and length.
        """
        if format_type == 'wave':
            if isinstance(data,np.ndarray):
                bytes_data = data.astype(dtype='i2').T.tobytes()
            elif isinstance(data,list):
                bytes_data = np.array(data,dtype='i4').tobytes()
        elif format_type == 'seq':
            bytes_data = np.array(data, dtype='<u2').tobytes()
        
        pad_cnt = (1024-(len(bytes_data)&0x3FF))&0x3FF
        if pad_cnt:
            pad_data = [0]*pad_cnt
            pad_data = pack(f'{pad_cnt}B',*pad_data)
            bytes_data += pad_data
        return bytes_data,len(bytes_data)

    def download_qc_wave_seq(self, channel_type: Literal['xy','z'], channel: Union[int, list], wave: Union[np.ndarray,list], seq: Union[np.ndarray,list], slot: Union[int, None] = None) -> int:
        """"
        <a id="awg5">Write wave and sequnece to DDR then to AWG BRAM.</a>

        Args:
            channel_type (str): The channel type that is actually marked on the board. Value is `xy` or `z`.
            channel (int, list): The channel number that is actually marked on the AWG board. If channel_type='xy', Value range in `1 - 8`. If channel_type='z', Value range in `1 - 20`. 
            wave (ndarray,list): If wave is numpy ndarray, the wave must be 2-dimension numpy ndarray,for xy channel row 0 is I-data and row 1 is Q-data, for z channel only require 1 row data. If wave is list, for xy channel the wave is 16 bit I,Q alternating data or I,Q merging into 32-bit data list, for z channel only is data list. Please refer to the user manual for wave generation instructions.
            seq (ndarray,list): If seq is numpy ndarray, the seq must be 1-dimension numpy ndarray or 2-dimension numpy data with n rows and 4 columns Each row represents a control instruction.If seq is list,the seq control instruction list. Please refer to the user manual for wave generation instructions.
            slot (int, optional): The slot number of the AWG board. Value in list `[0, 1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18, 19, 20]`. Defaults to `None`.

        Raises:
            AwgChannelOutOfRange: Awg channel out of range.
            WriteSeqChannelOutOfRange: Input the wrong channel.
            WaveSequenceLengthWrongError: Wave sequence out of range.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal
        """
        if channel_type == 'xy':
            real_channel = self.__channel_check(channel, v_min = 1, v_max = 8)
        elif channel_type == 'z':
            channel = self.__channel_check(channel, v_min = 1, v_max = 20)
            real_channel = [i+8 for i in channel]
        else:
            raise SetChannelTypeWrongError(self.name, channel_type)
        slot = self.slot_check(slot)
        # 波形
        if isinstance(wave,np.ndarray) and wave.shape[0] != 2:
            WaveTypeOrDimensionWrongError(self.name,type(wave),wave.ndim)
        wave_bytes_data,wave_length = self.__bytes_completion(data=wave,format_type='wave')
        # 序列
        seq_bytes_data,seq_length = self.__bytes_completion(data=seq,format_type='seq')

        if self.batch_mode:
            for ch in real_channel:
                wave_start_addr = const.AWG_WAVE_ADDR[ch - 1] # 波形缓存  
                self.w_mem_packet.write_mem(wave_start_addr, wave_bytes_data, slot)
                self.reg_packet[slot, 'CPU.DDR_ADDR'] = wave_start_addr
                self.reg_packet[slot, 'CPU.DATA_LEN'] = wave_length
                self.reg_packet[slot, 'CPU.TDEST'] = ch * 2 - 1
                self.reg_packet[slot, 'CPU.LOAD_WAVE'] = 0x01
        else:
            for ch in real_channel:
                wave_start_addr = const.AWG_WAVE_ADDR[ch - 1] # 波形缓存
                self.write_mem(wave_start_addr, wave_bytes_data, slot)
                self[slot, 'CPU.DDR_ADDR'] = wave_start_addr
                self[slot, 'CPU.DATA_LEN'] = wave_length
                self[slot, 'CPU.TDEST'] = ch * 2 - 1
                self[slot, 'CPU.LOAD_WAVE'] = 0x01

        if self.batch_mode:
            for ch in real_channel:
                seq_start_addr = const.AWG_SEQ_ADDR[ch - 1] # 序列缓存
                self.w_mem_packet.write_mem(seq_start_addr, seq_bytes_data, slot)
                self.reg_packet[slot, 'CPU.DDR_ADDR'] = seq_start_addr
                self.reg_packet[slot, 'CPU.DATA_LEN'] = seq_length
                self.reg_packet[slot, 'CPU.TDEST'] = ch * 2
                self.reg_packet[slot, 'CPU.LOAD_SEQ'] = 0x01
        else:
            for ch in real_channel:
                seq_start_addr = const.AWG_SEQ_ADDR[ch - 1] # 序列缓存
                self.write_mem(seq_start_addr, seq_bytes_data, slot)
                self[slot, 'CPU.DDR_ADDR'] = seq_start_addr
                self[slot, 'CPU.DATA_LEN'] = seq_length
                self[slot, 'CPU.TDEST'] = ch * 2
                self[slot, 'CPU.LOAD_SEQ'] = 0x01       
        
        return 0

    def set_qc_on_off(self, channel_type: Literal['xy','z'], channel: Union[int, list], on_off: Literal['on','off'] = 'on', slot: Union[int, None] = None) -> int:
        """
        <a id="awg6">Start or Stop AWG output wave.</a>

        Args:
            channel_type (str): The channel type that is actually marked on the board. Value is `xy` or `z`.
            channel (int, list): The channel number that is actually marked on the AWG board. If channel_type='xy', Value range in `1 - 8`. If channel_type='z', Value range in `1 - 20`.
            on_off (str): Control the start or stop of the AWG wave output. Value is `on` or `off` , `on -> start` and `off -> stop`.
            slot (int, optional): The slot number of the AWG board. Value in list `[0, 1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18, 19, 20]`. Defaults to `None`.

        Raises:
            AwgChannelOutOfRange: Awg channel out of range.
            StartOutputWaveChannelOutOfRange: Input the wrong channel.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal
        """
        if channel_type == 'xy':
            real_channel = self.__channel_check(channel, v_min = 1, v_max = 8)
        elif channel_type == 'z':
            channel = self.__channel_check(channel, v_min = 1, v_max = 20)
            real_channel = [i+8 for i in channel] 
        else:
            raise SetChannelTypeWrongError(self.name, channel_type)
        slot = self.slot_check(slot)

        if self.batch_mode: # 批量模式
            for ch in real_channel:
                cmd = 1 << ((ch - 1) % 4) if on_off == 'on' else 1 << ((ch - 1) % 4) + 4
                if ch <= const.AWG_XY_CHANNEL_AMOUNT:
                    register = f'AWG_A_{(ch - 1) // 4 + 1}.CTRL_REG'
                else:
                    register = f'AWG_B_{(ch - 1) // 4 - 1}.CTRL_REG'
                self.reg_packet[slot, register] = cmd
        else: # 直接模式
            for ch in real_channel:
                cmd = 1 << ((ch - 1) % 4) if on_off == 'on' else 1 << ((ch - 1) % 4) + 4
                if ch <= const.AWG_XY_CHANNEL_AMOUNT:
                    register = f'AWG_A_{(ch - 1) // 4 + 1}.CTRL_REG'
                else:
                    register = f'AWG_B_{(ch - 1) // 4 - 1}.CTRL_REG'
                self[slot, register] = cmd
        return 0

    def set_xy_nco_frequency(self, channel: Union[int, list], frequency: float, slot: Union[int, None] = None) -> int:
        """
        <a id="awg7">Set the XY-channel NCO frequency</a>

        Note:
            Because NCO uses GHz as the basic input unit, the user input Hz unit data needs to be converted to GHz units, 
            so user input data need to dividing by 1e9 within the program.

        Args:
            channel (int, list): The channel number that is actually marked on the AWG board. If channel_type='xy', Value range in `1 - 8`. If channel_type='z', Value range in `1 - 20`.
            frequency (float): Set NCO frequency. Value range in `0 - 6e9` and units is Hz and minimum step size `10Hz` float number.
            slot (int, optional): The slot number of the AWG board. Value in list `[0, 1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18, 19, 20]`. Defaults to `None`.

        Raises:
            AwgChannelOutOfRange: Awg channel out of range.
            ChannelWrongError: Input the wrong channel number.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal
        """
        real_channel = self.__channel_check(channel, v_min=1, v_max=const.AWG_XY_CHANNEL_AMOUNT)
        # if frequency % 10 != 0:
        #     raise IllegallNCOFrequencyError(frequency, const.NCO_FREQUENCY_STEP)
        self.value_validate(value = frequency, v_min = 0, v_max = 6e9, 
                            error_class = awg_error.NCOFrequencyValueOutOfRange)
        slot = self.slot_check(slot)

        if self.batch_mode: # 批量模式
            for ch in real_channel:
                register = f'CHIP_CONFIG.CH{ch}_NCO_FREQ'
                self.reg_packet[slot, register] = float(frequency / 1e9)
        else: # 直接模式
            for ch in real_channel:
                register = f'CHIP_CONFIG.CH{ch}_NCO_FREQ'
                self[slot, register] = float(frequency / 1e9)
        self.__set_xy_filter_voltage(real_channel, frequency, slot)
        return 0

    def __set_xy_filter_voltage(self, channel: Union[int, list], frequency: float, slot: Union[int, None] = None) -> int:
        """
        Set the XY-channel filter voltage

        Args:
            channel (int, list): The channel number that is actually marked on the AWG board. If channel_type='xy', Value range in `1 - 8`. If channel_type='z', Value range in `1 - 20`.
            frequency (float): Set NCO frequency. Value range in `0-6e9` and units is Hz and minimum step size `10Hz` float number.
            slot (int, optional): The slot number of the AWG board. Value in list `[0, 1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18, 19, 20]`. Defaults to `None`.

        Raises:
            AwgChannelOutOfRange: Awg channel out of range.
            ChannelWrongError: Input the wrong channel number.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal
        """
        real_channel = self.__channel_check(channel, v_min=0, v_max=const.AWG_XY_CHANNEL_AMOUNT)
        slot = self.slot_check(slot)
        self.value_validate(value = frequency, v_min = 0, v_max = 6e9, 
                            error_class = awg_error.NCOFrequencyValueOutOfRange)
        # 3阶多项式拟合 最大误差0.2530571444039813，平均误差0.10609596609638378，方差0.005051682449573988
        # 限制幅度 [0,14]
        filter_volt = min(max(-5.80082938e-29 * frequency ** 3 + 1.00467873e-18 * frequency ** 2 + -2.14569526e-09 * frequency + -3.42123377e+00,0),15)
        # 建立滤波器电压与编码值线性映射关系,输入0 ~ 12V, 输出编码0 ~ 65535
        value = int(65535 * filter_volt / 12)
        if self.batch_mode: # 批量模式
            for ch in real_channel:
                register = f'CHIP_CONFIG.CH{ch}_F_VOLT'
                self.reg_packet[slot, register] = value
        else: # 直接模式
            for ch in real_channel:
                register = f'CHIP_CONFIG.CH{ch}_F_VOLT'
                self[slot, register] = value
        return 0

    def init_pipeline(self, slot: Union[int, None] = None) -> int:
        """
        <a id="awg8">Pipeline initialization</a>

        Args:
            slot (int, optional): The slot number of the AWG board. Value in list `[0, 1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18, 19, 20]`. Defaults to `None`.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal
        """
        reset_reg = 'PIPELINE.PIPELINE_INIT'
        slot = self.slot_check(slot)
        self[slot, reset_reg] = 0x01
        for i in range(const.AWG_XYZ_CHANNEL_AMOUNT):
            assert bytes_to_int(self[f'PIPELINE.INSTR_FREE_SPACE_{i+1}']) == 32, self[f'PIPELINE.INSTR_FREE_SPACE_{i+1}']
            assert bytes_to_int(self[f'PIPELINE.INSTR_CATHE_START_NUM_{i+1}']) == 0
            assert bytes_to_int(self[f'PIPELINE.CIRCUIT_NUM_STATUS_{i+1}']) == 0
            assert bytes_to_int(self[f'PIPELINE.ABANDON_STATUS_{i+1}']) == 0
        return 0

    def get_ch_avail_circuit_num(self, channel_type: str, channel: Union[int, list], slot: Union[int, None] = None) -> int:
        """
        <a id="awg9">Query the remaining space of channel line instructions</a>

        Args:
            channel_type (str): The channel type that is actually marked on the board. Value in `xy`, `z`.
            channel (int, list): The channel number that is actually marked on the AWG board. If channel_type='xy', Value range in `1 - 8`. If channel_type='z', Value range in `1 - 20`.
            slot (int, optional): The slot number of the AWG board. Value in list `[0, 1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18, 19, 20]`. Defaults to `None`.

        Raises:
            AwgChannelOutOfRange: Awg channel out of range.
            ChannelWrongError: Input the wrong channel number.

        Returns:
            The remaining space of channel line instructions
        """

        if channel_type == 'xy':
            real_channel = self.__channel_check(channel, v_min = 1, v_max = 8)
        elif channel_type == 'z':
            channel = self.__channel_check(channel, v_min = 1, v_max = 20)
            real_channel = [i+8 for i in channel] 
        else:
            raise SetChannelTypeWrongError(self.name, channel_type)
        slot = self.slot_check(slot)

        if self.batch_mode: # 批量模式
            for ch in real_channel:
                avail_ckt_num_reg = f'PIPELINE.INSTR_FREE_SPACE_{ch}'
                self.reg_packet(slot, avail_ckt_num_reg)
                num = 0
        else: # 直接模式
            for ch in real_channel:
                avail_ckt_num_reg = f'PIPELINE.INSTR_FREE_SPACE_{ch}'
                num = self[slot, avail_ckt_num_reg]
                num = bytes_to_int(num)
        return num

    def get_ch_avail_start_num(self, channel_type: str, channel: Union[int, list], slot: Union[int, None] = None) -> int:
        """
        <a id="awg10">Query channel line issuing start number</a>

        Args:
            channel_type (str): The channel type that is actually marked on the board. Value in `xy`, `z`.
            channel (int, list): The channel number that is actually marked on the AWG board. If channel_type='xy', Value range in `1 - 8`. If channel_type='z', Value range in `1 - 20`.
            slot (int, optional): The slot number of the AWG board. Value in list `[0, 1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18, 19, 20]`. Defaults to `None`.

        Raises:
            ChannelWrongError: Input the wrong channel number.

        Returns:
            channel line issuing start number
        """

        if channel_type == 'xy':
            real_channel = self.__channel_check(channel, v_min = 1, v_max = 8)
        elif channel_type == 'z':
            channel = self.__channel_check(channel, v_min = 1, v_max = 20)
            real_channel = [i+8 for i in channel] 
        else:
            raise SetChannelTypeWrongError(self.name, channel_type)
        slot = self.slot_check(slot)

        if self.batch_mode: # 批量模式
            for ch in real_channel:
                start_num_reg = f'PIPELINE.INSTR_CATHE_START_NUM_{ch}'
                self.reg_packet(slot, start_num_reg)
                num = 0
        else: # 直接模式
            for ch in real_channel:
                start_num_reg = f'PIPELINE.INSTR_CATHE_START_NUM_{ch}'
                num = self[slot, start_num_reg]
                num = bytes_to_int(num)
        return num

    def set_ch_download_circuit_amount(self, channel_type: str, channel: Union[int, list], download_amount: int, slot: Union[int, None] = None) -> int:
        """
        <a id="awg11">Set the number of channel lines issued</a>

        Notes:
            The number of lines delivered cannot exceed the remaining space of the channel.

        Args:
            channel_type (str): The channel type that is actually marked on the board. Value in `xy`, `z`.
            channel (int, list): The channel number that is actually marked on the AWG board. If channel_type='xy', Value range in `1 - 8`. If channel_type='z', Value range in `1 - 20`.
            download_amount (int): download circuit amount. The number of lines delivered cannot exceed the remaining space of the channel.
            slot (int, optional): The slot number of the AWG board. Value in list `[0, 1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18, 19, 20]`. Defaults to `None`.

        Raises:
            AwgChannelOutOfRange: Awg channel out of range.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal
        """
        if channel_type == 'xy':
            real_channel = self.__channel_check(channel, v_min = 1, v_max = 8)
        elif channel_type == 'z':
            channel = self.__channel_check(channel, v_min = 1, v_max = 20)
            real_channel = [i+8 for i in channel] 
        else:
            raise SetChannelTypeWrongError(self.name, channel_type)
        slot = self.slot_check(slot)

        if self.batch_mode: # 批量模式
            for ch in real_channel:
                dl_ckt_amount_reg = f'PIPELINE.INSTR_DOWNLOAD_{ch}'
                self.reg_packet[slot, dl_ckt_amount_reg] = download_amount
        else: # 直接模式
            for ch in real_channel:
                dl_ckt_amount_reg = f'PIPELINE.INSTR_DOWNLOAD_{ch}'
                self[slot, dl_ckt_amount_reg] = download_amount
        return 0

    def search_ch_circuit(self, channel_type: str, channel: Union[int, list], circuit_num: int, slot: Union[int, None] = None) -> int:
        """
        <a id="awg12">Set query line number</a>

        Notes:
            When the line number is written to this register, all lines smaller than the query number are discarded.

        Args:
            channel_type (str): The channel type that is actually marked on the board. Value in `xy`, `z`.
            channel (int, list): The channel number that is actually marked on the AWG board. If channel_type='xy', Value range in `1 - 8`. If channel_type='z', Value range in `1 - 20`.
            circuit_num (int): circuit number. When the line number is written to this register, all lines smaller than the query number are discarded.
            slot (int, optional): The slot number of the AWG board. Value in list `[0, 1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18, 19, 20]`. Defaults to `None`.

        Raises:
            AwgChannelOutOfRange: Awg channel out of range.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal
        """
        if channel_type == 'xy':
            real_channel = self.__channel_check(channel, v_min = 1, v_max = 8)
        elif channel_type == 'z':
            channel = self.__channel_check(channel, v_min = 1, v_max = 20)
            real_channel = [i+8 for i in channel] 
        else:
            raise SetChannelTypeWrongError(self.name, channel_type)
        slot = self.slot_check(slot)

        if self.batch_mode: # 批量模式
            for ch in real_channel:
                srch_ckt_num_reg = f'PIPELINE.CIRCUIT_NUM_INQUIRE_{ch}'
                self.reg_packet[slot, srch_ckt_num_reg] = circuit_num
        else: # 直接模式
            for ch in real_channel:
                srch_ckt_num_reg = f'PIPELINE.CIRCUIT_NUM_INQUIRE_{ch}'
                self[slot, srch_ckt_num_reg] = circuit_num
        return 0

    def get_ch_ckt_analysis_result(self, channel_type: str, channel: Union[int, list], slot: Union[int, None] = None) -> int:
        """
        <a id="awg13">Query channel line analysis results</a>

        Args:
            channel_type (str): The channel type that is actually marked on the board. Value in `xy`, `z`.
            channel (int, list): The channel number that is actually marked on the AWG board. If channel_type='xy', Value range in `1 - 8`. If channel_type='z', Value range in `1 - 20`.
            slot (int, optional): The slot number of the AWG board. Value in list `[0, 1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18, 19, 20]`. Defaults to `None`.

        Raises:
            AwgChannelOutOfRange: Awg channel out of range.

        Returns:
            channel line analysis results
        """

        if channel_type == 'xy':
            real_channel = self.__channel_check(channel, v_min = 1, v_max = 8)
        elif channel_type == 'z':
            channel = self.__channel_check(channel, v_min = 1, v_max = 20)
            real_channel = [i+8 for i in channel] 
        else:
            raise SetChannelTypeWrongError(self.name, channel_type)
        slot = self.slot_check(slot)

        if self.batch_mode: # 批量模式
            for ch in real_channel:
                start_num_reg = f'PIPELINE.CIRCUIT_NUM_STATUS_{ch}'
                self.reg_packet(slot, start_num_reg)
                start_num = 0
        else: # 直接模式
            for ch in real_channel:
                start_num_reg = f'PIPELINE.CIRCUIT_NUM_STATUS_{ch}'
                start_num = self[slot, start_num_reg]
                start_num = bytes_to_int(start_num)
        return start_num
    
    def enable_ch_circuit(self, channel_type: str, channel: Union[int, list], circuit_num: int, slot: Union[int, None] = None) -> int:
        """
        <a id="awg14">Enable line execution</a>

        Args:
            channel_type (str): The channel type that is actually marked on the board. Value in `xy`, `z`.
            channel (int, list): The channel number that is actually marked on the AWG board. If channel_type='xy', Value range in `1 - 8`. If channel_type='z', Value range in `1 - 20`.
            circuit_num (int): circuit number.
            slot (int, optional): The slot number of the AWG board. Value in list `[0, 1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18, 19, 20]`. Defaults to `None`.

        Raises:
            AwgChannelOutOfRange: Awg channel out of range.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal
        """

        if channel_type == 'xy':
            real_channel = self.__channel_check(channel, v_min = 1, v_max = 8)
        elif channel_type == 'z':
            channel = self.__channel_check(channel, v_min = 1, v_max = 20)
            real_channel = [i+8 for i in channel] 
        else:
            raise SetChannelTypeWrongError(self.name, channel_type)
        slot = self.slot_check(slot)

        if self.batch_mode: # 批量模式
            for ch in real_channel:
                exec_ckt_reg = f'PIPELINE.CIRCUIT_NUM_EXECUTE_{ch}'
                self.reg_packet[slot, exec_ckt_reg] = circuit_num
        else: # 直接模式
            for ch in real_channel:
                exec_ckt_reg = f'PIPELINE.CIRCUIT_NUM_EXECUTE_{ch}'
                self[slot, exec_ckt_reg] = circuit_num
        return 0

    def get_ch_abandon_state(self, channel_type: str, channel: Union[int, list], slot: Union[int, None] = None) -> int:
        """
        <a id="awg15">Querying channel line discard status</a>

        Args:
            channel_type (str): The channel type that is actually marked on the board. Value in `xy`, `z`.
            channel (int, list): The channel number that is actually marked on the AWG board. If channel_type='xy', Value range in `1 - 8`. If channel_type='z', Value range in `1 - 20`.
            slot (int, optional): The slot number of the AWG board. Value in list `[0, 1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18, 19, 20]`. Defaults to `None`.

        Raises:
            AwgChannelOutOfRange: Awg channel out of range.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal
        """

        if channel_type == 'xy':
            real_channel = self.__channel_check(channel, v_min = 1, v_max = 8)
        elif channel_type == 'z':
            channel = self.__channel_check(channel, v_min = 1, v_max = 20)
            real_channel = [i+8 for i in channel] 
        else:
            raise SetChannelTypeWrongError(self.name, channel_type)
        slot = self.slot_check(slot)

        if self.batch_mode: # 批量模式
            for ch in real_channel:
                abandon_reg = f'PIPELINE.ABANDON_STATUS_{ch}'
                self.reg_packet(slot, abandon_reg)
                state = 0
        else: # 直接模式
            for ch in real_channel:
                abandon_reg = f'PIPELINE.ABANDON_STATUS_{ch}'
                state = self[slot, abandon_reg]
                state = bytes_to_int(state)
        return state

    def abandon_ch_circuit(self, channel_type: str, channel: Union[int, list], circuit_num: int, slot: Union[int, None] = None) -> int:
        """
        <a id="awg16">Set discard line experiment ID</a>

        Notes:
            Only one circuit with one experiment ID can be discarded at a time, and the next experiment ID cannot be discarded until one experiment ID is discarded.

        Args:
            channel_type (str): The channel type that is actually marked on the board. Value in `xy`, `z`.
            channel (int, list): The channel number that is actually marked on the AWG board. If channel_type='xy', Value range in `1 - 8`. If channel_type='z', Value range in `1 - 20`.
            circuit_num (int): circuit number.
            slot (int, optional): The slot number of the AWG board. Value in list `[0, 1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18, 19, 20]`. Defaults to `None`.

        Raises:
            AwgChannelOutOfRange: Awg channel out of range.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal
        """

        if channel_type == 'xy':
            real_channel = self.__channel_check(channel, v_min = 1, v_max = 8)
        elif channel_type == 'z':
            channel = self.__channel_check(channel, v_min = 1, v_max = 20)
            real_channel = [i+8 for i in channel] 
        else:
            raise SetChannelTypeWrongError(self.name, channel_type)
        slot = self.slot_check(slot)

        if self.batch_mode: # 批量模式
            for ch in real_channel:
                abandon_exp_reg = f'PIPELINE.ABANDON_ID_{ch}'
                self.reg_packet[slot, abandon_exp_reg] = circuit_num
        else: # 直接模式
            for ch in real_channel:
                abandon_exp_reg = f'PIPELINE.ABANDON_ID_{ch}'
                self[slot, abandon_exp_reg] = circuit_num
        return 0