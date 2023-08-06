# coding: utf-8
import struct
import socket
import time

def get_init_ip(port = 7000) -> str:
    """
    Get ezq init ip

    Args:
        ip (str): udp broadcast init ip. Defaults to "".
        port (int, optional): udp broadcast port. Defaults to 7000.

    Returns:
        ezq init ip
    """
    address = ('', port)
    udpServer = socket(socket.AF_INET,socket.SOCK_DGRAM)
    udpServer.bind(address)
    data, addr = udpServer.recvfrom(2048)
    udpServer.close()
    return addr[0]

def format_hex_data(data: list) -> str:
    hex_str = [f'{d:02X}' for d in data]
    return ' '.join(hex_str)

def get_bit(data, pos):
    mask = (1 << pos)
    bit = (data & mask) >> pos
    return bit

def int_to_bytes(x):
    return struct.pack('>I', x)

def bytes_to_int(b):
    x, = struct.unpack('<I', b)
    return x

def bytes_to_float(b):
    x, = struct.unpack('<f', b)
    return x

def float_to_bytes(x):
    return struct.pack('<f', x)

def int_to_ip(x):
    local_ip = int_to_bytes(x)
    ip = '.'.join([str(d) for d in local_ip])
    return ip

def ip_to_int(ip):
    ib = socket.inet_aton(ip)
    ip_int, = struct.unpack('>I', ib)
    return ip_int

def get_host_ip():
    addrs = socket.getaddrinfo(socket.gethostname(), None)
    for item in addrs:
        if item[-1][0].find('10.0') > -1:
            return item[-1][0]
    return '10.0.255.255'

def cacl_twos_complement(data, bit_width=0xFFFFFFFF):
    data = int(data)
    if data < 0:
        data = abs(data) & bit_width
        data ^= bit_width
        data = data + 1
    else:
        data &= bit_width
    return data

def restore_twos_complement(data, bit_width=16):
    """
    Convert Two's Complement Back to Integer

    Note:
    The function takes two arguments: "data" represents the two's complement to be restored, and "bit_width" represents the bit width of the data and is set to 16 by default.
    To restore the two's complement, we need to know whether the number is positive or negative. If the most significant bit is 1, it indicates that this is a negative number in two's complement form.
    In this case, we need to convert it to the corresponding negative integer. Specifically, we need to calculate 2 ^ bit_width using the operation (1 << bit_width)
    (because Python does not have an unsigned integer type, so we need to use a signed integer to represent it), and then subtract the two's complement from this value to obtain the corresponding negative integer.
    For positive numbers in two's complement form, the most significant bit is 0, so we can directly use it as an unsigned integer. It should be noted that Python's integer type itself supports representations of arbitrary length,
    so we don't need to consider overflow problems when implementing it.

    Args:
        data (int): Complement data
        bit_width (int, optional): bit width. Defaults to 16.

    Returns:
        _type_: _description_
    """
    sign_bit = 1 << (bit_width - 1)
   
    if data & sign_bit:
        data = data - (1 << bit_width) # 补码转整数
    return data

def find_best_tap(arr: list) -> int:
    """
    此函数用于找出数组中离1最远的0的的位置

    Args:
        arr (list): 输入数组

    Returns:
        寻找最佳tap值
    """
    # 初始化变量
    max_distance = -1
    start_index = -1
    current_start_index = -1
    arr_len = len(arr)
    # 遍历数组
    for i in range(arr_len):
        if arr[i] == 0:
            # 如果当前值为0，则更新起始位置
            if current_start_index == -1:
                current_start_index = i
        else:
            # 如果当前值为1，则更新最大距离和对应的起始和终止位置
            if current_start_index != -1 and i - current_start_index > max_distance:
                max_distance = i - current_start_index
                start_index = current_start_index
            current_start_index = -1
    # 如果最后一段连续的0的长度大于已知的最大距离，则更新最大距离和对应的起始和终止位置
    if current_start_index != -1 and arr_len - current_start_index > max_distance:
        max_distance = arr_len - current_start_index
        start_index = current_start_index
    if start_index == 0:
        return 0
    elif start_index + max_distance - 1 == arr_len - 1:
        return arr_len - 1
    else:
        return int(start_index + max_distance / 2)


def replace_bytes(org: bytes,rep:bytes,start:int) -> bytes:
    """
    Replace byte data from specified location

    Args:
        org (bytes): Original Byte Array.
        rep (bytes): Replace Byte Array.
        start (int): Start position.

    Raises:
        ValueError: Value Error.

    Returns:
        Returns the replaced byte array.
    """
    if start + len(rep) > len(org):
        raise ValueError("rep or start value error!")
    result = org[:start]    # 获取开始位置之前的字节
    result += rep     # 添加替换字节 
    result += org[start+len(rep):]  # 添加开始位置之后的字节
    return result


