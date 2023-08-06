# coding: utf-8
# ezq_driver/units/cmu_unit.py

__all__ = ['set_reg',
           'get_reg',
           'get_slot_type',
           'clear_buffer',
           'write_mem',
           'read_mem',
           'packet',
           'commit_mem',
           'commit_reg']

import socket
import random
import numpy as np

from ..register import _REG_MAP
from ..constant import const
from ..protocol.cmu_protocol import CMUProtocol
from ..utils import format_hex_data,bytes_to_int
from ..logger import get_logger
from typing import Tuple, Union
from ..error.comm_error import (
    WriteMemRetransmissionTimeout,
    ReadMemRetransmissionTimeout,
    RecvTimeoutError,
    RegRetransmissionTimeout,
    ReadRegisterPermissionError,
    WriteRegisterPermissionError,
    SendNotMatchRecvError,
    RegisterWriteAndReadDataError,
    DDRWriteAndReadDataError
)


class CmuUnit:
    """
    该单元是ez-Q2.0产品通信管理子模块, 允许用户直接控制通信模块的各项功能.

    Examples:
        >>> from ezq_driver.driver import EzqDevice
        >>> cmu = EzqDevice(ip = '10.0.9.11', slot = 23, console_log = True, batch_mode = False)
        >>> cmu.connect()
        >>> cmu.set_reg(slot = 23, reg = 0x30000, value = 0x28)
        0

    该模块包含以下函数:

    - `set_reg(slot, reg, value)` - Writes the specified value to the specified register address in the specified slot
    - `get_reg(slot, reg, func)` - Reads the specified value to the specified register address in the specified slot
    - `get_slot_type(slot)` - Gets which module the specified slot number belongs to
    - `clear_buffer()` - Clear buffer that may be cached in the socket.
    - `write_mem(address, data, slot, wait_response) ` - Write *data* to device unit memory.
    - `read_mem(address, length, slot, wait_response)` - Read *data* from device unit memory.
    - `packet(pkt_type)` - Return packet class.
    - `commit_mem()` - Commit write data to ddr operation to deivce unit.
    - `commit_reg()` - Commit register parameters settings to device unit.
    """
    
    logger = None
    def __init__(
        self, ip, port=10000, slot=23, name='', logger=None,
        console_log=False, dev_mode=False, batch_mode=True
    ):
        """
        Initialize an cmu unit instance.

        Args:
            ip (str): Ip address of cmu.
            port (int): Port number of cmu. Defaults to 10000.
            slot (int): Slot of cmu. Defaults to 23.
            name (str): Name of unit. Defaults to ''.
            logger (None) : object of logger.
            console_log (bool): Whether to print log in console. Defaults to False.
            dev_mode (bool): Whether set develop mode,Default to False
            batch_mode (bool): Whether data are sent in batch mode. Defaults to True.
        """
        # init cmu basic information
        self.ip = ip
        self.port = port
        self.name = name if name else f'Slot:{slot}'
        if CmuUnit.logger is None:
            if logger:
                CmuUnit.logger = logger
            else:
                CmuUnit.logger = get_logger('ezq_device_log', 'driver',
                                            console=console_log)
        # init cmu udp communication setting
        self.sock = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.sock.setblocking(1)  # set socket to non-blocking mode
        # small buffer may cause error 10035 in non-blocking mode
        # if data size exceeds buffer size
        self.buffer_size = 1024 * 1024
        self.sock.setsockopt(
            socket.SOL_SOCKET, socket.SO_SNDBUF, self.buffer_size)
        self.recv_buffer_size = 1024 * 1024 * 2
        self.sock.setsockopt(
            socket.SOL_SOCKET, socket.SO_RCVBUF, self.recv_buffer_size)
        self.sock.settimeout(const.RESPONSE_TIMEOUT)
        # self.clear_buffer()

        self.protocol = CMUProtocol(self.logger, console_log=console_log)
        self.reg_map = _REG_MAP
        self.set_memory_mapper()
        self.set_reg_packet()
        self.set_write_mem_packet()
        self.set_read_mem_packet()
        # # 系统上电后默认CMU槽位上电因此在CMU初始化的时候进行寄存器&内存自检
        # self.fix_reg_rw_selfcheck(fix_reg_list=['CPU.TESTREG', 'UDP.TESTREG', 'FUNC.TESTREG'], slot=slot)
        # self.ddr_selfcheck(test_type_dict={0:'常规'}, data_type_dict = {0:'全0', 1:'全1'}, addr_list=[0x00000000], slot=slot)
        self.slot = slot
        self.dev_mode = dev_mode
        self.batch_mode = batch_mode
        self.connect_status = 0
        self.logger.info(f'Init {self.name}')

    def __fix_reg_rw_selfcheck(self,fix_reg_list:list = ['CPU.TESTREG', 'UDP.TESTREG', 'FUNC.TESTREG'], slot: Union[int, None] = None) -> int:
        """
        Fixed Register Read/Write Test

        Args:
            fix_reg_list (list, optional): fixed registers list. Defaults to ['CPU.TESTREG', 'UDP.TESTREG', 'FUNC.TESTREG'].
            slot (int, optional): The slot number of the AWG board. Value in list `[23]`. Defaults to `None`.

        Raises:
            Exception: No reg data return, test failed.
            Exception: Wrong data returned, test failed.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal
        """
        data_list = [random.randint(0, 10000) for i in range(len(fix_reg_list))]
        r_data = []
        # 读写数据在通信阶段就异常
        try:
            for index, reg in enumerate(fix_reg_list):
                # self.set_reg(slot=slot, reg=reg, value = data_list[index])
                self[slot,reg] = data_list[index]
                # r_data.append(self.get_reg(slot=slot,reg= reg,func=bytes_to_int))
                r_data.append(bytes_to_int(self[slot,reg]))
        except:
            self.logger.error(f'Slot:{slot}, self-check failed, write and read communication abnormally!')
            raise Exception(f'Slot:{slot}, self-check failed, write and read communication abnormally!')

        # 返回数据长度与实际长度不匹配
        if len(r_data) != len(fix_reg_list): 	
            self.logger.error(f'Slot:{slot}, self-check failed, No reg data return!')
            raise RegisterWriteAndReadDataError(slot)
        
        # 返回的数据与输入数据不匹配
        if data_list != r_data:
            self.logger.error(f'Slot:{slot}, self-check failed, Wrong data return!')
            raise RegisterWriteAndReadDataError(slot)
        
        return 0
    
    def __ddr_selfcheck(self,test_type_dict: dict = {0:'常规', 1:'边界-1kB', 2:'边界-64MB', 3:'压力'}, data_type_dict: dict = {0:'全0', 1:'全1', 2:'累加数', 3:'随机数'}, length_dict: dict = {0:1<<20, 1:1<<10, 2: 1<<26, 3:1<<20}, addr_list:list = [0], slot: Union[int, None] = None) -> int:
        """
        DDR self-check

        Args:
            test_type_dict (dict, optional): self-check test type dict. Defaults to {0:'常规', 1:'边界-1kB', 2:'边界-64MB', 3:'压力'}.
            data_type_dict (dict, optional): self-check data type dict. Defaults to {0:'全0', 1:'全1', 2:'累加数', 3:'随机数'}.
            length_dict (dict, optional): self-check length dict. Defaults to {0:1<<20, 1:1<<10, 2: 1<<26, 3:1<<20}.
            addr_list (list, optional): self-check address list. Defaults to [0].
            slot (int, optional): The slot number of the AWG board. Value in list `[23]`. Defaults to `None`.

        Raises:
            Exception: Slot self-check failed.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal
        """
        for test_index, test_type in test_type_dict.items(): 
            for data_index, data_type in data_type_dict.items():
                length = length_dict[test_index] >> 2
                if data_index == 0:
                    data = np.zeros((length,1), dtype='uint32')
                if data_index == 1:
                    data = np.zeros((length,1), dtype='uint32')+0xFFFFFFFF
                if data_index == 2:
                    data = np.linspace(0, length, length, dtype='uint32')
                if data_index == 3:
                    data = (np.random.uniform(0, 0xFFFFFFFFF, length)).astype('uint32')
                try:
                    for addr in addr_list:
                        self.write_mem(addr,data.tobytes(),slot = slot)
                        r_data = self.read_mem(addr, length<<2, slot = slot)
                except:
                    raise DDRWriteAndReadDataError(slot, test_type,data_type,length,addr)

                if r_data != data.tobytes():
                    raise DDRWriteAndReadDataError(slot, test_type,data_type,length,addr)
        return 0

    def set_reg(self, slot: int, reg: int, value: int) -> int:
        """
        Writes the specified value to the specified register address in the specified slot

        Args:
            slot (int, optional): The slot number of the CMU board. Value is `23`. Defaults to `None`.
            reg (int): The register address.
            value (int): The value written to the specified register.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal
        """
        if self.batch_mode:
            self.reg_packet[slot, reg] = value
        else:
            self[slot, reg] = value
        return 0

    def get_reg(self, slot, reg, func = None) -> Union[int, bytes]:
        """
        Reads the specified value to the specified register address in the specified slot

        Args:
            slot (int, optional): The slot number of the CMU board. Value is `23`. Defaults to `None`.
            reg (int): The register address
            func (optional): Read the result conversion function. Defaults to None.

        Returns:
            Read and convert the result
        """
        if self.batch_mode:
            self.reg_packet(slot, reg)
            num = 0
        else:
            num = self[slot, reg]
            if func:
                num = func(num)
        return num

    def slot_check(self, slot: int) -> int:
        """
        Verify the slot number

        Args:
            slot (int, optional): The slot number of the CMU board. Value is `23`. Defaults to `None`.

        Returns:
            The right slot number
        """
        if slot is None:
            return self.slot
        else:
            self.slot = slot
            return slot

    def value_validate(self, value, v_min, v_max, error_class):
        """
        Verify that the input values are correct

        Args:
            value (optional): The value to be validated
            v_min (optional): The minimum value
            v_max (optional): The maximum value
            error_class (optional): Throws the specified exception

        Raises:
            error_class: Throws the specified exception
        """
        if value < v_min or value > v_max:
            raise error_class(self.name, v_min, v_max, value)

    def get_slot_type(self, slot: int) -> str:
        """
        Gets which module the specified slot number belongs to

        Args:
            slot (int, optional): The slot number of the CMU board. Value is `23`. Defaults to `None`.

        Returns:
            Which module the specified slot belongs to
        """
        if slot in const.AWG_SLOTS:
            device_type = 'AWG'
        elif slot in const.DAQ_SLOTS:
            device_type = 'DAQ'
        elif slot in const.MIX_SLOTS:
            device_type = 'MIX'
        else:
            device_type = 'CMU'
        return device_type

    def set_memory_mapper(self):
        """
        Create a memory object for current Unit.
        """
        self._byte_mapper = MemoryMapper(self, 'byte')

    def set_reg_packet(self):
        """
        Create register packet.
        """
        self.reg_packet = self.packet('reg')

    def set_write_mem_packet(self):
        """
        Create write memory packet.
        """
        self.w_mem_packet = self.packet('mem')

    def set_read_mem_packet(self):
        """
        Create read memory packet.
        """
        self.r_mem_packet = self.packet('mem')

    def map_memory(self):
        """
        Return current unit's memory object.

        Returns:
            MemoryMapper: Current memory management object.
        """
        return self._byte_mapper

    def __str__(self):
        return f'({self.name}|{self.ip}:{self.port})'

    def send(self, data: bytes):
        """
        Send *data* to CMU.

        Args:
            data (bytes): Data to be sent to CMU.
        """
        dst = (self.ip, self.port)
        self.sock.sendto(data, dst)
        # self.display_data('Send', data)

    def recv(self, count: int) -> bytes:
        """
        Receive data from CMU.

        Args:
            count (int): The number of bytes that should be received from the CMU.

        Returns:
            Data received from the CMU.
        """
        data, addr_info = self.sock.recvfrom(count)
        # self.display_data('Recv', data)
        return data

    def clear_buffer(self) -> int:
        """
        Clear buffer that may be cached in the socket.

        Returns:
            The program ends normally with return value `0`, otherwise abnormal.
        """
        try:
            data = self.sock.recv(8192)
            self.logger.debug(f'Clear {len(data)} bytes from buffer.')
        except OSError:
            return 0

    def display_data(self, tag: str, data: bytes):
        """
        Convert data to hex data and display it in the log.

        Args:
            tag (str): Tag out where *data* belongs.
            data (byte): Data need to be converted to hex data and display in the log.
        """
        head = f'{tag} data ({len(data)} bytes)'
        segment = 32
        offset = 0
        total = len(data)
        self.logger.debug(head)
        while offset < total:
            data_seg = data[offset:(offset + segment)]
            seg_hex = format_hex_data(data_seg)
            self.logger.debug(f'[{offset:08X}] {seg_hex}')
            print(f"{head} / [{offset:08X}] / {seg_hex}")
            offset += segment

    def write_mem(self, address: Union[int, list], data: bytes, slot: Union[int, None] = None, wait_response: bool=True) ->int:
        """
        Write *data* to device unit memory.

        Args:
            address (int|list): Start address of device unit memory where data will be written, which should be multiples of 1024.
            data (bytes|bytes[]): Data to be written in device unit memory.
            slot (int|list): The slot of the crate.
            wait_response (bool, optional): Whether to wait for device unit's response. Defaults to True.

        Returns:
            Number of frames received by device unit if *wait_response* is True, otherwise number of frames sent by driver.
        """
        if isinstance(address, int):
            address = [address]
            data = [data]

        n = len(address)
        slot = self.slot_check(slot)
        if isinstance(slot, int):
            slot = [slot] * n
        total_count = self.__write_mem_iterate_send(address, data, slot, wait_response)
        return total_count

    def __write_mem_iterate_send(self, address, data, slot, wait_response):
        """
        Send write memory frame every time finish packing a frame

        Args:
            address (list): Start address of device unit memory where data will be written, which should be multiples of 1024.
            data (list): Data to be written in device unit memory. includes 'byte', 'wave' and 'seq'. Defaults to 'byte'.
            slot (list): The slot of device unit.
            wait_response (bool): Whether to wait for device unit's response. Defaults to True.

        Raises:
            RetransmissionTimeout: Retransmit miss frame fail.

        Returns:
            The number of frames had been sent.
        """
        frames_generator = self.protocol.write_mem_frames_spd_ctrl(address, data, slot)
        total_count = 0
        sent_frame = []
        while True:
            try:
                frame, last = next(frames_generator)
                total_count += 1
                self.send(frame)
                if wait_response:
                    sent_frame.append(frame)
                if last and wait_response:
                    count, miss_frame_num = self.__wait_write_mem_response()
                    if miss_frame_num is not None:
                        max_times = 5
                        retransmit_times = 0
                        while retransmit_times < max_times:
                            sent_cnt = len(sent_frame)
                            if sent_cnt - count == 1:
                                miss_frame = sent_frame[miss_frame_num]
                                # set last tag
                                last_tag = b'\x01\xC0'
                                # set frame number equals to 0
                                frame_number = b'\x00\x00'
                                miss_frame = miss_frame[:4] + frame_number + last_tag + miss_frame[8:]
                                self.logger.warn(f'{self.name} received {count} frames of {sent_cnt}, miss NO.{miss_frame_num}. ')
                                self.logger.warn(f'{self.name} retransmit NO.{miss_frame_num} frame. ')
                                self.send(miss_frame)
                                count, miss_frame_num = self.__wait_write_mem_response()
                            else:
                                self.logger.warn(f'{self.name} retransmit all frames. ')
                                for frame in sent_frame:
                                    self.send(frame)
                                count, miss_frame_num = self.__wait_write_mem_response()
                            retransmit_times += 1
                            if miss_frame_num is None:
                                sent_frame = []
                                break
                            if retransmit_times == max_times:
                                raise WriteMemRetransmissionTimeout(self.slot, retransmit_times)
                    else:
                        sent_frame = []
            except StopIteration:
                break
        return total_count

    def __wait_write_mem_response(self) -> Tuple[int,int]:
        """
        Wait response for writing memory.

        Returns:
            Numberr of frames received by CMU, number of miss frame.
        """
        try:
            response = self.wait_response(response_size=8, pattern='Write_Mem')
            count, miss_frame_num = self.protocol.parse_write_mem_response(response)
        except RecvTimeoutError:
            count = 0
            miss_frame_num = 0
        return count, miss_frame_num

    def __read_mem_old(self, address: Union[int, list], length: int, slot: Union[int, None] = None, wait_response: bool = True) -> Union[int, list]:
        """
        Read *data* from device unit memory.

        Args:
            address (int|list[int]): Start address of device unit memory where data will be read from, which should be multiples of 1024.
            length (int|list[int]): The length of the data to be read, which should be multiples of 1024.
            slot (list): The slot of device unit.
            wait_response (bool, optional): Whether to wait for CMU's response. Defaults to True.

        Returns:
            Data list read from device unit memory if *wait_response* is True, otherwise number of frames sent by driver.
        """
        
        if isinstance(address, int):
            address = [address]
            length = [length]

        n = len(address)

        slot = self.slot_check(slot)
        if isinstance(slot, int):
            slot = [slot] * n

        frames_list = []
        response_sizes_list = []
        for i, addr in enumerate(address):
            frames, resp_sizes = self.protocol.read_mem_frame_spd_ctrl(addr, length[i], slot[i])
            frames_list.append(frames)
            response_sizes_list.append(resp_sizes)
        if wait_response:
            data = []
            for frames, response_sizes in zip(frames_list, response_sizes_list):
                total_size = sum(response_sizes)
                response = bytearray(total_size)
                recv_size = 0
                for idx, frame in enumerate(frames):
                    self.send(frame)
                    resp = self.wait_response(response_size = response_sizes[idx], pattern='Read_Mem')
                    resp_size = response_sizes[idx]
                    response[recv_size:recv_size+resp_size] = resp
                    recv_size += resp_size
                mem_data = self.protocol.parse_read_mem_response(response)
                mem_data = mem_data.tobytes()
                data.append(mem_data)
            # return 0
            return data if len(data) > 1 else data[0]
        else:
            response_size = []
            for frames, response_sizes in zip(frames_list, response_sizes_list):
                rsize = []
                for idx, frame in enumerate(frames):
                    self.send(frame)
                    rsize.append(response_sizes[idx])
                response_size.append(sum(rsize))
            return response_size

    def __wait_read_mem_response(self, response_size, retransmit_times=0) -> Tuple[bytearray, bool]:
        """
        Wait response for reading memory.

        Args:
            response_size (int): response size.

        Returns:
            Received data and whether it is received normally.
        """
        try:
            response = self.wait_response(response_size=response_size,pattern='Read_Mem', retransmit_time=retransmit_times)
            flag = False
        except RecvTimeoutError:
            response = bytearray()
            flag = True
        return response,flag

    def read_mem(self, address: Union[int, list], length: int, slot: Union[int, None] = None, wait_response: bool = True) -> Union[int, list]:
        """
        Read *data* from device unit memory.

        Args:
            address (int|list[int]): Start address of device unit memory where data will be read from, which should be multiples of 1024.
            length (int|list[int]): The length of the data to be read, which should be multiples of 1024.
            slot (list): The slot of device unit.
            wait_response (bool, optional): Whether to wait for CMU's response. Defaults to True.

        Returns:
            Data list read from device unit memory if *wait_response* is True, otherwise number of frames sent by driver.
        """
        
        if isinstance(address, int):
            address = [address]
            length = [length]

        n = len(address)

        slot = self.slot_check(slot)
        if isinstance(slot, int):
            slot = [slot] * n

        frames_list = []
        response_sizes_list = []
        for i, addr in enumerate(address):
            frames, resp_sizes = self.protocol.read_mem_frame_spd_ctrl(addr, length[i], slot[i])
            frames_list.append(frames)
            response_sizes_list.append(resp_sizes)
        if wait_response:
            data = []
            for frames, response_sizes in zip(frames_list, response_sizes_list):
                total_size = sum(response_sizes)
                response = bytearray(total_size)
                recv_size = 0
                for idx, frame in enumerate(frames):
                    self.send(frame)
                    resp, flag = self.__wait_read_mem_response(response_sizes[idx], 0)
                    if flag:
                        max_times = 5
                        retransmit_times = 0
                        while retransmit_times < max_times:
                            self.send(frame)
                            resp, flag = self.__wait_read_mem_response(response_sizes[idx], retransmit_times + 1)
                            retransmit_times += 1
                            if not flag:
                                break
                            if retransmit_times == max_times:
                                raise ReadMemRetransmissionTimeout(self.slot, retransmit_times)
                    resp_size = response_sizes[idx]
                    response[recv_size:recv_size+resp_size] = resp
                    recv_size += resp_size
                mem_data = self.protocol.parse_read_mem_response(response)
                mem_data = mem_data.tobytes()
                data.append(mem_data)
            # return 0
            return data if len(data) > 1 else data[0]
        else:
            response_size = []
            for frames, response_sizes in zip(frames_list, response_sizes_list):
                rsize = []
                for idx, frame in enumerate(frames):
                    self.send(frame)
                    rsize.append(response_sizes[idx])
                response_size.append(sum(rsize))
            return response_size

    def send_reg_cmd(self, register_entries, wait_response=True):
        """Send register command to device unit.

        Args:
            register_entries (list[(slot,baseaddr,register,data)]): List of register command entry. Register command entry is composed of slot(int), base address id(int) and register address(int), if it is a write register command, add the data(int) written to device unit register to the tuple.
            wait_response (bool, optional): Whether to wait for device unit's response. Defaults to True.

        Returns:
            list|int: List of register command result received by CMU if *wait_response* is True,otherwise number of frames sent by driver.
        """
        frame, response_size = self.protocol.reg_frame(register_entries)
        max_times = 5
        try_times = 0
        while try_times < max_times:
            try:
                self.send(frame)
                if wait_response:
                    response = self.wait_response(response_size=response_size,pattern='Send_Reg')
                    registers = self.protocol.parse_reg_response(response)
                    return registers
                else:
                    return response_size
            except RecvTimeoutError:
                try_times += 1
            if try_times == max_times:
                raise RegRetransmissionTimeout(self.name, try_times)

    def wait_response(self, response_size, timeout=None, interval=None, pattern = 'unknown', retransmit_time = 0):
        """Wait response from CMU.

        Args:
            response_size (int): Size of response received from CMU.
            timeout (float, optional): Maximum time for waiting CMU's response. Defaults to None.
            interval (float, optional): Interval time for waiting CMU's response. Defaults to None.

        Raises:
            RecvTimeoutError: Error of not receiving enough *response_size* data within the *timeout* time.

        Returns:
            byte: Data received from CMU.
        """
        if timeout is None:
            timeout = const.RESPONSE_TIMEOUT
        if interval is None:
            interval = 1e-3
        self.sock.settimeout(timeout)
        offset = 0
        response = bytearray(response_size)
        recved_size = 0
        while offset < response_size:
            try:
                resp = self.recv(response_size)
                resp_len = len(resp)
                response[recved_size:recved_size+resp_len] = resp
                recved_size += resp_len
            except socket.error:
                break
            if recved_size == response_size:
                break
        if self.connect_status and recved_size == 0:
            self.re_connect()
            self.logger.error(
                f'Pattern ({pattern}) and Retransmit Times({retransmit_time}) Recv timeout ({timeout:g} s) for {self.name}, '
                f'expecting {response_size} bytes, '
                f'{recved_size} bytes received')
            raise RecvTimeoutError(self, recved_size, response_size, timeout)
        else:
            if recved_size != response_size:
                self.logger.error(
                    f'Pattern ({pattern}) and Retransmit Times({retransmit_time}) Recv timeout ({timeout:g} s) for {self.name}, '
                    f'expecting {response_size} bytes, '
                    f'{recved_size} bytes received')
                raise RecvTimeoutError(self, recved_size, response_size, timeout)
        return response

    def close(self):
        """
        Close socket connection.
        """
        self.sock.close()

    def __getitem__(self, key):
        slot = self.slot
        device_type = self.get_slot_type(slot)
        if isinstance(key, int):
            base_addr = 0
            addr = key
        elif isinstance(key, tuple):
            if len(key) == 3:
                slot, base_addr, addr = key
                device_type = self.get_slot_type(slot)
            else:
                prev, last = key
                if isinstance(last, str):
                    slot = prev
                    device_type = self.get_slot_type(slot)
                    base_addr, addr = self.reg_map.get_addr_by_name(device_type, last)
                else:
                    base_addr, addr = prev, last
        elif isinstance(key, str):
            base_addr, addr = self.reg_map.get_addr_by_name(device_type, key)
        else:
            raise KeyError(f'index should be int, tuple or str, got {key}')
        if not self.dev_mode and not self.reg_map.readable(device_type, base_addr, addr):
            name = self.reg_map.get_name_by_addr(device_type, base_addr, addr)
            raise ReadRegisterPermissionError(name)
        entry = (slot, base_addr, addr)
        reg_info = self.send_reg_cmd([entry])
        # TODO: check read back infomation
        return reg_info[0]['data']

    def __setitem__(self, key, value):
        slot = self.slot
        device_type = self.get_slot_type(slot)
        if isinstance(key, int):
            base_addr = 0
            addr = key
        elif isinstance(key, tuple):
            if len(key) == 3:
                slot, base_addr, addr = key
                device_type = self.get_slot_type(slot)
            else:
                prev, last = key
                if isinstance(last, str):
                    slot = prev
                    device_type = self.get_slot_type(slot)
                    base_addr, addr = self.reg_map.get_addr_by_name(device_type, last)
                else:
                    base_addr, addr = prev, last
        elif isinstance(key, str):
            base_addr, addr = self.reg_map.get_addr_by_name(device_type, key)
        if not self.dev_mode and not self.reg_map.writable(device_type, base_addr, addr):
            name = self.reg_map.get_name_by_addr(device_type, base_addr, addr)
            raise WriteRegisterPermissionError(name)
        entry = (slot, base_addr, addr, value)
        reg_info = self.send_reg_cmd([entry])
        return reg_info

    def packet(self, pkt_type='reg'):
        """
        Return packet class.

        Args:
            pkt_type (str, optional): Packet type. Defaults to 'reg'.

        Returns:
            RegisterPacket|MemoryPacket: Packet class.
        """
        pkt_map = dict(reg=RegisterPacket, mem=MemoryPacket)
        PacketClass = pkt_map[pkt_type]
        return PacketClass(self)

    def commit_mem(self) -> dict:
        """
        Commit write data to ddr operation to deivce unit.

        Returns:
            dict: Write memory data to data result.
        """
        result = self.w_mem_packet.send()
        self.w_mem_packet.clear()
        return result

    def commit_reg(self) -> dict:
        """
        Commit register parameters settings to device unit.

        Returns:
            dict: register setting result
        """
        result = self.reg_packet.send()
        self.reg_packet.clear()
        return result

