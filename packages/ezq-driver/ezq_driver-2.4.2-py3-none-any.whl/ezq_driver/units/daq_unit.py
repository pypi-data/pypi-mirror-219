# coding: utf-8
# ezq_driver/units/daq_unit.py

__all__ = [
           'set_acq_params',
           'set_demod_mode',
           'set_demod_filter',
           'set_mulstate_disc_params',
           'set_daq_enable',
           'get_daq_data',
           'download_qr_wave_seq',
           'set_qr_on_off', 
           'set_reset_pulse_width'
           'run_circuit',
           'sync_system_clk'
          ]

from struct import unpack,pack
import numpy as np
import time

from .cmu_unit import CmuUnit
from ..utils import cacl_twos_complement,bytes_to_int,find_best_tap
from ..constant import const
from ..error.daq_error import *
from ..protocol.data_analysis import ReadoutDataAnalysis
from typing import Union, List, Tuple
import warnings
class DAQUnit(CmuUnit):
    """
    该单元是ez-Q2.0产品通信管理子模块, 允许用户直接控制通信模块的各项功能.

    Examples:
        >>> from ezq_driver.driver import EzqDevice
        >>> daq = EzqDevice(ip = '10.0.9.11', slot = 23, console_log = True, batch_mode = False)
        >>> daq.connect()
        >>> daq.set_qr_on_off(gen_type = 'ifin', channel = 1, on_off = 'on', slot = 4)
        0

    # 该模块包含以下函数:

    ## DAQ模块:

    - <a href="#daq1">***set_acq_params(channel, mode, sample_count, start, depth, slot)***</a> - Config wave mode and demod mode parameters.
    - <a href="#daq2">***set_demod_mode(channel, mode, slot)***</a> - Set the demo mode qubits number.
    - <a href="#daq3">***set_demod_filter(channel, data_type, demod_data_list, slot)***</a> - Set the matching filter data.
    - <a href="#daq4">***set_mulstate_disc_params(channel, pointlist, qubit_index, slot)***</a> - Set the state judgment parameters.
    - <a href="#daq5">***set_daq_enable(channel, mode, ts_mask, slot)***</a> - DAQ module enable: Set bit[6:4] to 1 to realize wave mode, demo mode and state mode reset.
    - <a href="#daq6">***get_daq_data(channel, mode, start_address, timeout, slot)***</a> - Read data of WAVE_MODE、DEMO_MODE、STATES_MODE from corresponding start address.
    
    ## 激励模块:

    - <a href="#daq7">***download_qr_wave_seq(gen_type, channel, wave, seq, slot)***</a> - Write wave data to awg BRAM.
    - <a href="#daq8">***set_qr_on_off(gen_type, channel, on_off, slot)***</a> - Start or Stop daq channel output wave.
    
    ## 反馈模块:
    
    - <a href="#daq9">***set_reset_pulse_width(channel, pulse1_width, pulse2_width, slot)***</a> - Feedback pulse control.

    ## 同步模块:
    - <a href="#daq10">***run_circuit(command, slot)***</a> - Set synchronization command.
    - <a href="#daq11">***sync_system_clk(peripheral_list)***</a> - System synchronization.

    </br>
    ************************************************************************************************************************************************
    
    """

    def __init__(self, ip, port=10000, slot=4, name='',logger=None, console_log=False, dev_mode=False, batch_mode=True,sample_depth=2000, sample_start=0, 
            sample_count=1, demod_freqs=[],demod_weights=None, demod_window_start=[0],demod_window_width=[1000], point_list=[], sync_mode=None):
        super().__init__(ip, port, slot, name, logger, console_log, dev_mode, batch_mode)
        self.sample_depth = sample_depth
        self.sample_start = sample_start
        self.sample_count = sample_count
        self.demod_freqs = demod_freqs
        self.demod_weights = demod_weights
        self.demod_window_start = demod_window_start
        self.demod_window_width = demod_window_width
        self.point_list = point_list
        self.sync_mode = sync_mode
        self.mode = const.DEMO_MODE
        self.qubits_mode = 0

    def __mode_check(self, mode) -> int:
        if mode is None:
            mode = self.mode
        if mode not in [const.DEMO_MODE, const.WAVE_MODE, const.STATE_MODE, const.FEED_MODE]:
            raise ModeWrongError(self.slot, mode)
        return mode
    
    def __channel_check(self, channel: Union[int, list]) -> list:
        if isinstance(channel, int):
            channel = [channel]
        for ch in channel:
            if ch < const.DAQ_MIN_CHANNEL_AMOUNT or ch > const.DAQ_MAX_CHANNEL_AMOUNT:
                raise ChannelWrongError(self.slot, ch)
        return channel

    def set_acq_params(self, channel: Union[int, list], mode: Union[int, None] = None, sample_count: int = 1,  start: Union[int, list, None] = None, depth: Union[int, list, None] = None, slot: Union[int, None] = None) -> int:
        """
        <a id="daq1">Config wave mode and demod mode parameters:</a>
            - Set the trigger count in wave mode.
            - Set the acquisition start time in wave mode.
            - Set the sample depth in wave mode.
            - Set the trigger count in demod mode.
            - Set the start position of the demod window.
            - Set the width of the demod window.

        Notes:
            the number of demod qubits and demod window width:

            | number of demo qubits |   demod window width  | description | 
            | :-------------------: | :-------------------: | :---------: |
            |        16 qubits      |       0 - 1.6e-6s     |             |
            |        8 qubits       |       0 - 3.2e-6s     |             |
            |        4 qubits       |       0 - 6.4e-6s     |             |

        Args:
            channel (int, list): The channel number that is actually marked on the DAQ board. Value range in `1 - 4`.
            mode (int, optional): The Patterns of DAQ experiments. value in list `[0, 1]` and `mode = 0 -> WAVE MODE`, `mode = 1 -> DEMO_MODE`. Defaults to `None`.
            sample_count int: The wave or demod trigger count. Default 1.
            start (list, optional): If `mode = 0`, it represents acquisition start time, value range in `-5e-6 - 5e-6` and units is s. If `mode = 1`, it represents start position of the demod window, value range in `0 - 65535` without unit. Defaults to None.
            depth (list, optional): If `mode = 0`, it represents sampling depth, value range in `0 - 10e-6` and unit is s. If `mode = 1`, it represents start position of the demod window, max value in [1.6e-6, 3.2e-6, 6.4e-6] and unit is s, `16 qubits -> 0-1.6e-6s`, `8 qubits -> 0-3.2e-6s`, `4 qubits -> 0-6.4e-6s`. Defaults to `None`.
            slot (int, optional): The slot number of the DAQ board. Value in list `[4, 15]`. Defaults to `None`.

        Raises:
            WaveStartTimeOutOfRange: Wave start time out of range
            WaveSampleDepthOutOfRange: Wave sample depth out of range
            DemodWindowStartOutOfRange: Demod window start out of range
            DemodWindowWidthOutOfRange: Demod window width out of range
            ModeWrongError: Mode wrong error
            SampleCountOutOfRange: Sample count out of range
            ChannelWrongError: Channel wrong error.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal.
        """
        channel_list = self.__channel_check(channel)
        slot = self.slot_check(slot)
        mode = self.__mode_check(mode)
        self.sample_count = sample_count
        if self.batch_mode:
            for ch in channel_list:
                if mode == const.WAVE_MODE:
                    # 设置波形触发个数
                    trig_count_reg = f'DAQ_{ch-1}.WAVE_TRIG_COUNT'
                    max_cnt = const.MAX_WAVE_SAMPLE_COUNT
                    # 设置波形采集开始时间
                    if start > const.MAX_WAVE_SAMPLE_POSITION or start < const.MIN_WAVE_SAMPLE_POSITION:
                        raise WaveStartTimeOutOfRange(slot, const.MIN_WAVE_SAMPLE_POSITION, const.MAX_WAVE_SAMPLE_POSITION, start)
                    wave_position_reg = f'DAQ_{ch-1}.WAVE_SAMPLE_POSITION'
                    sample_cnt = int(abs(start) * const.SAMPLE_RATE)
                    if start < 0:
                        sample_cnt = (1 << 15 | sample_cnt)
                    sample_cnt_twos_cpl = cacl_twos_complement(sample_cnt, bit_width=0xFFFF)
                    self.reg_packet[slot, wave_position_reg] = sample_cnt_twos_cpl
                    # 设置波形采样深度
                    if depth < const.MIN_WAVE_SAMPLE_DEPTH or depth > const.MAX_WAVE_SAMPLE_DEPTH:
                        raise WaveSampleDepthOutOfRange(slot, const.MIN_WAVE_SAMPLE_DEPTH, const.MAX_WAVE_SAMPLE_DEPTH, depth)
                    depth_reg = f'DAQ_{ch-1}.WAVE_SAMPLE_DEPTH'
                    sample_cnt = (int(depth * const.SAMPLE_RATE)) // 16 * 16
                    # sample_cnt = int(depth * DAQUnit.SAMPLE_RATE)
                    self.sample_depth = sample_cnt
                    self.reg_packet[slot, depth_reg] = sample_cnt
                elif mode == const.DEMO_MODE:
                    # 设置解模触发个数
                    trig_count_reg = f'DAQ_{ch-1}.DEMOD_TRIG_COUNT'
                    max_cnt = const.MAX_DEMOD_TRIG_COUNT
                    # 设置解模窗口起始位置
                    window_start_reg = f'DAQ_{ch-1}.DEMOD_WINDOW_START'
                    if isinstance(start,int):
                        start = [start]
                    for sta in start:
                        if sta < const.MIN_DEMOD_WINDOW_START or sta > const.MAX_DEMOD_WINDWOS_START:
                            raise DemodWindowStartOutOfRange(slot, const.MIN_DEMOD_WINDOW_START, const.MAX_DEMOD_WINDWOS_START, sta)
                    demod_window_start_cnts = [int(i * const.SAMPLE_RATE) // 16 * 16 for i in start]
                    # sample_cnt = int(abs(start) * const.SAMPLE_RATE)
                    # window_start_value = cacl_twos_complement(sample_cnt, bit_width=0xFFFF)
                    self.demod_window_start = demod_window_start_cnts
                    self[slot, window_start_reg] = min(demod_window_start_cnts) #window_start_value
                    # 设置解模窗口宽度
                    if self.qubits_mode == const.DEMO_QUBITS_MODE[0]:
                        max_width = const.QUBITS_16_WINDOW_WIDTH
                    elif self.qubits_mode == const.DEMO_QUBITS_MODE[1]:
                        max_width = const.QUBITS_8_WINDOW_WIDTH
                    else:
                        max_width = const.QUBITS_4_WINDOW_WIDTH
                    window_width_reg = f'DAQ_{channel-1}.DEMOD_WINDOW_WIDTH'
                    if isinstance(depth,int):
                        depth = [depth]
                    # 如果输入单值转换成列表处理
                    for dep in depth:
                        if dep < 0 or dep > max_width:
                            raise DemodWindowWidthOutOfRange(slot, 0, max_width, dep, self.qubits_mode)
                    sample_cnts = [int(i * const.SAMPLE_RATE) // 16 * 16 for i in depth]
                    self.demod_window_width = sample_cnts
                    self.reg_packet[slot, window_width_reg] = max(sample_cnts) #如果输入多频点的解模宽度列表，找最大值作为功用解模宽度
                elif mode == const.STATE_MODE:
                    # 设置态读出触发个数
                    trig_count_reg = f'DAQ_{ch-1}.RDOUT_TRIG_COUNT'
                    max_cnt = const.MAX_RDOUT_TRIG_COUNT
                else:
                    raise ModeWrongError(self.slot, mode)
                
                if sample_count < 0 or sample_count > max_cnt:
                    raise SampleCountOutOfRange(slot, 0, max_cnt, sample_count, self.mode)
                self.reg_packet[slot, trig_count_reg] = sample_count
        else:
            for ch in channel_list:
                if mode == const.WAVE_MODE:
                    # 设置波形触发个数
                    trig_count_reg = f'DAQ_{ch-1}.WAVE_TRIG_COUNT'
                    max_cnt = const.MAX_WAVE_SAMPLE_COUNT
                    # 设置波形采集开始时间
                    if start > const.MAX_WAVE_SAMPLE_POSITION or start < const.MIN_WAVE_SAMPLE_POSITION:
                        raise WaveStartTimeOutOfRange(slot, const.MIN_WAVE_SAMPLE_POSITION, const.MAX_WAVE_SAMPLE_POSITION, start)
                    wave_position_reg = f'DAQ_{ch-1}.WAVE_SAMPLE_POSITION'
                    sample_cnt = int(abs(start) * const.SAMPLE_RATE)
                    if start < 0:
                        sample_cnt = (1 << 15 | sample_cnt)
                    sample_cnt_twos_cpl = cacl_twos_complement(sample_cnt, bit_width=0xFFFF)
                    self[slot, wave_position_reg] = sample_cnt_twos_cpl
                    # 设置波形采样深度
                    if depth < const.MIN_WAVE_SAMPLE_DEPTH or depth > const.MAX_WAVE_SAMPLE_DEPTH:
                        raise WaveSampleDepthOutOfRange(slot, const.MIN_WAVE_SAMPLE_DEPTH, const.MAX_WAVE_SAMPLE_DEPTH, depth)
                    depth_reg = f'DAQ_{ch-1}.WAVE_SAMPLE_DEPTH'
                    sample_cnt = (int(depth * const.SAMPLE_RATE)) // 16*16
                    # sample_cnt = int(depth * DAQUnit.SAMPLE_RATE)
                    self.sample_depth = sample_cnt
                    self[slot, depth_reg] = sample_cnt
                elif mode == const.DEMO_MODE:
                    # 设置解模触发个数
                    trig_count_reg = f'DAQ_{ch-1}.DEMOD_TRIG_COUNT'
                    max_cnt = const.MAX_DEMOD_TRIG_COUNT
                    # 设置解模窗口起始位置
                    window_start_reg = f'DAQ_{ch-1}.DEMOD_WINDOW_START'
                    if isinstance(start,int):
                        start = [start]
                    for sta in start:
                        if sta < const.MIN_DEMOD_WINDOW_START or sta > const.MAX_DEMOD_WINDWOS_START:
                            raise DemodWindowStartOutOfRange(slot, const.MIN_DEMOD_WINDOW_START, const.MAX_DEMOD_WINDWOS_START, sta)
                    demod_window_start_cnts = [int(i * const.SAMPLE_RATE) // 16 * 16 for i in start]
                    # sample_cnt = int(abs(start) * const.SAMPLE_RATE)
                    # window_start_value = cacl_twos_complement(sample_cnt, bit_width=0xFFFF)
                    self.demod_window_start = demod_window_start_cnts
                    self[slot, window_start_reg] = min(demod_window_start_cnts) #window_start_value
                    # 设置解模窗口宽度
                    if self.qubits_mode == const.DEMO_QUBITS_MODE[0]:
                        max_width = const.QUBITS_16_WINDOW_WIDTH
                    elif self.qubits_mode == const.DEMO_QUBITS_MODE[1]:
                        max_width = const.QUBITS_8_WINDOW_WIDTH
                    else:
                        max_width = const.QUBITS_4_WINDOW_WIDTH
                    window_width_reg = f'DAQ_{channel-1}.DEMOD_WINDOW_WIDTH'
                    # 如果输入单值转换成列表处理
                    if isinstance(depth,int):
                        depth = [depth]
                    for dep in depth:
                        if dep < 0 or dep > max_width:
                            raise DemodWindowWidthOutOfRange(slot, 0, max_width, dep, self.qubits_mode)
                    sample_cnts = [int(i * const.SAMPLE_RATE) // 16 * 16 for i in depth]
                    self.demod_window_width = sample_cnts
                    self[slot, window_width_reg] = max(sample_cnts) #如果输入多频点的解模宽度列表，找最大值作为功用解模宽度
                elif mode == const.STATE_MODE:
                    # 设置态读出触发个数
                    trig_count_reg = f'DAQ_{ch-1}.RDOUT_TRIG_COUNT'
                    max_cnt = const.MAX_RDOUT_TRIG_COUNT
                else:
                    raise ModeWrongError(self.slot, mode)
                
                if sample_count < 0 or sample_count > max_cnt:
                    raise SampleCountOutOfRange(slot, 0, max_cnt, sample_count, self.mode)
                self[slot, trig_count_reg] = sample_count            
            return 0

    def set_demod_mode(self, channel: Union[int, list], mode: int, slot: Union[int, None] = None) -> int:
        """
        <a id="daq2">Set the demo mode qubits number.</a>

        Notes:
            The value of the mode parameter and the number of demo qubits:

            | mode value | number of demo qubits | description | 
            | :--------: | :-------------------: | :---------: |
            |      0     |        16 qubits      |             |
            |      1     |        8 qubits       |             |
            |      2     |        4 qubits       |             |

        Args:
            channel (int, list): The channel number that is actually marked on the DAQ board. Value range in `1 - 4`.
            mode (int): The selection of qubits number. value in list `[0, 1, 2]` and `mode = 0 -> 16 qubits`, `mode = 1 -> 8 qubits`, `mode = 2 -> 4 qubits`.
            slot (int, optional): The slot number of the DAQ board. Value in list `[4, 15]`. Defaults to `None`.

        Raises:
            QubitsModeWrongError: Qubits mode wrong error.
            ChannelWrongError: Channel wrong error.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal.
        """
        channel_list = self.__channel_check(channel)
        slot = self.slot_check(slot)
        if mode not in const.DEMO_QUBITS_MODE:
            raise QubitsModeWrongError(self.name, mode)
        
        if self.batch_mode:
            for ch in channel_list:
                function_reg = f'DAQ_{ch - 1}.FUNCTION'
                self.reg_packet[slot, function_reg] = mode
        else:
            for ch in channel_list:
                function_reg = f'DAQ_{ch - 1}.FUNCTION'
                self[slot, function_reg] = mode
        self.qubits_mode = mode
        return 0

    def __filter_data_normalization(self, data):
        max_data = np.max(data)
        min_data = np.min(data)
        k = (const.MAX_FILTER_DATA - const.MIN_FILTER_DATA) / (max_data - min_data)
        normal_data = const.MIN_FILTER_DATA + k * (data - min_data)
        return normal_data
    
    def set_demod_filter(self, channel: Union[int, list], demod_freqs: Union[list, np.ndarray], demod_weights: Union[list, np.ndarray] = [[[]],[[]]], slot: Union[int, None] = None) -> Tuple[list,list]:
        """
        <a id="daq3">Set the matching filter data</a>

        Note:
            1.You need to ensure that setting the demod window width is done before the function call.
            2.The cos(wt) function is used to generate the matching filter data of I, and the Q matched filter data of 
            the same time is composed of a 32-bit data as a high 16-bit data and the Q matched filter data at the same time.
            The -sin(wt) function is used to generate Q matching filter data, which is used as low 16bit data and I-matching 
            filter data at the same time to form a 32-bit data when it is delivered.

        Args:
            channel (int, list): The channel number that is actually marked on the DAQ board. Value range in `1 - 4`.
            demod_freqs (ndarray, optional): The 1-dimension numpy ndarray demod frequency. Defaults to `None`.
            demod_weights (ndarray, optional): The 3-dimension numpy ndarray demod weight , row 0 is I-data and row 1 is Q-data, The 3-dim for multi-frequency. Defaults to `None`.
            slot (int, optional): The slot number of the DAQ board. Value in list `[4, 15]`. Defaults to `None`.

        Raises:
            DemodFrequencyLengthNotMatch: Demod frequency length not match
            FilterDataLengthOutOfRange: Filter data length out of range
            ChannelWrongError: Channel wrong error.

        Returns:
            Return demod i and q filter data.
        """
        channel_list = self.__channel_check(channel)
        slot = self.slot_check(slot)
        ram_address = const.MATCH_FILTER_RAM_OFFSET_ADDRESS
        ram_data = {i: b'' for i in range(len(ram_address))}
        if self.qubits_mode == 0:    # 16qubits
            group = 1
            qubit_max_demod_len = int(const.QUBITS_16_WINDOW_WIDTH * const.SAMPLE_RATE) // 16*16
            qubit_max_demod_time = const.QUBITS_16_WINDOW_WIDTH
        elif self.qubits_mode == 1:  # 8qubits
            group = 2
            qubit_max_demod_len = int(const.QUBITS_8_WINDOW_WIDTH * const.SAMPLE_RATE) // 16*16
            qubit_max_demod_time = const.QUBITS_8_WINDOW_WIDTH
        else:                        # 4qubits
            group = 4
            qubit_max_demod_len = int(const.QUBITS_4_WINDOW_WIDTH * const.SAMPLE_RATE) // 16*16
            qubit_max_demod_time = const.QUBITS_4_WINDOW_WIDTH

        qubit_num = int(const.RAM_NUM / group)
        # 解模频率列表数不应当大于qubit数据,例如当qubits_mode=1时为8qubit解模那么解模频率列表个数应当<=8,否则会超出ram会报错
        if len(demod_freqs) > qubit_num: 
            # demod_freqs = demod_freqs + [0] * (qubit_num-len(demod_freqs)) # 在频点列表后强制补0
            raise DemodFrequencyLengthNotMatch(len(demod_freqs), qubit_num)
        # 用户输入的多频点长度与解模窗口宽度列表以及解模窗口起始列表长度保持一致
        if len(self.demod_window_width) != len(demod_freqs) or len(self.demod_window_start) != len(demod_freqs):
            raise DemodWindowWidthAndStartNotMatch(len(demod_freq),len(self.demod_window_width),len(self.demod_window_start))
        # 如果是解模权重模式先对用户参数进行判定
        if any(any(sublist) for sublist in demod_weights) and (len(demod_weights) != 2 or len(demod_freqs[0]) != len(demod_weights[1])):
            # 对权重数据维度判定,防止用户输入错误
            raise DemodWeightDimensionNotMatch(len(demod_freqs),2,qubit_max_demod_len)            
        
        # 取解模窗口最小起始位置作为基点
        demod_window_start_np = np.array(self.demod_window_start)
        demod_window_width_np = np.array(self.demod_window_width)
        demod_endpoint_max = max(demod_window_start_np + demod_window_width_np)
        min_demod_start = min(self.demod_window_start)
        # 每一个频点的解模窗口宽度采样点数转换成采样时间
        t_array = [np.arange(i) / const.SAMPLE_RATE for i in self.demod_window_width]
        i_filter_ = []
        q_filter_ = []

        if demod_endpoint_max > qubit_max_demod_len: # 16频点的最大解模终点(self.demod_window_start[idx] + self.demod_window_width[idx])大于最大解模深度
            # 此模式下不应当有权重数据
            if any(any(sublist) for sublist in demod_weights):
            # if demod_weights is not None:
                raise ValueError("权重模式下的解模终点位置应当小于最大解模深度")
            else:
                for idx, demod_freq in enumerate(demod_freqs):
                    if not np.all(demod_window_start_np == demod_window_start_np[0]) or not np.all(demod_window_width_np == demod_window_width_np[0]):
                        warnings.warn(f"请注意各个频点的解模起始位置或解模宽度是否一致！系统将全频点设置解模起始位置0，解模窗口宽度{qubit_max_demod_time}")
                        self.logger.warning(f"请注意各个频点的解模起始位置或解模宽度是否一致！系统将全频点设置解模起始位置0，解模窗口宽度{qubit_max_demod_time}")
                    # 频率近似,保证波形首尾相接
                    num_samples = int(const.SAMPLE_RATE * qubit_max_demod_time)
                    num_period  = int(num_samples * demod_freq / const.SAMPLE_RATE)
                    demod_freq_apx = const.SAMPLE_RATE / ( num_samples / num_period) 
                    w = 2 * np.pi * demod_freq_apx
                    cos_wave = np.cos(w * qubit_max_demod_time)
                    sin_wave = -np.sin(w * qubit_max_demod_time)
                    i_filter_t = self.__filter_data_normalization(cos_wave).astype('<i2')
                    q_filter_t = self.__filter_data_normalization(sin_wave).astype('<i2')
                    i_filter_cpl = np.where(i_filter < 0, (~abs(i_filter) + 1) & 0xFFFF, i_filter & 0xFFFF).astype('<u4')
                    i_filter_.append(i_filter_cpl)
                    q_filter_cpl = np.where(q_filter < 0, (~abs(q_filter) + 1) & 0xFFFF, q_filter & 0xFFFF).astype('<u4')
                    q_filter_.append(q_filter_cpl)
                    # I high 16 bit, Q low 16 bit
                    iq_filter = i_filter_cpl << 16 | q_filter_cpl
                    # iq_filter = (cos_wave << 16) | sin_wave
                    new_filter = iq_filter.reshape(len(iq_filter)>>4,16) #iq解模时一个时钟周期解模16个采样数据

                    for k in range(group):
                        ram_data[idx * group + k] += new_filter[k::group, ::].tobytes()
        else:
            for idx, demod_freq in enumerate(demod_freqs):
                w = 2 * np.pi * demod_freq
                cos_wave = np.cos(w * t_array[idx])
                sin_wave = -np.sin(w * t_array[idx])
                # 在头部用0补齐起始位置采样点数(相对解模起始位置基点)，在尾部补齐qubit对应的解模总长度:16qubit->1.6384e-6s->8000, 8qubit->3.2768e-6s->16000, 4qubit->6.5536e-6s->32000
                pad_head = self.demod_window_start[idx] - min_demod_start
                pad_tail = demod_endpoint_max - self.demod_window_width[idx] - pad_head
                if any(any(sublist) for sublist in demod_weights) and any(demod_weights[0][idx]) and any(demod_freqs[1][idx]): # 如果权重数据不为空则IQ幅值需要乘以对应的权重数据
                    if len(demod_weights[0][idx]) != self.demod_window_width[idx] or len(demod_weights[1][idx]) != self.demod_window_width[idx]:
                        raise DemodWeightDimensionNotMatch(len(demod_freqs),2,self.demod_window_width[idx])
                    # 每一个频点对应一组解模权重，每一组解模权重对应一组I、Q列表
                    # 0 -> 深度，1-> 行数，2 -> 列数
                    demod_weights_t_i = np.array(demod_weights[0][idx])
                    demod_weights_t_q = np.array(demod_weights[1][idx])
                    i_filter_t = np.ceil(self.__filter_data_normalization(cos_wave) * demod_weights_t_i).astype('<i2')
                    q_filter_t = np.ceil(self.__filter_data_normalization(sin_wave) * demod_weights_t_q).astype('<i2')
                    i_filter = np.pad(i_filter_t, (pad_head,pad_tail),'constant',constant_values=0).astype('<i2') 
                    q_filter = np.pad(q_filter_t, (pad_head,pad_tail),'constant',constant_values=0).astype('<i2')
                else:
                    i_filter_t = self.__filter_data_normalization(cos_wave).astype('<i2')
                    q_filter_t = self.__filter_data_normalization(sin_wave).astype('<i2')
                    i_filter = np.pad(i_filter_t,(pad_head, pad_tail),'constant',constant_values=0).astype('<i2')
                    q_filter = np.pad(q_filter_t,(pad_head, pad_tail),'constant',constant_values=0).astype('<i2')
                i_filter_cpl = np.where(i_filter < 0, (~abs(i_filter) + 1) & 0xFFFF, i_filter & 0xFFFF).astype('<u4')
                i_filter_.append(i_filter_cpl)
                q_filter_cpl = np.where(q_filter < 0, (~abs(q_filter) + 1) & 0xFFFF, q_filter & 0xFFFF).astype('<u4')
                q_filter_.append(q_filter_cpl)
                # I high 16 bit, Q low 16 bit
                iq_filter = i_filter_cpl << 16 | q_filter_cpl
                # iq_filter = (cos_wave << 16) | sin_wave
                new_filter = iq_filter.reshape(len(iq_filter)>>4,16) #iq解模时一个时钟周期解模16个采样数据

                for k in range(group):
                    ram_data[idx * group + k] += new_filter[k::group, ::].tobytes()
        
        for idx, address in enumerate(ram_address):
            data = ram_data[idx]
            address += const.MATCH_FILTER_RAM_BASE_ADDRESS[channel-1]
            if len(data) > const.MAX_FILTER_LENGTH:
                raise FilterDataLengthOutOfRange(slot, len(data), const.MAX_FILTER_LENGTH)
            pad_cnt = 32 * 1024 - len(data)
            data += b'\x00' * pad_cnt
            if self.batch_mode:
                self.w_mem_packet.write_mem(address, data, slot)
            else:
                self.write_mem(address, data, slot)
                
        return i_filter_, q_filter_

    def __perpendicular_bisector_coefficients(self, p1:Tuple[np.int32,np.int32], p2:Tuple[np.int32,np.int32]):
        """计算通过两个点p1和p2的中垂线的方程的三个系数"""
        if p1[0] == p2[0]:
            # 如果两个点在同一条竖直线上，中垂线为水平线y = (p1[1] + p2[1]) / 2
            if p1[1] < (p1[1]+p2[1]) / 2:   
                return (0, 1, (p1[1] + p2[1]) / 2)
            else:
                return (0, -1, -(p1[1] + p2[1]) / 2)
        elif p1[1] == p2[1]:
            # 如果两个点在同一条水平线上，中垂线为竖直线x = (p1[0] + p2[0]) / 2
            if p1[0] < (p1[0] + p2[0]) / 2:
                return (1, 0, (p1[0] + p2[0]) / 2)
            else:
                return (-1, 0, -(p1[0] + p2[0]) / 2)
        else:
            # 其他情况下，中垂线的斜率为-1/k，其中k是p1和p2之间的斜率
            k = (p2[1] - p1[1]) / (p2[0] - p1[0])
            m = -1 / k
            mid = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
            b = mid[1] - m * mid[0]
            if -p1[0]*m + p1[1] < b:
                return (-m, 1, b)
            else:
                return (m, -1, -b)
        
    def set_mulstate_disc_params(self, channel: Union[int, list], pointlist: List[Tuple[np.int32,np.int32]], qubit_index: int, slot: Union[int, None] = None) -> Tuple[list, list, list]:
        """
        <a id="daq4">Set the state judgment parameters</a>

        Note:
            1. A total of 4 channels, 16 qubits per channel need to be judged, and the issuing address refers to 
            the register offset address.
            2. When the A and B parameters are combined, A is 16 bits high and B is 16 bits lower.

        Raises:
            ChannelWrongError: Channel wrong error.

        Args:
            channel (int, list): The channel number that is actually marked on the DAQ board. Value range in `1 - 4`.
            pointlist (List[Tuple[np.int32,np.int32]]): A,B,C point tuple list.
            qubit_index (int): The qubit index. Value range in `0 - 15`
            slot (int, optional): The slot number of the DAQ board. Value in list `[4, 15]`. Defaults to `None`.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal.
        """
        data = [0] * 9 # a:data[0],data[1],data[2],b:data[3],data[4],data[5],c:data[6],data[7],data[8]
        if len(pointlist) == 2:
            data[0],data[3],data[6] = self.__perpendicular_bisector_coefficients(pointlist[0],pointlist[1])
            data[1],data[4],data[7] = self.__perpendicular_bisector_coefficients(pointlist[1],pointlist[0])
            data[2],data[5],data[8] = [data[0],data[3],data[6]]
        elif len(pointlist) == 3:
            data[0],data[3],data[6] = self.__perpendicular_bisector_coefficients(pointlist[0],pointlist[2])
            data[1],data[4],data[7] = self.__perpendicular_bisector_coefficients(pointlist[1],pointlist[0])
            data[2],data[5],data[8] = self.__perpendicular_bisector_coefficients(pointlist[2],pointlist[1])
        else:
            raise Exception("Point number error")
        estmA = [0] * 3
        estmB = [0] * 3
        estmC = [0] * 3
        for i in range(3):
            max_abs_ab = max(abs(data[i]),abs(data[i+3]))
            if max_abs_ab != 0:
                scale = 32767/max_abs_ab #缩放为16位有符号整形数据
                # a高16位 b低16位 合并为1个32为数
                estmA[i] = int(data[i]*scale) 
                estmB[i] = int(data[i+3]*scale)
                # c独立32位数
                estmC[i] = int(data[i+6]*scale) >> 8
        self.__set_state_estm_params(channel=channel,estmA_list=estmA,estmB_list=estmB,estmC_list=estmC,qubit_index=qubit_index,slot=slot)
        return estmA, estmB, estmC

    def __set_state_estm_params(self, channel: Union[int, list], estmA_list: list, estmB_list: list, estmC_list: list, qubit_index: int, slot: Union[int, None] = None) -> int:
        """
        <a id="daq4">Set the state judgment parameters</a>

        Note:
            1. A total of 4 channels, 16 qubits per channel need to be judged, and the issuing address refers to 
            the register offset address.
            2. When the A and B parameters are combined, A is 16 bits high and B is 16 bits lower.

        Raises:
            ChannelWrongError: Channel wrong error.

        Args:
            channel (int, list): The channel number that is actually marked on the DAQ board. Value range in `1 - 4`.
            estmA_list (list): The estmA list.
            estmB_list (list): The estmB list.
            estmC_list (list): The estmC list.
            qubit_index (int): The qubit index. Value range in `0 - 15`
            slot (int, optional): The slot number of the DAQ board. Value in list `[4, 15]`. Defaults to `None`.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal.
        """
        channel_list = self.__channel_check(channel)
        slot = self.slot_check(slot)
        idx = 0
        if self.batch_mode:
            for ch in channel_list:
                for estmA, estmB, estmC in zip(estmA_list, estmB_list, estmC_list):
                    A_B_reg = f'DAQ_{ch-1}.STATE_EST_Q{qubit_index}_AB_{idx}'
                    C_reg = f'DAQ_{ch-1}.STATE_EST_Q{qubit_index}_C_{idx}'
                    estmA_cpl = cacl_twos_complement(estmA, bit_width=0xFFFF)
                    estmB_cpl = cacl_twos_complement(estmB, bit_width=0xFFFF)
                    estmC_cpl = cacl_twos_complement(estmC, bit_width=0xFFFFFFFF)
                    A_B_cpl = (estmA_cpl << 16) | estmB_cpl
                    self.reg_packet[slot, A_B_reg] = A_B_cpl
                    self.reg_packet[slot, C_reg] = estmC_cpl
                    idx += 1
        else:
            for ch in channel_list:
                for estmA, estmB, estmC in zip(estmA_list, estmB_list, estmC_list):
                    A_B_reg = f'DAQ_{ch-1}.STATE_EST_Q{qubit_index}_AB_{idx}'
                    C_reg = f'DAQ_{ch-1}.STATE_EST_Q{qubit_index}_C_{idx}'
                    estmA_cpl = cacl_twos_complement(estmA, bit_width=0xFFFF)
                    estmB_cpl = cacl_twos_complement(estmB, bit_width=0xFFFF)
                    estmC_cpl = cacl_twos_complement(estmC, bit_width=0xFFFFFFFF)
                    A_B_cpl = (estmA_cpl << 16) | estmB_cpl
                    self[slot, A_B_reg] = A_B_cpl
                    self[slot, C_reg] = estmC_cpl
                    idx += 1
        return 0

    def set_daq_enable(self, channel: Union[int, list], mode: Union[int, None] = None, ts_mask: Union[int, None] = None, slot: Union[int, None] = None) -> int:
        """
        <a id="daq5">DAQ module enable: Set bit[6:4] to 1 to realize wave mode, demo mode and state mode reset</a>

        Notes:
            The value of the mode parameter and its meaning:

            | mode value | patterns of DAQ | description | 
            | :--------: | :-------------: | :---------: |
            |      0     |    WAVE_MODE    |             |
            |      1     |    DEMO_MODE    |             |
            |      2     |    STATE_MODE   |             |
            |      3     |    FEED_MODE    |             |

            Trigger mask definition (active high):

            |       bit       |                definition                       |
            | :-------------: | :---------------------------------------------: |
            |     bit[19:0]   |  sequence controller generation trigger         |
            |     bit[20]     |  internal rising edge simulates trigger masks   |
            |     bit[21]     |  internal falling edge simulates trigger masks  |
            |     bit[22]     |  external hardware trigger signal               |
            |     bit[23]     |  internal software trigger signal               |

            `When the mode is FEED_MODE, bit [15:0] is also used to control the generation of feedback pulses.`

        Raises:
            ChannelWrongError: Channel wrong error.
            ModeWrongError: Mode wrong error

        Args:
            channel (int, list): The channel number that is actually marked on the DAQ board. Value range in `1 - 4`.
            mode (int, optional): The Patterns of DAQ experiments. value in list `[0, 1, 2, 3]` and `mode = 0 -> WAVE_MODE`, `mode = 1 -> DEMO_MODE`, `mode = 2 -> STATE_MODE`, `mode = 3 -> FEED_MODE. Defaults to `None`.
            ts_mask (int, optional): The trigger mask. Defaults to `None`.
            slot (int, optional): The slot number of the DAQ board. Value in list `[4, 15]`. Defaults to `None`.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal.
        """

        channel_list = self.__channel_check(channel)
        slot = self.slot_check(slot)
        mode = self.__mode_check(mode)
        
        if self.batch_mode:
            for ch in channel_list:
                command_reg = f'DAQ_{ch-1}.COMMAND'
                if mode == const.WAVE_MODE: 
                    reset_wave = 1 << 4 # 波形复位
                    ts_mask_reg = f'DAQ_{ch - 1}.WAVE_STORE_TS_MASK'
                    ts_mask = 1 << 16 if ts_mask is None else ts_mask # 内部波形触发掩码
                elif mode == const.DEMO_MODE:
                    reset_wave = 1 << 5 # 解模复位
                    ts_mask_reg = f'DAQ_{ch - 1}.DEMOD_STORE_TS_MASK' # 内部解模触发掩码
                    ts_mask = 1 << 17 if ts_mask is None else ts_mask  
                elif mode == const.STATE_MODE:
                    reset_wave = 1 << 6 # 态判断复位
                    ts_mask_reg = f'DAQ_{ch - 1}.RDOUT_STORE_TS_MASK'
                    ts_mask = 1 << 18 if ts_mask is None else ts_mask # 内部态判断触发掩码
                else:
                    ts_mask_reg = f'DAQ_{channel-1}.FB_TS_MASK'
                    ts_mask = 1 << 19 if ts_mask is None else ts_mask # 内部反馈触发掩码
                
                self.reg_packet[slot, ts_mask_reg] = ts_mask
                self.reg_packet[slot, command_reg] = reset_wave
        else:
            for ch in channel_list:
                command_reg = f'DAQ_{ch-1}.COMMAND'
                if mode == const.WAVE_MODE: 
                    # 波形复位
                    reset_wave = 1 << 4
                    # 内部波形触发掩码
                    ts_mask_reg = f'DAQ_{ch - 1}.WAVE_STORE_TS_MASK'
                    ts_mask = 1 << 16 if ts_mask is None else ts_mask 
                elif mode == const.DEMO_MODE:
                    # 解模复位
                    reset_wave = 1 << 5 
                    # 内部解模触发掩码
                    ts_mask_reg = f'DAQ_{ch - 1}.DEMOD_STORE_TS_MASK' 
                    ts_mask = 1 << 17 if ts_mask is None else ts_mask
                elif mode == const.STATE_MODE:
                    # 态判断复位
                    reset_wave = 1 << 6
                    # 内部态判断触发掩码
                    ts_mask_reg = f'DAQ_{ch - 1}.RDOUT_STORE_TS_MASK'
                    ts_mask = 1 << 18 if ts_mask is None else ts_mask 
                else:
                    # 内部反馈触发掩码
                    ts_mask_reg = f'DAQ_{channel-1}.FB_TS_MASK'
                    ts_mask = 1 << 19 if ts_mask is None else ts_mask 

                self[slot, ts_mask_reg] = ts_mask
                self[slot, command_reg] = reset_wave

    def __daq_flush(self, channel: int, mode: Union[int, None] = None, slot: Union[int, None] = None) -> int:
        """
        Set bit[9:7] to 1 to realize wave mode, demo mode and state mode data flush, after the end of the experiment or 
        the unexpected termination, flush the cached data into DDR3

        Notes:
            The value of the mode parameter and its meaning:

            | mode value | patterns of DAQ |                                     description                                        | 
            | ---------- |-----------------|----------------------------------------------------------------------------------------|
            |      0     |    WAVE_MODE    | After the experiment or terminates unexpectedly, flush the cached wave data into DDR3  |
            |      1     |    DEMO_MODE    | After the experiment or terminates unexpectedly, flush the cached demo data into DDR3  |
            |      2     |    STATE_MODE   | After the experiment or terminates unexpectedly, flush the cached state data into DDR3 |

        Raises:
            ChannelWrongError: Channel wrong error.
            ModeWrongError: Mode wrong error

        Args:
            channel (int): The channel number that is actually marked on the DAQ board. Value range in `1 - 4`.
            mode (int, optional): The Patterns of DAQ experiments. value in list `[0, 1, 2]` and `mode = 0 -> WAVE_MODE`, `mode = 1 -> DEMO_MODE`, `mode = 2 -> STATE_MODE`. Defaults to `None`.
            slot (int, optional): The slot number of the DAQ board. Value in list `[4, 15]`. Defaults to `None`.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal.
        """
        self.__channel_check(channel)
        slot = self.slot_check(slot)
        mode = self.__mode_check(mode)
        command_reg = f'DAQ_{channel-1}.COMMAND'
        if mode == const.WAVE_MODE:
            set_value = 1 << 7
        elif mode == const.DEMO_MODE:
            set_value = 1 << 8
        else:
            set_value = 1 << 9
        self.set_reg(slot, command_reg, set_value)
        return 0

    def __get_sample_status(self, channel: int, mode: Union[int, None] = None, slot: Union[int, None] = None) -> int:
        """
        Get the data count of WAVE_MODE、DEMO_MODE、RDOUT

        Args:
            channel (int): The channel number that is actually marked on the DAQ board. Value range in `1 - 4`.
            mode (int, optional): The Patterns of DAQ experiments. value in list `[0, 1, 2]` and `mode = 0 -> WAVE_MODE`, `mode = 1 -> DEMO_MODE`, `mode = 2 -> STATE_MODE`. Defaults to `None`.
            slot (int, optional): The slot number of the DAQ board. Value in list `[4, 15]`. Defaults to `None`.

        Raises:
            ChannelWrongError: Channel wrong error.
            ModeWrongError: Mode wrong error

        Returns:
            The program ends normally with return value `0`, otherwise abnormal.
        """
        self.__channel_check(channel)
        slot = self.slot_check(slot)
        mode = self.__mode_check(mode)
        if mode == const.WAVE_MODE:
            reg = f'DAQ_{channel-1}.WAVE_DATA_COUNT'
        elif mode == const.DEMO_MODE:
            reg = f'DAQ_{channel-1}.DEMOD_DATA_COUNT'
        else:
            reg = f'DAQ_{channel-1}.RDOUT_DATA_COUNT'
        count_bytes = self[slot, reg]
        count, = unpack('<I', count_bytes)
        return count

    def __data_acquisition_process(self, channel: int, mode: int, start_addr, data_segment, expected_cnt, analysis_process, timeout=None):
        t_start = time.time()
        if timeout is None:
            timeout = 20 # 读取超时默认20s
        offset = 0
        received_bytes = bytearray(expected_cnt)
        received_data = None
        max_4kb_aqcuire_times = int(expected_cnt // 4096)
        cur_4kb_acquire_times = 0
        already_done_trig = 0
        begin = time.time()
        address = start_addr

        read_mem_time = 0
        handle_data_time = 0
        while offset < expected_cnt:
            already_done = self.__get_sample_status(channel, mode)
            time.sleep(0.01)
            bytes_cnt = already_done - offset
            # read 4KB per time
            if cur_4kb_acquire_times < max_4kb_aqcuire_times and max_4kb_aqcuire_times > 0:
                acquire_cnt = int(bytes_cnt // 4096)
                # address = start_addr + offset
                if acquire_cnt:
                    length = acquire_cnt * 4096
                    t1 = time.time()
                    raw_data = self.read_mem(address, length, self.slot)
                    t2 = time.time()
                    read_mem_time += t2 - t1
                    received_bytes[offset:offset+length] = raw_data
                    offset += length
                    address += length
                    cur_4kb_acquire_times += acquire_cnt
            else:
                # 如果数据不满4kb,先判断expected_cnt==already_done(保障最后的数据写到RAM)，之后再冲刷数据到DDR
                if expected_cnt == already_done:
                    self.__daq_flush(channel, mode)
                    raw_data = self._byte_mapper[address:address+bytes_cnt]
                    received_bytes[offset:offset+bytes_cnt] = raw_data
                    offset = expected_cnt
                    # offset = already_done
                    
            # handle data that received
            # if mode == const.STATE_MODE:
            #     # wait until all triggers have been done
            #     # if offset == expected_cnt:
            #     if expected_cnt == already_done:
            #         received_data = analysis_process(received_bytes,data_segment)
            # else:
                # once trigger have been done, convert the bytes to data
            trig_cnt = int(offset // data_segment)
            handle_trig_cnt = trig_cnt - already_done_trig
            if handle_trig_cnt != 0:
                start_bytes = already_done_trig * data_segment
                end_bytes = already_done_trig * data_segment + handle_trig_cnt * data_segment
                t1 = time.time()
                if mode == const.STATE_MODE:
                    data = analysis_process(received_bytes[start_bytes:end_bytes], data_segment)
                else:
                    desc, data = analysis_process(received_bytes[start_bytes:end_bytes], data_segment)
                t2 = time.time()
                handle_data_time += t2 - t1
                if received_data is None:
                    received_data = data
                else:
                    received_data = np.concatenate((received_data, data))
                already_done_trig = trig_cnt
            if offset == expected_cnt:
                break
            end = time.time()
            if end - begin > timeout :
                raise ReceiveDataTimeOut(self.slot, timeout)
        t_end = time.time()
        self.logger.info(f'    read {expected_cnt / 1024 / 1024:0.2f}M raw data from daq cost time: {read_mem_time:.3f}')
        self.logger.info(f'    convert all raw data to iq/wave/state data cost time: {handle_data_time:.3f}')
        self.logger.info(f'    receive data cost time: {t_end - t_start}')
        return received_data

    def get_daq_data(self, channel: Union[int, list], mode: Union[int, None] = None,start_address: Union[int, None] = None, timeout: Union[int, None] = None, slot: Union[int, None] = None) -> Union[np.ndarray, np.ndarray, np.ndarray]:
        """
        <a id="daq6">Read data of WAVE_MODE、DEMO_MODE、STATES_MODE from corresponding start address</a>

        Args:
            channel (int): The channel number that is actually marked on the DAQ board. Value range in `1 - 4`.
            slot (int, optional): The slot number of the DAQ board. Value in list `[4, 15]`. Defaults to `None`.
            timeout (int, optional): receive timeout. Defaults to None.
            start_address (int, optional): start address of corresponding mode. Defaults to None.

        Raises:
            ModeWrongError: Mode wrong error
            
        Returns:
            The program ends normally with return value `0`, otherwise abnormal
        """
        mode = self.__mode_check(mode)
        slot = self.slot_check(slot)
        if mode == const.WAVE_MODE:
            if start_address is None:
                wave_start_address = const.WAVE_DATA_ADDR_MALLOC[channel-1] # >> 12
            else:
                wave_start_address = start_address
            # 1 bytes per point
            data_segment = const.WAVE_DATA_HEAD_LENGTH + self.sample_depth
            expected_bytes = data_segment * self.sample_count
            wave_data = self.__data_acquisition_process(channel, const.WAVE_MODE, wave_start_address, data_segment,
                            expected_bytes, ReadoutDataAnalysis.wave_data_analysis,timeout=timeout)
            wave_mat = np.array(wave_data).reshape(self.sample_count, self.sample_depth)
            return wave_mat
            
        elif mode == const.DEMO_MODE:
            if start_address is None:
                demod_start_address = const.DEMOD_DATA_ADDR_MALLOC[channel-1] # >> 12
            else:
                demod_start_address = start_address
            # demod_start_address = DAQUnit.DEMOD_DATA_ADDR_MALLOC[channel-1]
            data_segment = const.DEMOD_DATA_LENGTH
            expected_bytes = data_segment * self.sample_count
            iq_data = self.__data_acquisition_process(channel, const.DEMO_MODE, demod_start_address, data_segment,
                            expected_bytes, ReadoutDataAnalysis.demod_data_analysis,timeout=timeout)
            i_data = iq_data[::2]
            q_data = iq_data[1::2]
            i_mat = np.array(i_data).reshape(self.sample_count, const.DEMOD_FREQ_COUNT)
            q_mat = np.array(q_data).reshape(self.sample_count, const.DEMOD_FREQ_COUNT)
            return i_mat, q_mat
        elif mode == const.STATE_MODE:
            data_segment = const.STATES_DATA_LENGTH
            # 期望字节数(expected_bytes)=单次触发4字节(data_segment) * 触发次数(self.sample_count)
            expected_bytes = data_segment * self.sample_count
            if start_address is None:
                states_start_address = const.STATE_DATA_ADDR_MALLOC[channel-1] # >> 12
            else:
                states_start_address = start_address
            states_data = self.__data_acquisition_process(channel, const.STATE_MODE, states_start_address, data_segment,
                            expected_bytes, ReadoutDataAnalysis.state_data_analysis,timeout=timeout)
            state_mat = np.array(states_data).reshape(self.sample_count, const.RDOUT_FREQ_COUNT)
            return state_mat
            
        else:
            raise ModeWrongError(self.slot, mode)

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

    def download_qr_wave_seq(self, gen_type:str, channel: Union[int, list], wave: Union[np.ndarray,list], seq: Union[np.ndarray,list], slot: Union[int, None] = None) -> int:
        """
        <a id="daq7">Write wave data to awg BRAM.</a>

        Args:
            gen_type (str): The generator type. Value is `ifout` or `ifin` , `ifout -> wave generator` and `ifin -> timing generator`. 
            channel (int, list): The channel number that is actually marked on the DAQ board. Value range in `1 - 4`.
            wave (ndarray,list): If wave is numpy ndarray, the wave data must be 2-dimension numpy ndarray, row 0 is I-data and row 1 is Q-data, if wave data is list the wave data is 16 bit I,Q alternating data or I,Q merging into 32-bit data list. Please refer to the user manual for wave generation instructions.
            seq (ndarray,list): If seq is numpy ndarray, the seq must be 1-dimension numpy ndarray or 2-dimension numpy data with n rows and 4 columns Each row represents a control instruction. Please refer to the user manual for wave generation instructions.
            slot (int, optional): The slot number of the DAQ board. Value in list `[4, 15]`. Defaults to `None`.

        Raises:
            ChannelWrongError: Input the wrong channel number.
            WaveLengthOutOfRange: Wave length out of range.
            GeneratorTypeWrongError: Generator type wrong error.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal.
        """
        channel_list = self.__channel_check(channel)
        slot = self.slot_check(slot)
        # wave
        if isinstance(wave,np.ndarray) and wave.shape[0] != 2:
            WaveTypeOrDimensionWrongError(self.name,type(wave),wave.ndim)
        wave_bytes_data,wave_length = self.__bytes_completion(data=wave,format_type='wave')
        # seq
        seq_bytes_data,seq_length = self.__bytes_completion(data=seq,format_type='seq')

        if self.batch_mode:
            for ch in channel_list:
                if gen_type == 'ifout' or gen_type == 'ro':
                    wave_start_addr = const.DAC_WAVE_DATA_ADDR[ch-1] # DAC数据地址
                    seq_start_addr = const.DAC_WAVE_SEQ_ADDR[ch-1] # DAC序列地址
                elif gen_type == 'ifin' or gen_type == 'ri':
                    wave_start_addr = const.DAC_TIMING_DATA_ADDR[ch-1] # DAC数据地址
                    seq_start_addr = const.DAC_TIMING_SEQ_ADDR[ch-1] # DAC序列地址
                else:
                    raise GeneratorTypeWrongError(self.name,gen_type)
                
                self.w_mem_packet.write_mem(wave_start_addr, wave_bytes_data, slot)
                self.w_mem_packet.write_mem(seq_start_addr, seq_bytes_data, slot)
        else:
            for ch in channel_list:
                if gen_type == 'ifout' or gen_type == 'ro':
                    wave_start_addr = const.DAC_WAVE_DATA_ADDR[ch-1] # DAC数据地址
                    seq_start_addr = const.DAC_WAVE_SEQ_ADDR[ch-1] # DAC序列地址
                elif gen_type == 'ifin' or gen_type == 'ri':
                    wave_start_addr = const.DAC_TIMING_DATA_ADDR[ch-1] # DAC数据地址
                    seq_start_addr = const.DAC_TIMING_SEQ_ADDR[ch-1] # DAC序列地址
                else:
                    raise GeneratorTypeWrongError(self.name,gen_type)

                self.write_mem(wave_start_addr, wave_bytes_data, slot)
                self.write_mem(seq_start_addr, seq_bytes_data, slot)
        return 0
    
    def set_qr_on_off(self, gen_type:str, channel: Union[int, list], on_off: str, slot: Union[int, None] = None) -> int:
        """
        <a id="daq8">Start or Stop daq channel output wave.</a>

        Args:
            gen_type (str): The generator type. Value is `ifout` or `ifin` , `ifout -> wave generator` and `ifin -> timing generator`. 
            channel (int): The channel number that is actually marked on the DAQ board. Value range in `1 - 4`.
            on_off (str): The Flag of start / stop daq channel output wave. Value is `on` or `off` , `on -> start` and `off -> stop`.
            slot (int, optional): The slot number of the DAQ board. Value in list `[4, 15]`. Defaults to `None`.

        Raises:
            ChannelWrongError: Input the wrong channel number.
            GeneratorTypeWrongError: Generator type wrong error.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal.
        """
        channel_list = self.__channel_check(channel)
        slot = self.slot_check(slot)
        cmd = 0x01 if on_off == 'on' else 0x02
        if self.batch_mode:
            for ch in channel_list:
                if gen_type == 'ifout' or gen_type == 'ro':
                    register = f'DAC_WAVE_{ch-1}.CTRL_REG'
                elif gen_type == 'ifin' or gen_type == 'ri':
                    register = f'DAC_TIMING_{ch-1}.CTRL_REG'
                else:
                    raise GeneratorTypeWrongError(self.name,gen_type)

                self.reg_packet[slot, register] = cmd
        else:
            for ch in channel_list:
                if gen_type == 'ifout' or gen_type == 'ro':
                    register = f'DAC_WAVE_{ch-1}.CTRL_REG'
                elif gen_type == 'ifin' or gen_type == 'ri':
                    register = f'DAC_TIMING_{ch-1}.CTRL_REG'
                else:
                    raise GeneratorTypeWrongError(self.name,gen_type)

                self[slot, register] = cmd
        return 0 

    def set_reset_pulse_width(self, channel: Union[int, list], pulse1_width: float, pulse2_width: float, slot: Union[int, None] = None) -> int:
        """
        <a id="daq9">Feedback pulse control</a>

        Note:
            The microwave switch is normally open, and when actively reset, the output of a specific waveform is blocked by pulling 
            the control pulse low. pulse_width1 and pulse_width2 are used to control the width of the 1-state and 2-state reset pulses, 
            respectively, and the number of clock cycles per unit hour (the clock frequency is tentatively set at 312.5MHz)

            The pulse2_width entered by the user is measured in seconds and automatically converted into the number of pulses in the program.

        Args:
            channel (int, list): The channel number that is actually marked on the DAQ board. Value range in `1 - 4`.
            pulse1_width (int): The pulse1_width entered by the user is measured in seconds and automatically converted into the number of pulses in the program.
            pulse2_width (int): The pulse2_width entered by the user is measured in seconds and automatically converted into the number of pulses in the program.
            slot (int, optional): The slot number of the DAQ board. Value in list `[4, 15]`. Defaults to `None`.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal
        """
        channel_list = self.__channel_check(channel)
        slot = self.slot_check(slot)
        if self.batch_mode:
            for ch in channel_list:
                pulse1_reg = f'DAQ_{ch-1}.PULSE_WIDTH1'
                pulse2_reg = f'DAQ_{ch-1}.PULSE_WIDTH2'
                self.reg_packet[slot, pulse1_reg] = int((pulse1_width * 1e9) / 3.2)
                self.reg_packet[slot, pulse2_reg] = int((pulse2_width * 1e9) / 3.2)
        else:
            for ch in channel_list:
                pulse1_reg = f'DAQ_{ch-1}.PULSE_WIDTH1'
                pulse2_reg = f'DAQ_{ch-1}.PULSE_WIDTH2'
                self[slot, pulse1_reg] = int((pulse1_width * 1e9) / 3.2)
                self[slot, pulse2_reg] = int((pulse2_width* 1e9) / 3.2)
        return 0

    def run_circuit(self, command: int = 1, slot: Union[int, None] = None) -> int:
        """
        <a id="daq10">Set synchronization command</a>

        Notes:
            The synchronization command is issued to initiate system synchronization, the corresponding bit is written to 1 to issue the command, 
            and the register is self-clearing:

            |       bit       |                          definition                        |
            | :-------------: | :--------------------------------------------------------: |
            |     bit[0]      |  A global synchronization command is issued in master mode |
            |     bit[1]      |  Upper computer control sends internal trigger commands    |
            |     bit[2]      |  Load sync signal input delay                              |
            |     bit[3]      |  Load cascaded signal input delay                          |
            |     bit[7:4]    |  Undefined                                                 |
            |     bit[8]      |  Reset synchronous generation state machine                |
            |     bit[9]      |  Reset trigger generation state machine                    |
            |     bit[10]     |  Clear synchronization delay statistics error count        |
            |     bit[11]     |  Clear cascading delay statistics error count              |
            |     bit[31:12]  |  Undefined                                                 |

        Args:
            commnad (int): Synchronous command values. the corresponding bit is written to 1 to issue the command
            slot (int, optional): The slot number of the DAQ board. Value in list `[4, 15]`. Defaults to `None`.
        Raises:
            ChannelWrongError: Input the wrong channel number.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal.
        """
        slot = self.slot_check(slot)
        reg = f'SYNC.COMMAND'
        self.set_reg(slot, reg, command)
        return 0

    @staticmethod
    def sync_system_clk(peripheral_list, delay:float = 5) -> int:
        """
        <a id="daq10">Sync system clock</a>

        Notes:
            0 -> : 单机箱master
            1 -> cas: 多机箱master
            2 -> slave: 丛集箱

            | definition |  value  |         describe       |
            | :--------: | :-----: | :--------------------: |
            |   master   |    0    |      single master     |
            |   cas      |    1    |      multiple master   |
            |   slave    |    2    |      slave             |

        Args:
            peripheral_list (list): DAQ object

        Returns:
            The program ends normally with return value `0`, otherwise abnormal.
        """

        def sync_input_delay(master, peripheral_list, delay: float = 0.5) -> int:
            """
            # 在10 / 62.5MHz时钟域下，校准列表中所有读取单元的输入同步延时

            Args:
                peripheral_list (List[DAQUnit]): List of objects to be synchronized

            Returns:
                The program ends normally with return value `0`, otherwise abnormal.
            """
            command_reg = 0
            command_reg |= 1<<10 # bit[10]=1 -> 清空同步延时统计错误计数
            command_reg |= 1<<2 # bit[2]=1 -> 加载同步信号输入延时
            master.set_reg(master.slot,'SYNC.INTRA_CYCLE_P',int(100000))
            master.set_reg(master.slot,'SYNC.INTRA_CYCLE_C',int(2))
            err_cnt_arr=np.zeros((len(peripheral_list), 32))
            for i in range(32):
                for index,per in enumerate(peripheral_list):
                    per.set_reg(per.slot,'SYNC.SYNC_CTRL',int(i))
                    per.set_reg(per.slot,'SYNC.COMMAND',command_reg)
                master.set_reg(master.slot,'SYNC.COMMAND',1)# bit[0]=1 -> 向板外发出全局同步命令
                time.sleep(delay) # 延时50ms用于保障同步脉冲发送完毕
                for index,per in enumerate(peripheral_list):
                    sync_ctrl_value = bytes_to_int(per.get_reg(per.slot,'SYNC.SYNC_CTRL'))
                    err_cnt = sync_ctrl_value>>16 # 取低16-31位为周期校准错误计数值
                    err_cnt_arr[index][i] = err_cnt
            # 找最佳参数
            for index,per in enumerate(peripheral_list):        
                # 此处找出数组中离1最远的0的的位置
                best_tap = find_best_tap(err_cnt_arr[index])
                per.set_reg(per.slot,'SYNC.SYNC_CTRL',best_tap)
                per.set_reg(per.slot,'SYNC.COMMAND',0x4) # bit[2]=1 -> 加载同步信号输入延时
            
            # 复位参数
            master.set_reg(master.slot,'SYNC.INTRA_CYCLE_P',int(1))
            master.set_reg(master.slot,'SYNC.INTRA_CYCLE_C',int(1))      
            return 0
        
        master = None # master对象
        master_cnt = 0 # master计数
        # 第一步找出master以及检测master,slave对象数是否合理
        for index,per in enumerate(peripheral_list):
            if per.sync_mode == 0 or per.sync_mode == 1:
                master_cnt += 1
                master = per
        if master_cnt != 1:
            raise ValueError(f'please check master number! current master number is {master_cnt}')

        if master.sync_mode == 0:
            # 单机箱 bit[1] = 1
            reg_value = [1] * (len(peripheral_list))
        else:
            # 默认多机箱模式 bit[0] = 0
            reg_value = [0] * (len(peripheral_list))

        # master 设置为主控机箱 其他设置为从机箱 同步10MHz时钟域
        for index, per in enumerate(peripheral_list):
            if per.sync_mode == 0 or per.sync_mode == 1:
                # master 设置为主控机箱 其他设置为从机箱 同步10MHz时钟域
                reg_value[index] |= 1<<1 # bit[1]=1 -> master设置为主控机箱
            else:
                reg_value[index] &= ~(1<<1) # bit[1]=0 -> 其余待同步对象设置为从机箱
            reg_value[index] |= 1<<4 # bit[4]=1 -> 设置10MHz时钟域
            per.set_reg(per.slot,'SYNC.FUNCTION',reg_value[index])
        
        # 在10MHz时钟域下，校准列表中所有读取单元的输入同步延时
        # sync_input_delay(master,peripheral_list,delay=0.5)
        for index, per in enumerate(peripheral_list):
            reg_value[index] |= 1<<2 # bit[2]=1 -> 打开时钟芯片同步
            per.set_reg(per.slot,'SYNC.FUNCTION',reg_value[index])
        master.set_reg(master.slot,'SYNC.COMMAND',1)# bit[0]=1 -> 由master对象向板外发出全局同步命令
        time.sleep(delay)
        # 同步62.5MHz时钟域
        for index, per in enumerate(peripheral_list):
            reg_value[index] &= ~(1<<2) #bit[2]=0 -> 关闭时钟芯片同步
            reg_value[index] &= ~(1<<4) # bit[4]=0 -> 62.5MHz
            per.set_reg(per.slot,'SYNC.FUNCTION',reg_value[index])

        # 在62.5MHz时钟域下，校准列表中所有读取单元的输入同步延时
        # sync_input_delay(master,peripheral_list,delay=0.08)

        # # 打开ADC芯片同步
        # for index, per in enumerate(peripheral_list):
        #     reg_value[index] |= 1<<3 #bit[3]=1 -> 打开ADC芯片同步
        #     per.set_reg(per.slot,'SYNC.FUNCTION',reg_value[index])
        # master.set_reg(master.slot,'SYNC.COMMAND',1)# bit[0]=1 -> 向板外发出全局同步命令

        # for per in peripheral_list: 
        #     per._DAQUnit__config_adc(chip_num=0,slot=per.slot) #  ADC校准延时
        #     per._DAQUnit__set_interrupt(slot=per.slot) # 设置ADC校准中断
        #     per._DAQUnit__config_adc(chip_num=1,slot=per.slot)
        #     per._DAQUnit__set_interrupt(slot=per.slot)
        return 0

    def __set_store_address(self, channel: int, page, mode: Union[int, None] = None, slot: Union[int, None] = None) -> int:
        """
        Set wave store addrees in wave mode

        Args:
            channel (int): The channel number that is actually marked on the DAQ board. Value range in `1 - 4`.
            page (int): The page(4KB) of the DDR3.
            mode (int, optional): The acquisition mode of DAQ. Defaults to None.
            slot (int, optional): The slot number of the DAQ board. Value in list `[4, 15]`. Defaults to `None`.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal
        """
        self.__channel_check(channel)
        slot = self.slot_check(slot)
        mode = self.__mode_check(mode)
        if mode == const.WAVE_MODE:
            store_addr_reg = f'DAQ_{channel-1}.WAVE_STORE_ADDR'
        elif mode == const.DEMO_MODE:
            store_addr_reg = f'DAQ_{channel-1}.DEMOD_STORE_ADDR'
        else:
            store_addr_reg = f'DAQ_{channel-1}.RDOUT_STORE_ADDR'
        self.set_reg(slot, store_addr_reg, page)
        return 0
    
    def __set_dds_update(self, slot: Union[int, None] = None) -> int:
        """
        Generate DDS configuration interrupt.Set the lowest bit to 1 to enable DDS configurations

        Args:
            slot (int, optional): The slot number of the DAQ board. Value in list `[4, 15]`. Defaults to `None`.

        Raises:
            ChannelWrongError: Input the wrong channel number.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal
        """
        slot = self.slot_check(slot)
        reg = 'DDS.REG2MICR_INTR'
        self.set_reg(slot, reg, 0x0000)
        time.sleep(1)
        self.set_reg(slot, reg, 0x0001)
        return 0

    def __set_dds_channel_sel(self, channel: int, slot: Union[int, None] = None) -> int:
        """
        Set DDS effective channel

        Args:
            channel (int): The channel number that is actually marked on the DAQ board. Value range in `1 - 4`.,and other values indicate that the 4 channels are fully open
            slot (int, optional): The slot number of the DAQ board. Value in list `[4, 15]`. Defaults to `None`.

        Raises:
            ChannelWrongError: Input the wrong channel number.

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

    def __set_dds_mode(self, mode:int = 0, slot: Union[int, None] = None) -> int:
        """
        Set DDS working mode

        Args:
            mode (int): 0 means normal mode=0x000000C (output frequency<1.25GHZ), 1 means mixing mode=0x00050C (output frequency>1.25GHZ), 2 means closing channel=0x02000C0
            slot (int, optional): The slot number of the DAQ board. Value in list `[4, 15]`. Defaults to `None`.
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

    def __set_dds_freq(self, frequency: int, slot: Union[int, None] = None) -> int:
        """
        Set DDS output frequency

        Args:
            frequency (int): frequency is the user's actual expectation that the output frequency exceeds the DDS frequency range, the unit is Hz.
            slot (int, optional): The slot number of the DAQ board. Value in list `[4, 15]`. Defaults to `None`.

        Raises:
            ChannelWrongError: Input the wrong channel number.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal
        """
        slot = self.slot_check(slot)
        # freq = frequency % 100e6 + 1.9e9 # frequency为用户实际期望输出频率超过DDS频率范围，故操作保留MHz数据并加入DDS的1.9GHz~2.0GHz范围中作为激励输出给mix
        freq = frequency #配合邵燕燕做但功能测试用
        freq_int = int(freq / 2.5e9*2**48)
        reg_high = 'DDS.FREQ_TUNING_WORD_H'
        reg_low = 'DDS.FREQ_TUNING_WORD_L'
        freq_low = freq_int & 0xFFFFFFFF
        freq_high = (freq_int >> 32) & 0xFFFF
        self.set_reg(slot, reg_high, freq_high)
        self.set_reg(slot, reg_low, freq_low)
        return 0

    def __set_dds_amp(self, amplitude, phase=0, slot: Union[int, None] = None) -> int:
        """
        Set DDS output amplitude

        Note:
            In this drive, the DDS output amplitude adopts 14-bit bit coding and the coding range is 0~16383, 
            so we establish a linear relationship between the amplitude encoding and the absolute output power 0 ~ 15dBm.
            The formula is : value = 16383 * amplitude / 15, Among them, the user input power range in 0 ~ 15 and unit is dBm, 
            and the linear output is 0 ~ 16383.

        Args:
            amplitude (int): The output power amplitude. value range in `0 ~ 15` and units is dBm
            phase (int): phase
            slot (int, optional): The slot number of the DAQ board. Value in list `[4, 15]`. Defaults to `None`.

        Raises:
            ValueError: Input the wrong range value.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal
        """
        slot = self.slot_check(slot)
        if amplitude < 0 or amplitude > 15:
            raise ValueError('The value of amplitude is abnormal, The normal power range in (0 ~ 15)')
        reg = 'DDS.PHASE_AMPLITUDE_CTRL'
        value = int(16383 * amplitude / 15)
        phase = int(phase)
        amp = (phase << 16) | value
        self.set_reg(slot, reg, amp)
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

    # def __set_dds_output(self,channel:int, mode: int, frequency: int, amplitude: int, slot: Union[int, None] = None) -> int:
    #     """
    #     Real time DDS chip configuration

    #     Args:
    #         channel (int): channel (int): The channel number that is actually marked on the DAQ board. Value range in `1 - 4`.
    #         ch_contr_h (int): 48bit channel control register 0 high 16bit
    #         ch_contr_l (int): 48bit channel control register 0 low 32bit
    #         mode (int): channel control register
    #         dac_current (int): DAC output current control word
    #         freq_h (int): 48bit frequency data, 16bit high
    #         freq_l (int): 48bit frequency data low 32bit
    #         amplitude (int): Amplitude control
    #         slot (int, optional): The slot number of the DAQ board. Value in list `[4, 15]`. Defaults to `None`.

    #     Raises:
    #         ValueError: Value Error.

    #     Returns:
    #         The program ends normally with return value `0`, otherwise abnormal
    #     """
    #     slot = self.slot_check(slot)
    #     self.__channel_check(channel)
    #     self.set_reg(slot, 'MULT_FUNC.MUL_FUNC_PARAM1', 1)
    #     self.set_reg(slot, 'MULT_FUNC.MUL_FUNC_PARAM2', 0)
    #     self.set_reg(slot, 'MULT_FUNC.MUL_FUNC_PARAM3', 0)
    #     # DDS通道选择
    #     if channel >= 1 and channel <= 4:
    #         self.set_reg(slot,'MULT_FUNC.MUL_FUNC_PARAM4',(1 << (channel + 3)))
    #     else:
    #         self.set_reg(slot, 'MULT_FUNC.MUL_FUNC_PARAM4', 0xF0)
    #     if mode == 0:
    #         self.set_reg(slot, 'MULT_FUNC.MUL_FUNC_PARAM7', 0x00000C)
    #     elif mode == 1:
    #         self.set_reg(slot, 'MULT_FUNC.MUL_FUNC_PARAM7', 0x00050C)
    #     elif mode == 2:
    #         self.set_reg(slot, 'MULT_FUNC.MUL_FUNC_PARAM7', 0x02000C)
    #     else:
    #         raise ValueError("设置DDS工作模式参数错误(0:普通模式,1:混频模式,2:关闭通道)")
    #     freq_int = int(frequency / 2.5e9*2**48)
    #     freq_high = (freq_int >> 32) & 0xFFFF
    #     self.set_reg(slot,'MULT_FUNC.MUL_FUNC_PARAM9',freq_high)
    #     freq_low = freq_int & 0xFFFFFFFF
    #     self.set_reg(slot,'MULT_FUNC.MUL_FUNC_PARAM10',freq_low)
    #     self.set_reg(slot,'MULT_FUNC.MUL_FUNC_PARAM11',int(amplitude))
    #     return 0

    # def __config_dds_realtime(self,channel:int,ch_contr_h:int,ch_contr_l:int, mode: int,dac_current:int , freq_h: int,freq_l: int, amplitude: int, slot: Union[int, None] = None) -> int:
    #     """
    #     Real time DDS chip configuration

    #     Args:
    #         channel (int): channel (int): The channel number that is actually marked on the DAQ board. Value range in `1 - 4`.
    #         ch_contr_h (int): 48bit channel control register 0 high 16bit
    #         ch_contr_l (int): 48bit channel control register 0 low 32bit
    #         mode (int): channel control register
    #         dac_current (int): DAC output current control word
    #         freq_h (int): 48bit frequency data, 16bit high
    #         freq_l (int): 48bit frequency data low 32bit
    #         amplitude (int): Amplitude control
    #         slot (int, optional): The slot number of the DAQ board. Value in list `[4, 15]`. Defaults to `None`.

    #     Raises:
    #         ValueError: Value Error.

    #     Returns:
    #         The program ends normally with return value `0`, otherwise abnormal
    #     """
    #     slot = self.slot_check(slot)
    #     self.__channel_check(channel)
    #     self.set_reg(slot, 'MULT_FUNC.MUL_FUNC_PARAM1', 1)
    #     self.set_reg(slot, 'MULT_FUNC.MUL_FUNC_PARAM2', 0)
    #     self.set_reg(slot, 'MULT_FUNC.MUL_FUNC_PARAM3', 0)
    #     # DDS通道选择
    #     if channel >= 1 and channel <= 4:
    #         self.set_reg(slot,'MULT_FUNC.MUL_FUNC_PARAM4',(1 << (channel + 3)))
    #     else:
    #         self.set_reg(slot, 'MULT_FUNC.MUL_FUNC_PARAM4', 0xF0)
    #     ch_h = (ch_contr_h & 0xFFFF)
    #     self.set_reg(slot,'MULT_FUNC.MUL_FUNC_PARAM5',ch_h)
    #     ch_l = (ch_contr_l & 0xFFFFFFFF)
    #     self.set_reg(slot,'MULT_FUNC.MUL_FUNC_PARAM6',ch_l)
    #     if mode == 0:
    #         self.set_reg(slot, 'MULT_FUNC.MUL_FUNC_PARAM7', 0x00000C)
    #     elif mode == 1:
    #         self.set_reg(slot, 'MULT_FUNC.MUL_FUNC_PARAM7', 0x00050C)
    #     elif mode == 2:
    #         self.set_reg(slot, 'MULT_FUNC.MUL_FUNC_PARAM7', 0x02000C)
    #     else:
    #         raise ValueError("设置DDS工作模式参数错误(0:普通模式,1:混频模式,2:关闭通道)")
    #     self.set_reg(slot, 'MULT_FUNC.MUL_FUNC_PARAM8', int(dac_current))
    #     self.set_reg(slot,'MULT_FUNC.MUL_FUNC_PARAM9',freq_h)
    #     self.set_reg(slot,'MULT_FUNC.MUL_FUNC_PARAM10',freq_l)
    #     self.set_reg(slot,'MULT_FUNC.MUL_FUNC_PARAM11',int(amplitude))
    #     return 0

    def __config_dds_gain(self, func_sel: int = 0, amplitude:List =[0,0,0,0],slot: Union[int, None] = None) -> int :
        """
        DDS chip configuration

        Args:
            func_sel (int, optional):Sub function selection, 0:configuration gain, 1:curing gain. Defaults to 0.
            amplitude (List, optional): Channel amplitude. Each value is represented by 8 bits. Defaults to [0,0,0,0].
            slot (int, optional): The slot number of the DAQ board. Value in list `[4, 15]`. Defaults to `None`.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal
        """
        slot = self.slot_check(slot)
        self.set_reg(slot, 'MULT_FUNC.MUL_FUNC_PARAM1', 2)
        self.set_reg(slot, 'MULT_FUNC.MUL_FUNC_PARAM2', func_sel) # 子功能选择
        self.set_reg(slot, 'MULT_FUNC.MUL_FUNC_PARAM3', 0)
        for channel in range(4):
            self.set_reg(slot, f'MULT_FUNC.MUL_FUNC_PARAM{channel + 4}', amplitude[channel]) # 设置通道channel幅值
        return 0
    
    def __config_dac9164(self,func_sel:int = 0,chip_num:int = 0, gain:int = 0,slot: Union[int, None] = None) -> int:
        """
        DAC9164 chip configuration

        Args:
            func_sel (int, optional): Sub function selection, 0:configuration gain, 1:curing gain. Defaults to 0.
            chip_num (int, optional): Chip number. Defaults to 0.
            gain (int, optional): Chip gain. represented by 8 bits. Defaults to 0.
            slot (int, optional): The slot number of the DAQ board. Value in list `[4, 15]`. Defaults to `None`.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal
        """
        slot = self.slot_check(slot)
        self.set_reg(slot, 'MULT_FUNC.MUL_FUNC_PARAM1', 3)
        self.set_reg(slot, 'MULT_FUNC.MUL_FUNC_PARAM2', func_sel) # 子功能选择
        self.set_reg(slot, 'MULT_FUNC.MUL_FUNC_PARAM3', chip_num) #芯片编号 0-3
        self.set_reg(slot, 'MULT_FUNC.MUL_FUNC_PARAM4', gain)  # 增益
        return 0

    def __config_adc(self,func_sel:int = 0,chip_num:int = 0,slot: Union[int, None] = None) -> int:
        """
        ADC chip calibration

        Args:
            func_sel (int, optional): Sub function selection, 0:configuration gain, 1:curing gain, 2:delay calibration. Defaults to 0.
            chip_num (int, optional): Chip number. Defaults to 0.
            slot (int, optional): The slot number of the DAQ board. Value in list `[4, 15]`. Defaults to `None`.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal
        """
        slot = self.slot_check(slot)
        self.set_reg(slot, 'MULT_FUNC.MUL_FUNC_PARAM1', 4)
        self.set_reg(slot, 'MULT_FUNC.MUL_FUNC_PARAM2', func_sel) # 子功能选择
        self.set_reg(slot, 'MULT_FUNC.MUL_FUNC_PARAM3', chip_num) #芯片编号 0-1
        return 0

    def __config_lmk04821(self,func_sel:int = 0,chip_num:int = 0,slot4_e_data:int = 0, slot4_b_data: int = 0,slot15_e_data:int = 0, slot15_b_data: int = 0) -> int:
        """
        Lmk04821 chip configuration of slot 4 and slot 15

        Args:
            func_sel (int, optional): Sub function selection. Defaults to 0.
            chip_num (int, optional): Chip number. Defaults to 0.
            slot4_e_data (int, optional): 0x015E Register Data of slot 4. Defaults to 0.
            slot4_b_data (int, optional): 0x015B Register Data of slot 4. Defaults to 0.
            slot15_e_data (int, optional): 0x015E Register Data of slot 15. Defaults to 0.
            slot15_b_data (int, optional): 0x015B Register Data of slot 15. Defaults to 0.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal
        """
        self.set_reg(4, 'MULT_FUNC.MUL_FUNC_PARAM1', 5)
        self.set_reg(4, 'MULT_FUNC.MUL_FUNC_PARAM2', func_sel) # 子功能选择
        # self.set_reg(4, 'MULT_FUNC.MUL_FUNC_PARAM3', chip_num) #芯片编号 0-1
        self.set_reg(4, 'MULT_FUNC.MUL_FUNC_PARAM4', slot4_e_data) #0x015E寄存器数据
        self.set_reg(4, 'MULT_FUNC.MUL_FUNC_PARAM5', slot4_b_data) #0x015B寄存器数据
        self.set_reg(4, 'MULT_FUNC.MUL_FUNC_PARAM6', slot15_e_data) #0x015E寄存器数据
        self.set_reg(4, 'MULT_FUNC.MUL_FUNC_PARAM7', slot15_b_data) #0x015B寄存器数据

        self.set_reg(15, 'MULT_FUNC.MUL_FUNC_PARAM1', 5)
        self.set_reg(15, 'MULT_FUNC.MUL_FUNC_PARAM2', func_sel) # 子功能选择
        # self.set_reg(15, 'MULT_FUNC.MUL_FUNC_PARAM3', chip_num) #芯片编号 0-1
        self.set_reg(15, 'MULT_FUNC.MUL_FUNC_PARAM4', slot4_e_data) #0x015E寄存器数据
        self.set_reg(15, 'MULT_FUNC.MUL_FUNC_PARAM5', slot4_b_data) #0x015B寄存器数据
        self.set_reg(15, 'MULT_FUNC.MUL_FUNC_PARAM6', slot15_e_data) #0x015E寄存器数据
        self.set_reg(15, 'MULT_FUNC.MUL_FUNC_PARAM7', slot15_b_data) #0x015B寄存器数据
        return 0

    def __config_fpga_update(self,ddr_addr:int = 0,flash_addr:int = 0, length: int = 0, direct: int = 0,slot: Union[int, None] = None) -> int:
        """
        FPGA remote update

        Args:
            ddr_addr (int, optional): DDR address. Defaults to 0.
            flash_addr (int, optional): Flash address. Defaults to 0.
            length (int, optional): Data length. Defaults to 0.
            direct (int, optional): Data direct. Defaults to 0.
            slot (int, optional): The slot number of the DAQ board. Value in list `[4, 15]`. Defaults to `None`.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal
       """
        slot = self.slot_check(slot)
        self.set_reg(slot, 'MULT_FUNC.MUL_FUNC_PARAM1', 10)
        self.set_reg(slot, 'MULT_FUNC.MUL_FUNC_PARAM2', ddr_addr) # DDR地址
        self.set_reg(slot, 'MULT_FUNC.MUL_FUNC_PARAM3', flash_addr) #FLASH地址
        self.set_reg(slot, 'MULT_FUNC.MUL_FUNC_PARAM4', length) #数据长度
        self.set_reg(slot, 'MULT_FUNC.MUL_FUNC_PARAM5', direct) #数据方向 0:ddr -> flash, 1: flash -> ddr
        return 0

    def __config_hardware_info(self, batch_num ,slot: Union[int, None] = None) -> int:
        """
        Modification of board hardware information

        Args:
            batch_num (int): Hardware batch
            slot (int, optional): The slot number of the DAQ board. Value in list `[4, 15]`. Defaults to `None`.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal
        """
        slot = self.slot_check(slot)
        self.set_reg(slot, 'MULT_FUNC.MUL_FUNC_PARAM1', 0)
        self.set_reg(slot, f'MULT_FUNC.MUL_FUNC_PARAM5', batch_num) # 硬件批次
        return 0