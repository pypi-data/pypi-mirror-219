# coding: utf-8
from ..logger import get_logger


import sys
import numpy as np
from ..utils import get_bit
from ..constant import const
from struct import pack, unpack
from ..error.comm_error import (
    IllegalMemoryAddressError,
    TooManyRegisterEnriesError,
    IllegalMemoryFrameLengthError
)

class CMUProtocol:
    """Implementation of CMU Protocol, see /docs/sqc_protocol.md for reference.

    Attributes:
        VERSION (str): SQC protocol version.
        MEM_FRAME_HEADER_LEN (int): Length of memory frame header, fixed to 8.
    """

    # VERSION = '1.0'
    # MEM_FRAME_HEADER_LEN = 8
    # MEM_FRAME_DATA_LEN = 1024
    # MEM_FRAME_LEN = 1032
    # MAX_REG_NUM = 183
    # MAX_MEM_SEND_FRAMES = 1024 # 1M通信速率
    # MAX_MEM_SEND_FRAMES = 32 # 32K通信速率

    if 'win' in sys.platform:
        MAX_MEM_READ_SIZE = 1 << 19  # bytes
    else:
        MAX_MEM_READ_SIZE = 1 << 18

    logger = None

    def __init__(self, logger=None, console_log=True):
        if CMUProtocol.logger is None:
            if logger:
                CMUProtocol.logger = logger
            else:
                CMUProtocol.logger = get_logger(
                                    'ezq_device_log', 'cmu_protocol',
                                    console=console_log
                                    )

    def write_mem_frame(self, address, data, frame_num=0, mark_last=True, slot=0):
        segment = const.MEM_FRAME_DATA_LEN
        # segment = CMUProtocol.MEM_FRAME_DATA_LEN
        if address % segment != 0:
            self.logger.error(f'Illegal memory address: {address}')
            raise IllegalMemoryAddressError(address, segment)
        address_32bit = address & 0xFFFFFFFF
        rsv = 0b000000
        last_tag = 0x80 if mark_last else 0
        address_ext = last_tag | (rsv << 2) | (address >> 32)
        frame_num = frame_num << 8
        rw_tag = (0xC0 | slot) << 24
        head_list = [address_32bit, rw_tag | frame_num | address_ext]
        frame = pack('2I', *head_list) + data
        return frame

    def write_mem_frames_spd_ctrl(self, address, data, slot):
        segment = const.MEM_FRAME_DATA_LEN
        # segment = CMUProtocol.MEM_FRAME_DATA_LEN
        length_list = []
        # 最小1024个字节作为处理单位
        data_bytes = b''
        for dt in data:
            dt_bytes = dt
            dt_length = len(dt_bytes)
            pad_cnt = (1024 - (dt_length & 0x3FF)) & 0x3FF
            if pad_cnt:
                p_data = [0] * pad_cnt
                pad_data = pack(f'{pad_cnt}B', *p_data)
                dt_bytes += pad_data
            length_list.append(len(dt_bytes))
            data_bytes += dt_bytes
        frame_num = 0
        offset = 0
        count = 0
        is_last = False
        total_num = sum(length_list)
        len_cnt = 0
        addr = address[0]
        slt = slot[0]
        while offset < total_num:
            # if offset + segment == total_num or frame_num == CMUProtocol.MAX_MEM_SEND_FRAMES - 1:
            if offset + segment == total_num or frame_num == const.MAX_MEM_SEND_FRAMES - 1:
                is_last = True
            raw_data = data_bytes[offset:offset+segment]
            frame = self.write_mem_frame(addr, raw_data, frame_num=frame_num, mark_last=is_last, slot=slt)
            yield frame, is_last
            frame_num += 1
            if is_last:
                frame_num = 0
                is_last = False
            offset += segment
            if offset == total_num:
                break
            len_cnt += segment
            addr += segment
            if len_cnt == length_list[count]:
                count += 1
                addr = address[count]
                slt = slot[count]
                len_cnt = 0
        return 0

    def parse_write_mem_response(self, data):
        tag = data[4:8]
        if tag[::-1] != b'USTC':
            miss_frame_num, = unpack('<I', tag)
        else:
            miss_frame_num = None
        count, = unpack('<I', data[:3]+b'\x00')[:3]
        slot, = unpack('B', data[3:4])
        slot = slot & 0b00_111111
        return count, miss_frame_num

    def read_mem_frame_spd_ctrl(self, start_address, length, slot):
        frames = []
        counts = []
        max_read_size = CMUProtocol.MAX_MEM_READ_SIZE
        segment = const.MEM_FRAME_DATA_LEN
        # segment = CMUProtocol.MEM_FRAME_DATA_LEN
        if start_address % segment != 0:
            self.logger.error(f'Illegal memory address: {start_address}')
            raise IllegalMemoryAddressError(start_address, segment)

        if length % segment != 0:
            length = (length // segment + 1) * segment

        frames_num = int((length + max_read_size - 1) / max_read_size)
        for _ in range(frames_num-1):
            frame, count = self.read_mem_frame(start_address, max_read_size, slot)
            frames.append(frame)
            counts.append(count)
            start_address += max_read_size
        rest_len = length - (frames_num - 1) * max_read_size
        frame, count = self.read_mem_frame(start_address, rest_len, slot)
        frames.append(frame)
        counts.append(count)
        return frames, counts

    def read_mem_frame(self, start_address, length, slot):
        segment = const.MEM_FRAME_DATA_LEN
        # segment = CMUProtocol.MEM_FRAME_DATA_LEN
        rsv = 0b000000
        addr_bytes = pack('<I', start_address & 0xFFFFFFFF)
        addr_ext = start_address >> 32
        addr_ext_bytes = pack('<B', rsv << 2 | addr_ext)
        count = length // segment
        frame_cnt_bytes = pack('<H', count)

        # bit[0-5]: slot
        # bit[6]: read = 0
        # bit[7]: mem = 1
        tag = 0b10 << 6 | slot
        tag_byte = pack('B', tag)
        frame = addr_bytes + addr_ext_bytes + frame_cnt_bytes + tag_byte
        return frame, count * (segment + 8)

    def parse_read_mem_response(self, data):
        total = len(data)
        segment = const.MEM_FRAME_LEN
        # segment = CMUProtocol.MEM_FRAME_LEN
        if total % segment != 0:
            self.logger.error(f'Illegal data length: {total}')
            raise IllegalMemoryFrameLengthError(total, segment)
        offset = 0
        header = const.MEM_FRAME_HEADER_LEN
        # header = CMUProtocol.MEM_FRAME_HEADER_LEN
        segments = []
        while offset < total:
            frame = data[offset:(offset + segment)]
            index, = unpack('<I', frame[:4])[:3]
            slot = unpack('B', frame[3:4])
            readback_data = frame[header:]
            data_array = np.frombuffer(readback_data, dtype='B')
            segments.append(data_array)
            offset += segment
        return np.concatenate(segments)

    def reg_frame(self, register_entries):
        count = len(register_entries)
        if count > const.MAX_REG_NUM:
        # if count > CMUProtocol.MAX_REG_NUM:
            self.logger.error(f'Too many register entries: {count}')
            raise TooManyRegisterEnriesError(count, const.MAX_REG_NUM)
            # raise TooManyRegisterEnriesError(count, CMUProtocol.MAX_REG_NUM)

        reg_data = []
        for entry in register_entries:
            if len(entry) == 4:
                # write reg
                slot, base_addr, addr, data = entry
                op_mask = 0b01_000000  # write
            else:
                # read reg
                slot, base_addr, addr = entry
                data = 0xFFFFFFFF
                op_mask = 0b00_000000  # read

            address = base_addr + addr
            addr_bytes = pack('<I', address)[:3]

            tag = op_mask | slot
            tag_byte = pack('B', tag)
            if isinstance(data, int):
                data = data & 0xFFFFFFFF
                data_byte = pack('<I', data)
            elif isinstance(data, float):
                data_byte = pack('<f', data)
            else:
                data_byte = data
            reg = data_byte + addr_bytes + tag_byte
            reg_data.append(reg)
        frame = b''.join(reg_data)
        return frame, len(frame)

    def parse_reg_response(self, data):
        register_bytes = data
        segment = 8
        offset = 0
        total = len(register_bytes)
        registers = []
        while offset < total:
            entry = register_bytes[offset:(offset + segment)]
            if len(entry) == segment:
                tag = entry[7]
                reg_data = entry[:4]
                slot, = unpack('B', entry[7:])
                slot = slot & 0b00_111111
                op_bit = get_bit(tag, 6)
                op = 'write' if op_bit else 'read'
                address, = unpack('<I', entry[4:7]+b'\x00')
                addr = address & 65535
                base_addr = address - addr
                item = dict(
                    slot=slot, base_addr=hex(base_addr),
                    addr=hex(addr), data=reg_data, op=op)
                registers.append(item)
            offset += segment
        return registers