class UnitPacket:
    def __init__(self, unit, pkt_type):
        self.unit = unit
        self.result = None
        self.response = None
        self.pkt_type = pkt_type

    def update_result(self, data):
        result = self.parse_response(data)
        self.result = result
        self.check_result()

    def get_result(self):
        return self.result

    @property
    def sock(self):
        return self.unit.sock

    @property
    def unit_name(self):
        return self.unit.name

    @property
    def protocol(self):
        return self.unit.protocol

    def send(self):
        raise NotImplementedError('send is not implemented')

    def parse_response(self, data):
        raise NotImplementedError('parse_response is not implemented')

    def check_result(self):
        # raise NotImplementedError('check_result is not implemented')
        pass

class RegisterPacket(UnitPacket):
    """
    Class for batch register operations.
    """

    def __init__(self, unit):
        self.queue = []
        UnitPacket.__init__(self, unit, 'reg')

    def get_addr(self, name):
        return self.unit.reg_map.get_addr_by_name(name)

    def __setitem__(self, key, value):
        slot = self.unit.slot
        device_type = self.unit.get_slot_type(slot)
        if isinstance(key, tuple):
            if len(key) == 3:
                slot, base_addr, addr = key
                device_type = self.unit.get_slot_type(slot)
            else:
                prev, last = key
                if isinstance(last, str):
                    slot = prev
                    device_type = self.unit.get_slot_type(slot)
                    base_addr, addr = self.unit.reg_map.get_addr_by_name(device_type, last)
                else:
                    base_addr, addr = prev, last
        elif isinstance(key, str):
            base_addr, addr = self.get_addr(key)
        if not self.unit.dev_mode and not self.unit.reg_map.writable(device_type, base_addr, addr):
            name = self.unit.reg_map.get_name_by_addr(device_type, base_addr, addr)
            raise WriteRegisterPermissionError(name)
        entry = (slot, base_addr, addr, value)
        self.queue.append(entry)

    def __call__(self, *key):
        slot = self.unit.slot
        device_type = self.unit.get_slot_type(slot)
        if len(key) == 3:
            slot, base_addr, addr = key
            device_type = self.unit.get_slot_type(slot)
        elif len(key) == 2:
            prev, last = key
            if isinstance(last, str):
                slot = prev
                device_type = self.unit.get_slot_type(slot)
                base_addr, addr = self.unit.reg_map.get_addr_by_name(device_type, last)
            else:
                base_addr, addr = prev, last
        elif len(key) == 1:
            base_addr, addr = self.get_addr(key[0])
        if not self.unit.dev_mode and not self.unit.reg_map.readable(device_type, base_addr, addr):
            name = self.unit.reg_map.get_name_by_addr(device_type, base_addr, addr)
            raise ReadRegisterPermissionError(name)
        entry = (slot, base_addr, addr)
        self.queue.append(entry)

    def send(self, wait_response=True):
        ret = 0
        registers = self.queue
        if registers:
            ret = self.unit.send_reg_cmd(registers, wait_response=wait_response)
            return ret
        return ret

    def parse_response(self, data):
        self.response = data
        return self.unit.protocol.parse_reg_response(data)

    def check_result(self):
        # TODO: check write register result if there are write operations in self.queue
        pass

    def clear(self):
        self.queue = []

