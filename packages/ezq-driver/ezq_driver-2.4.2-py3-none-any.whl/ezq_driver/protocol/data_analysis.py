'''
Author: wly wangleungy@ustc.edu.cn
Date: 2022-09-13 16:25:09
LastEditors: wly wangleungy@ustc.edu.cn
LastEditTime: 2023-02-17 18:03:56
Description: data analysis process
'''
import numpy as np
from struct import unpack
import struct

class ReadoutDataAnalysis:

    @staticmethod
    def wave_data_analysis(raw_wave_data, data_segment):
        # total = len(raw_wave_data)
        # offset = 0
        # segments = []
        # while offset < total:
        #     raw_data = raw_wave_data[offset:offset+data_segment]
        #     wave_desc = raw_data[:16]
        #     sample_depth, = unpack('<I', wave_desc[:4])
        #     sample_pos, = unpack('<H', wave_desc[4:6])
        #     ts_vector, = unpack('<I', wave_desc[6:10])
        #     glb_timer_low_32, = unpack('<I', wave_desc[10:14])
        #     glb_timer_high_16, = unpack('<H', wave_desc[14:16])
        #     glb_timer = glb_timer_low_32 | (glb_timer_high_16 << 32)
        #     wave_bytes = raw_data[16:]
        #     wave_data = np.frombuffer(wave_bytes, dtype='B')
        #     segments.append(wave_data)
        #     offset += data_segment
        # wave_info = dict(
        #     # sample_depth=sample_depth,
        #     # sample_pos=sample_pos,
        #     # ts_vector=ts_vector,
        #     # glb_timer=glb_timer
        # )
        # return wave_info, np.concatenate(segments)
        repeats = int(len(raw_wave_data) / data_segment)
        wave_data = None
        sample_depth = []
        sample_pos = []
        ts_vector = []
        glb_timer = []
        offset = 0
        for i in range(repeats):
            wave_head = raw_wave_data[offset:offset+16]
            _s, = unpack('<I', wave_head[:4])
            _p, = unpack('<H', wave_head[4:6])
            _ts, = unpack('<I', wave_head[6:10])
            _gt_32, = unpack('<I', wave_head[10:14])
            _gt_16, = unpack('<H', wave_head[14:16])
            # _s, _p, _ts, _gt_32, _gt_16 = unpack('<IHIIH', wave_head)
            sample_depth.append(_s)
            sample_pos.append(_p)
            gt = (_gt_16 << 32) + _gt_32
            glb_timer.append(gt)
            ts_vector.append(_ts)
            if wave_data is None:
                wave_data = raw_wave_data[offset+16:offset+data_segment]
            else:
                wave_data += raw_wave_data[offset+16:offset+data_segment]
            offset += data_segment

        segments = np.frombuffer(wave_data, dtype='int8') # adc采样位数有关
        wave_info = dict(
            sample_depth=sample_depth,
            sample_pos=sample_pos,
            ts_vector=ts_vector,
            glb_timer=glb_timer
        )
        return wave_info, segments

    @staticmethod
    def demod_data_analysis(raw_demod_data, data_segment):
        total = len(raw_demod_data)
        offset = 0
        segments = []
        while offset < total:
            raw_data = raw_demod_data[offset:offset+data_segment]
            demod_desc = raw_data[:16]
            demod_winwdow_width, = unpack('<I', raw_demod_data[:4])
            demode_window_start, = unpack('<H', raw_demod_data[4:6])
            ts_vector, = unpack('<I', demod_desc[6:10])
            glb_timer_low_32, = unpack('<I', demod_desc[10:14])
            glb_timer_high_16, = unpack('<H', demod_desc[14:16])
            glb_timer = glb_timer_low_32 | (glb_timer_high_16 << 32)
            demod_data_bytes = raw_data[32:]
            demod_data = np.frombuffer(demod_data_bytes, dtype='<B')
            low_8_bit = demod_data[0::3].astype('uint32')
            mid_8_bit = demod_data[1::3].astype('uint32')
            hig_8_bit = demod_data[2::3].astype('uint32')
            _demod_data = hig_8_bit << 24 | mid_8_bit << 16 | low_8_bit << 8 
            #_demod_data = hig_8_bit << 16 | mid_8_bit << 8 | low_8_bit
            # bd = _demod_data.tobytes()
            # demod_data = np.frombuffer(bd, dtype='int32')
            demod_data = _demod_data.astype('int32') >> 8
            # print('数据类型', demod_data.dtype)
            segments.append(demod_data)
            # demod_data = _demod_data
            offset += data_segment
        demod_info = dict(
            demod_winwdow_width=demod_winwdow_width,
            demode_window_start=demode_window_start,
            ts_vector=ts_vector,
            glb_timer=glb_timer,
        )
        return demod_info, np.concatenate(segments)

    @staticmethod
    def state_data_analysis(raw_state_data,data_segment):
        offset = 0
        total = len(raw_state_data)
        states = []
        while offset < total:
            raw_state = raw_state_data[offset:offset+data_segment]
            qubits_state, = unpack('<I', raw_state)
            for i in range(16):
                qubit_state = (qubits_state >> 2 * i) & 3
                states.append(qubit_state)
            offset += data_segment
        return states
