class CONST:    
    class ConstError(TypeError): 
        pass
    class ConstCaseError(ConstError): 
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("can't change const %s" % name)
        if not name.isupper():
            raise self.ConstCaseError('const name "%s" is not all uppercase' % name)
        self.__dict__[name] = value

const = CONST()

# Protocol const
const.MAX_MEM_SEND_FRAMES = 32 # 32kb速率 # const.Const(0xFFFF)  # 65535 描述了最大发送的帧数，不要超过这个值
const.MAX_REG_NUM = 183
const.MEM_FRAME_LEN = 1032
const.MEM_FRAME_DATA_LEN = 1024
const.MEM_FRAME_HEADER_LEN = 8
const.PROTOCOL_VERSION = '1.0'

# Hardware const
# const.ONE_CLOCK_PERIOD = 4e-9
const.ONE_CLOCK_PERIOD = 16e-9

# AWG const
const.Z_MIN_GAIN = -512
const.Z_MAX_GAIN = 511
const.XY_MIN_GAIN = 0
const.XY_MAX_GAIN = 1023
const.MIN_DECAY = 0
const.MAX_DECAY = 32
const.MIN_NCO_FREQUENCY = 0
const.MAX_NCO_FREQUENCY = 6e9
const.MIN_DEFAULT_VOLTAGE_CHANNEL = 9
# Minimum channel number of the AWG module
const.MIN_CHANNEL = 1
const.AWG_MIN_CHANNEL_AMOUNT = 1
# Maximum channel number of the AWG module
const.MAX_CHANNEL = 32
const.AWG_MAX_CHANNEL_AMOUNT = 32
# XY channel number of the AWG module
const.AWG_XY_CHANNEL_AMOUNT = 8
# Z channel number of the AWG module
const.AWG_Z_CHANNEL_AMOUNT = 24
# XYZ channel number of the AWG module
const.AWG_XYZ_CHANNEL_AMOUNT = 32

const.NCO_FREQUENCY_STEP = 10
const.MAX_WAVE = 20e4
const.MAX_SEQ_LEN = 16384
const.MIN_TARGET_VOLT = 0.5
const.MAX_TARGET_VOLT = 2
const.MIN_Z_OFFSET_CONTROL_STATUS = 0
const.MAX_Z_OFFSET_CONTROL_STATUS = 1
# XYZ通道寄存器定义:0 - 31
const.AWG_WAVE_ADDR = [(0x40000000 + (i << 19) * 16) for i in range(32)]
const.AWG_SEQ_ADDR = [(0x80000000+(i << 17) * 16) for i in range(32)]

# CMU const
# UDP response timeout
const.RESPONSE_TIMEOUT = 5
# Corresponds to the AWG slot number of the chassis
const.AWG_SLOTS = [0, 1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18, 19, 20]
# Corresponds to the DAQ slot number of the chassis
const.DAQ_SLOTS = [4, 15]
# Corresponds to the MIX slot number of the chassis
const.MIX_SLOTS = [5, 16]
# Corresponds to the CMU slot number of the chassis
const.CMU_SLOT = 23

# DAQ const
# Minimum channel number of the DAQ module
const.DAQ_MIN_CHANNEL_AMOUNT = 1
# Maximum channel number of the DAQ module
const.DAQ_MAX_CHANNEL_AMOUNT = 4

# MIX const
# Minimum channel number of the MIX module
const.MIX_MIN_CHANNEL_AMOUNT = 1
# Maximum channel number of the MIX module
const.MIX_MAX_CHANNEL_AMOUNT = 4

# DAQ模式
const.WAVE_MODE = 0
const.DEMO_MODE = 1
const.STATE_MODE = 2
const.FEED_MODE = 3

const.SAMPLE_RATE = 5 * 1e9 # 5G 采样率
#const.SAMPLE_RATE = 1 * 1e9
const.DEMO_QUBITS_MODE = [0, 1, 2]
const.RAM_NUM = 16
const.DEMOD_FREQ_COUNT = 16
const.RDOUT_FREQ_COUNT = 16
# 波形数据页地址
const.WAVE_DATA_ADDR_MALLOC = [0x100000000, 0x180000000, 0x200000000, 0x280000000]
# 解模页地址
const.DEMOD_DATA_ADDR_MALLOC = [0x140000000, 0x1C0000000, 0x240000000, 0x2C0000000]
# 态读出页地址
const.STATE_DATA_ADDR_MALLOC = [0x17E000000, 0x1FE000000, 0x27E000000, 0x2FE000000]


const.MIN_WAVE_SAMPLE_POSITION = -5e-6
const.MAX_WAVE_SAMPLE_POSITION = 5e-6
const.MIN_WAVE_SAMPLE_DEPTH = 0
const.MAX_WAVE_SAMPLE_DEPTH = 10e-6
const.MAX_WAVE_SAMPLE_COUNT = 8000000
const.MIN_DEMOD_WINDOW_START = 0
const.MAX_DEMOD_WINDWOS_START = 65535
const.MIN_FILTER_DATA = -32768
const.MAX_FILTER_DATA = 32767
const.QUBITS_4_WINDOW_WIDTH = 6.5536e-6
const.QUBITS_8_WINDOW_WIDTH = 3.2768e-6
const.QUBITS_16_WINDOW_WIDTH = 1.6384e-6
const.MAX_DEMOD_TRIG_COUNT = 8000000
const.MAX_FILTER_LENGTH = 32 * 1024
const.MATCH_FILTER_RAM_BASE_ADDRESS = [0x800000 + 0x100000 * i for i in range(4)]
const.MATCH_FILTER_RAM_OFFSET_ADDRESS = sorted([0x10000 * i for i in range(8)] + [0x8000 + 0x10000 * i for i in range(8)])
const.MIN_DAC_DELAY = 0
const.MAX_DAC_DELAY = 10e-6
const.MIN_DAC_WAVE_LENGTH = 0
const.MAX_DAC_WAVE_LENGTH = 16000
const.DAC_WAVE_BASE_ADDRESS = [0xC00000 + 0x40000 for i in range(4)]
const.DAC_WAVE_OFFSET_ADDRESS = [0x200000 + 0x1000 for i in range(4)]
const.MAX_RDOUT_TRIG_COUNT = 8000000

# AWG波形发生器、时序生成器基地址
const.DAC_WAVE_DATA_ADDR = [(0xC00000 + 0x40000 * i) for i in range(4)]
const.DAC_WAVE_SEQ_ADDR = [(0xC20000 + 0x40000 * i) for i in range(4)]
const.DAC_TIMING_DATA_ADDR = [(0xD00000 + 0x2000 * i) for i in range(4)]
const.DAC_TIMING_SEQ_ADDR = [(0xD01000 + 0x2000 * i) for i in range(4)]

const.DEMOD_DATA_LENGTH = 128
const.WAVE_DATA_HEAD_LENGTH = 16
const.STATES_DATA_LENGTH = 4