class MemoryPacket(UnitPacket):
    def __init__(self, unit):
        self.address = []
        self.data = []
        self.length = []
        self.slot = []
        self.operation = None
        UnitPacket.__init__(self, unit, 'mem')

    def write_mem(self, address, data, slot=None):
        self.address.append(address)
        self.data.append(data)
        slot = self.unit.slot_check(slot)
        self.slot.append(slot)
        self.operation = 'write'

    def read_mem(self, address, length, slot=None):
        self.address.append(address)
        self.length.append(length)
        slot = self.unit.slot_check(slot)
        self.slot.append(slot)
        self.operation = 'read'

    def send(self, wait_response=True):
        if self.operation == 'write':
            if not self.data:
                return 0
            self.sent_frame_cnt = self.unit.write_mem(
                self.address, self.data, self.slot, wait_response=wait_response)
            if wait_response:
                self.result = self.sent_frame_cnt
                ret = self.sent_frame_cnt
            else:
                # cnt = int(np.ceil(self.sent_frame_cnt / self.protocol.MAX_MEM_SEND_FRAMES))
                cnt = int(np.ceil(self.sent_frame_cnt / const.MAX_MEM_SEND_FRAMES))
                ret = 8 * cnt  # response size in bytes
        elif self.operation == 'read':
            ret = self.unit.read_mem(
                self.address, self.length, self.slot, wait_response=wait_response)
            self.read_mem_ret = ret
        else:
            ret = 0
        return ret

    def parse_response(self, data):
        ret = 0
        # self.unit.display_data(f'{self.unit.name} Recv Response', data)
        self.response = data
        if self.operation == 'write':
            offset = 0
            segment = 8
            while offset < len(self.response):
                cnt, _ = self.protocol.parse_write_mem_response(self.response[offset:offset+segment])
                ret += cnt
                offset += segment
        else:
            response_sizes = self.read_mem_ret
            offset = 0
            ret = []
            for rsize in response_sizes:
                segment = data[offset:(offset + rsize)]
                mem_data = self.protocol.parse_read_mem_response(segment)
                ret.append(mem_data)
                offset += rsize
            if len(ret) == 1:
                ret = ret[0]
        return ret

    def check_result(self):
        if self.operation == 'write':
            recv_cnt_by_unit = self.result
            if recv_cnt_by_unit != self.sent_frame_cnt:
                raise SendNotMatchRecvError(
                    self.unit_name, self.sent_frame_cnt, recv_cnt_by_unit)
        else:
            # TODO: check read back data length
            pass

    def clear(self):
        self.address = []
        self.data = []
        self.length = []
        self.slot = []
        self.operation = None

