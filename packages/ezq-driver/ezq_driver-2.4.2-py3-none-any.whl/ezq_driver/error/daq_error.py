from . import StandardEzqError


class ChannelWrongError(StandardEzqError):
    code = 400001

    def __init__(self, daq, channel):
        self.msg = f'Got the wrong channel {channel} for slot {daq}'


class ModeWrongError(StandardEzqError):
    code = 400002

    def __init__(self, daq, mode):
        self.msg = (f'Got the wrong mode {mode} for slot {daq}, only for '
                    f'0-wave_mode, 1-demo_mode, 2-state_mode')


class SampleCountOutOfRange(StandardEzqError):
    code = 400003

    def __init__(self, daq, mini, maxi, count, mode):
        self.msg = (f'Set slot {daq} demod width out of range for {mode} mode, '
                    f'which should be between {mini} and {maxi}, got {count}')


class WaveStartTimeOutOfRange(StandardEzqError):
    code = 400004

    def __init__(self, daq, mini, maxi, start_time):
        self.msg = (f'Set slot {daq} wave start time out of range, '
                    f'which should be between {mini} and {maxi}, got {start_time}')


class WaveSampleDepthOutOfRange(StandardEzqError):
    code = 400005

    def __init__(self, daq, mini, maxi, sample_depth):
        self.msg = (f'Set slot {daq} wave sample depth out of range, '
                    f'which should be between {mini} and {maxi}, got {sample_depth}')


class DemodWindowStartOutOfRange(StandardEzqError):
    code = 400006

    def __init__(self, daq, mini, maxi, start):
        self.msg = (f'Set slot {daq} demod start out of range, '
                    f'which should be between {mini} and {maxi}, got {start}')


class DemodWindowWidthOutOfRange(StandardEzqError):
    code = 400007

    def __init__(self, daq, mini, maxi, width, qubits_mode):
        self.msg = (f'Set slot {daq} demod width out of range for {qubits_mode} qubits mode, '
                    f'which should be between {mini} and {maxi}, got {width}')


class DemodFrequencyLengthNotMatch(StandardEzqError):
    code = 400008

    def __init__(self, freq_length, qubit_length):
        self.msg = (f'The length of demod frequency {freq_length} '
                    f'does not macth the length of qubit {qubit_length}')


class FilterDataLengthOutOfRange(StandardEzqError):
    code = 400009

    def __init__(self, daq, length, max_length):
        self.msg = (f'Slot {daq} filter data length out of range '
                    f'which should be less than {max_length}, got {length}')


class DacWaveDelayOutOfRange(StandardEzqError):
    code = 400010

    def __init__(self, daq, mini, maxi, wave_delay):
        self.msg = (f'Set slot {daq} wave delay out of range, '
                    f'which should be between {mini} and {maxi}, got {wave_delay}')


class DacWaveLengthOutOfRange(StandardEzqError):
    code = 400011

    def __init__(self, daq, mini, maxi, wave_length):
        self.msg = (f'Set slot {daq} wave delay out of range, '
                    f'which should be between {mini} and {maxi}, got {wave_length}')


class ReceiveDataTimeOut(StandardEzqError):
    code = 400012

    def __init__(self, daq, timeout):
        self.msg = f'Slot {daq} receive data timeout in {timeout} seconds'

class WaveLengthOutOfRange(StandardEzqError):
    code = 400013

    def __init__(self, awg, maxi, length):
        self.msg = (f'DAQ {awg} write wave fail, wave length out of range, '
                    f'which should be less than {maxi}, got {length}')
        
class WaveSequenceLengthWrongError(StandardEzqError):
    code = 400014

    def __init__(self, awg, maxi, length):
        self.msg = (f'DAQ {awg} write seq fail, seq length out of range, '
                    f'which should be less than {maxi}, got {length}')

class GeneratorTypeWrongError(StandardEzqError):
    code = 400015

    def __init__(self, daq, type):
        self.msg = (f'Got the wrong generator type {type} for slot {daq}, only for '
                    f'ifout, ifin.')
        
class QubitsModeWrongError(StandardEzqError):
    code = 400016

    def __init__(self, daq, mode):
        self.msg = (f'Got the wrong mode {mode} for slot {daq}, only for '
                    f'16-qubits, 8-qubits , 4-qubits')
        
class WaveTypeOrDimensionWrongError(StandardEzqError):
    code = 400017

    def __init__(self, daq, type, dim):
        self.msg = (f'DAQ {daq} download wave data fail, ' 
                   f'which wave data type should be numpy.ndarray, got {type} '
                   f'or wave data dimension is 2, got {dim}')
        
class SeqTypeOrDimensionWrongError(StandardEzqError):
    code = 400018

    def __init__(self, daq, type, dim):
        self.msg = (f'DAQ {daq} download seq data fail, ' 
                   f'which seq data type should be numpy.ndarray, got {type} '
                   f'or seq data dimension is 1, got {dim}')
        
class DemodWindowWidthAndStartNotMatch(StandardEzqError):
    code = 400019

    def __init__(self, freq_length, window_width_length, window_start_length):
        self.msg = (f'The length of demod frequency list length {freq_length} '
                    f'does not macth the length of window width length {window_width_length} or window start leng {window_start_length}')
        

class DemodWindowWidthAndStartLengthOutOfRange(StandardEzqError):
    code = 400020

    def __init__(self, qubits_mode, qubit_max_demod_len, window_width_length, window_start_length):
        self.msg = (f'Qubits Mode {qubits_mode} require the sum of demod window width length and window start length is {qubit_max_demod_len}, '
                    f'which demod window width length is {window_width_length},window start length is {window_start_length}')
        
class DemodWeightDimensionNotMatch(StandardEzqError):
    code = 400021

    def __init__(self, depth, rows, columns):
        self.msg = (f'The Demod weight dimension require depth {depth}, rows {rows}, columns {columns}')