class ProgressBar():
    """Progress bar util.
    """
    def __init__(self, max, symbol='*', hint='Progress'):
        """Init progress bar.

        Args:
            max (int): Max process.
            symbol (str, optional): Progress bar symbol. Defaults to '*'.
            hint (str, optional): Progress bar hint. Defaults to 'Progress'.
        """
        self.hint = hint
        self.max = max
        self.symbol = symbol
        self.progress = 0

    def set_hint(self, hint):
        """Set progress hint.

        Args:
            hint (str): Progress hint.
        """
        self.hint = hint

    def set_symbol(self, symbol):
        """Set progress bar sysmbol.

        Args:
            symbol (str): Progress bar symbol.
        """
        self.symbol = symbol

    def start(self):
        """Record process start time.
        """
        self.start = time.perf_counter()

    def update(self, increment, info=''):
        """Update process by *increment*

        Args:
            increment (int): The increment of process.
            info (str, optional): Process infomation. Defaults to ''.
        """
        self.progress += increment
        progress = self.progress
        all_work = self.max
        if self.progress > self.max:
            progress = self.max
        scale = 50
        i = int(progress / all_work * scale)
        completed = self.symbol * i
        remain = "." * (scale - i)
        completed_percent = (i / scale) * 100
        try:
            dur = time.perf_counter() - self.start
            print(f'\r{self.hint} {info} {completed_percent:^3.0f}%'
                  f'[{completed}->{remain}]{dur:.2f}s', end='')
        except AttributeError:
            print("start() is not implemented.")


# coding: utf-8
import datetime
import json
import datetime
import struct
import numpy as np

class DACalcFunc:
    def calc_02(self, x):
        y = 30 + 7.3 * (x - 39200) / 1000
        return round(y,2)

    def calc_03(self, x):
        # x=calc_13(x)
        x=(x>>24)+((x>>8)&0xFF00)+((x<<8)&0xFF0000)+((x<<24)&0xFF000000)
        return str(datetime.timedelta(seconds=x))

    def calc_04(self, x):
        return struct.unpack("<I", struct.pack(">I", x))[0]

    def calc_05(self, x):
        return struct.unpack("<H", struct.pack(">H", x))[0]

    def calc_06(self, x):
        sw_ver = (x & 0xFF000000) >> 24
        hw_ver = (x & 0xFF0000) >> 16
        big_ver = (x & 0xFF00) >> 8
        return f'{big_ver:02d}-{hw_ver:03d}-{sw_ver:03d}'

    def calc_07(self, x):
        b = struct.pack('<I', x)
        return '.'.join(str(i) for i in b)

    def calc_09(self, x):
        b = struct.pack('>H', x)
        #print(hex(x))
        ser = b[1]
        num = b[0]
        if 2 <= ser <= 20:
            s = chr(ord('A') + ser)
        elif 220 >= ser >= 26:
            s = '公司'
        else:
            s = 'A/B'
        return f'{s}-{num:03d}'

    def calc_12(self, x):
        return struct.unpack("<H", struct.pack(">H", x))[0]

    def calc_13(self, x):
        return struct.unpack('>I', struct.pack("<I", x))[0]

    def calc_14(self, x):
        return (struct.unpack('>I', struct.pack("<I", x))[0] >> 8)

    def calc_17(self, x):
        num =  self.calc_13(x)*3/65536
        s = f'{round(num,2)} V'
        return s

    def calc_19(self, x):
        num =  self.calc_13(x)/65536
        R = 10000 * num / (1.8 - num)
        B = 3435
        T2 = 273.15 + 25
        if R != 0:
            t = 1 / ((np.log(R / 10000) / B) + (1 / T2)) -273.15
            s = f'{round(t,2)}℃'
        else:
            s = '无温度'
        return s

    def calc_21(self, x):
        num =  self.calc_13(x)
        id = (num >> 16) & 0xF
        num = num & 0xFFFF
        if id > 3:
            s = "hold output"
        else:
            s = f'{num}'
        return s

    def calc_22(self, x):
        cnt = struct.unpack("<I", struct.pack(">I", x))[0]
        return f'{cnt/250} us'

    def calc_23(self, x):
        return struct.unpack("<h", struct.pack(">H", x))[0]

    def calc_24(self, x):
        sta_map = {
            0x0 : 'IDLE'         ,
            0x1 : 'READY'        ,
            0x2 : 'WRITE_DDR4'   ,
            0x3 : 'WRITE_OK'     ,
            0x4 : 'WRITE_ERROR1' ,
            0x5 : 'WRITE_ERROR2' ,
            0x6 : 'WRITE_ERROR3' ,
            0x7 : 'READ_DDR4'    ,
            0x8 : 'WR_END'       ,
            0x9 : 'DROP'         
        }
        err_map = {
            0:'NORMAL'        ,
            1:'ERR_WR_SHORT'  , #写DDR时数据比预期写入少
            2:'ERR_WR_LONG'   , #写DDR时数据比预期写入多
            3:'ERR_CMD'       , #错误指令
            4:'ERR_WR_TIMEOUT', #写超时
            5:'ERR_RD_TIMEOUT'  #读超时
        }
        try:
            sta_s =  sta_map[(x>>4) & 0x0F]
        except:
            sta_s = 'NONE'
        try:
            err_s =  err_map[(x>>1) & 0x07]
        except:
            err_s = 'NONE'
        rt_s = f'MEM:{sta_s}, ERR:{err_s}' if x & 0x01 else f'MEM:{sta_s}'
        return rt_s

    def calc_25(self, x):
        return f'0x{hex(x)}'

    def calc_26(self, x):
        cmd = '写' if (x >> 5) & 0x01 else '读'
        tdest = x & 0x1F
        return f'DDR{cmd}-{tdest}'

    ## 此函数解析风扇转数，具体计算过程还需沟通
    def calc_27(self, x):
        temp = self.calc_13(x)
        return f'{temp} 转/分钟'

    def calc_28(x):
        fan1 = (x & 0xFF000000) >> 24
        fan2 = (x & 0xFF0000) >> 16
        fan3 = (x & 0xFF00) >> 8
        fan4 = (x & 0xFF)
        return f'风扇1:{fan1} 转/分钟 风扇2:{fan2} 转/分钟  风扇3:{fan3} 转/分钟 风扇4:{fan4} 转/分钟'

    def calc_29(self, x):
        tmp = self.calc_13(x)
        return f'{tmp}%'

    # 槽位上下电信息
    def calc_30(self, x):
        slot_status = []
        for slot in range(20):
            power = (x >> slot ) & 0x01
            if power == 0:
                slot_status.append('槽位%d:上电'%slot)
            if power == 1:
                slot_status.append('槽位%d:未上电'%slot)
        return " ".join(slot_status)

    # 槽位初始化信息
    def calc_31(self, x):
        slot_status = []
        for slot in range(20):
            power = (x >> slot ) & 0x01
            if power == 0:
                slot_status.append('槽位%d:未初始化、初始化失败'%slot)
            if power == 1:
                slot_status.append('槽位%d:完成初始化'%slot)
        return " ".join(slot_status)

    # 槽位高速接口状态
    def calc_32(self, x):
        slot_status = []
        for slot in range(20):
            power = (x >> slot ) & 0x01
            if power == 0:
                slot_status.append('槽位%d:握手失败'%slot)
            if power == 1:
                slot_status.append('槽位%d:握手正常'%slot)
        return " ".join(slot_status)