class MemoryMapper:
    """Class for mapping memory like a Python list.
    """

    def __init__(self, unit, memory_type):
        self.unit = unit
        self.memory_type = memory_type

    def get_range(self, key):
        if isinstance(key, slice):
            start = key.start
            stop = key.stop
            if start is None:
                start = 0
            if stop is None:
                stop = start + 1
        elif isinstance(key, int):
            start = key
            stop = start + 1
        return start, stop

    def index_to_memory_addr(self, start, stop):
        start_KB = start // 1024 * 1024
        end_KB = (stop - 1) // 1024 * 1024
        length = end_KB - start_KB + 1024
        return start_KB, length

    def __getitem__(self, key):
        start, stop = self.get_range(key)
        start_address, length = self.index_to_memory_addr(start, stop)
        data = self.unit.read_mem(start_address, length)
        values = data[(start - start_address):(stop - start_address)]
        if len(values) == 1:
            values = values[0]
        return values

    def __setitem__(self, key, value):
        start, stop = self.get_range(key)
        start_address, length = self.index_to_memory_addr(start, stop)
        data = self.unit.read_mem(start_address, length)
        data_array = bytearray(data)
        data_array[(start - start_address):(stop - start_address)] = value
        data_bytes = bytes(data_array)
        self.unit.write_mem(start_address, data_bytes)