class DAStatusParser:
    def __init__(self, json_file):
        self.parser_info = self.load_config_json(json_file)

    def load_config_json(self, file_name):
        with open(file_name, encoding='utf-8') as info:
            parse_info = json.load(info)
            return parse_info

    def byte_position(self, entry):
        get_byte_len = lambda l: (l >> 3) + ((l & 7) > 0)
        byte_offset = entry['startByte']
        bit_len = entry['bitLength']
        byte_len = get_byte_len(bit_len + entry['startBit'])
        return byte_offset, byte_len

    def masked_data(self, data, entry):
        bit_offset = entry['startBit']
        bit_len = entry['bitLength']
        mask = ((1 << bit_len) - 1) << bit_offset
        masked = (data & mask) >> bit_offset
        return masked

    def parse_data(self, data, entry, index):
        parse_type = entry['parseType']
        if parse_type == 'enum':
            option = entry['EnumValue'].get(str(data), {})
            value = option.get('name', 'undefined')
        elif parse_type == 'calc':
            calc_index = entry['dispIndex']
            func = getattr(DACalcFunc, f'calc_{calc_index:02d}', lambda x: x)
            value = func(self,data)
        else:
            value = data
        w = len(hex(data)) - 2
        w = w + (w & 1)
        return {'name': entry['name'], 'hex': f'0x{data:0{w}X}', 'value': value, 'index': index, 'parseType': parse_type}

    def parse_status(self, data):
        parse_info = self.parser_info
        items = []
        for i, entry in enumerate(parse_info):
            byte_offset, byte_len = self.byte_position(entry)
            seg = data[byte_offset:byte_offset+byte_len]
            seg_hex = int.from_bytes(seg, 'big')
            seg_data = self.masked_data(seg_hex, entry)
            item = self.parse_data(seg_data, entry, i+1)
            items.append(item)
        return items

