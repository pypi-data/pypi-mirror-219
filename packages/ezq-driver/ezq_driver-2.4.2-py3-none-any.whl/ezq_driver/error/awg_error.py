# coding: utf-8
from . import StandardEzqError

class AwgChannelOutOfRange(StandardEzqError):
    code = 30001

    def __init__(self, awg, mini, maxi, value):
        self.msg = (f'AWG {awg} set channel out of range, '
                    f'which should be between {mini} and {maxi}, got {value}')

class SetGainValueOutOfRange(StandardEzqError):
    code = 30002

    def __init__(self, awg, mini, maxi, value):
        self.msg = (f'AWG {awg} set gain value out of range, '
                    f'which should be between {mini} and {maxi}, got {value}')

class SetDefaultVoltageValueOutOfRange(StandardEzqError):
    code = 30004

    def __init__(self, awg, mini, maxi, value):
        self.msg = (f'AWG {awg} set default voltage value out of range, '
                    f'which should be between {mini} and {maxi}, got {value}')

class WaveLengthOutOfRange(StandardEzqError):
    code = 30006

    def __init__(self, awg, maxi, length):
        self.msg = (f'AWG {awg} write wave fail, wave length out of range, '
                    f'which should be less than {maxi}, got {length}')
        
class SetChannelTypeWrongError(StandardEzqError):
    code = 30007

    def __init__(self, awg, ch_type):
        self.msg = (f'AWG {awg} set gain channel type Wrong Error, '
                    f'the value should be xy or z, got {ch_type}')

class WaveSequenceLengthWrongError(StandardEzqError):
    code = 30008

    def __init__(self, awg, maxi, length):
        self.msg = (f'AWG {awg} write seq fail, seq length out of range, '
                    f'which should be less than {maxi}, got {length}')

class SetXYDecayValueOutOfRange(StandardEzqError):
    code = 30012

    def __init__(self, awg, mini, maxi, value):
        self.msg = (f'AWG {awg} set xy decay value out of range, '
                    f'which should be between {mini} and {maxi}, got {value}')

class IllegallNCOFrequencyError(StandardEzqError):
    code = 30014

    def __init__(self, frequency, step):
        self.msg = f'NCO frequency should be divided by {step},  got {frequency}'


class NCOFrequencyValueOutOfRange(StandardEzqError):
    code = 30015

    def __init__(self, awg, mini, maxi, frequency):
        self.msg = (f'AWG {awg} set NCO frequency value out of range, '
                    f'which should be between {mini} and {maxi}, got {frequency}')

class CalibrateControlValueOutOfRange(StandardEzqError):
    code = 30025

    def __init__(self, awg, mini, maxi, value):
        self.msg = (f'AWG {awg} set calibrate control value out of range, '
                    f'which should be between {mini} and {maxi}, got {value}')

class CalibrateControlTimeoutError(StandardEzqError):
    code = 30026

    def __init__(self, awg, waited_time, status):
        self.msg = (f'calibrate control timeout ({waited_time:g} s) for {awg}, '
                    f'op status equals to {status}')

class CalibrateControlFail(StandardEzqError):
    code = 30027

    def __init__(self, awg):
        self.msg = f'Set {awg} calibrate control fail'

class ZOffsetControlValueOutOfRange(StandardEzqError):
    code = 30028

    def __init__(self, awg, mini, maxi, value):
        self.msg = (f'AWG {awg} set z offset control channel out of range, '
                    f'which should be between {mini} and {maxi}, got {value}')

class SetTrigCountL1Fail(StandardEzqError):
    code = 10600107

    def __init__(self, awg):
        self.msg = f'Set {awg} trig count l1 fail'

class SetTrigIntervalL1Fail(StandardEzqError):
    code = 10600108

    def __init__(self, awg):
        self.msg = f'Set {awg} trig interval l1 fail'

class SetTrigSourceFail(StandardEzqError):
    code = 10600109

    def __init__(self, awg):
        self.msg = f'Set {awg} trig source fail'

class SetMultiBoardModeFail(StandardEzqError):
    code = 10600110

    def __init__(self, awg):
        self.msg = f'Set {awg} multi board mode fail'

class SetTrigStartFail(StandardEzqError):
    code = 10600111

    def __init__(self, awg):
        self.msg = f'Set {awg} trig start external fail'

class SetTrigStopFail(StandardEzqError):
    code = 10600111

    def __init__(self, awg):
        self.msg = f'Set {awg} trig stop external fail'

class SetDacStartFail(StandardEzqError):
    code = 10600112

    def __init__(self, awg):
        self.msg = f'Set {awg} dac start fail'

class SetDacStopFail(StandardEzqError):
    code = 10600112

    def __init__(self, awg):
        self.msg = f'Set {awg} dac stop fail'

class ClearTrigCountFail(StandardEzqError):
    code = 10600113

    def __init__(self, awg):
        self.msg = f'Clear {awg} trig count fail'

class TrigEnableFail(StandardEzqError):
    code = 10600114

    def __init__(self, awg):
        self.msg = f'Enable {awg} trigger fail'

class CheckTrigFail(StandardEzqError):
    code = 10600115

    def __init__(self, awg):
        self.msg = f'Check {awg} trig fail'

class SetQubitMapFail(StandardEzqError):
    code = 10600121

    def __init__(self, awg):
        self.msg = f'Set {awg} qubit map information fail'

class FeedbackEnable(StandardEzqError):
    code = 10600122

    def __init__(self, awg):
        self.msg = f'{awg} feedback enable fail'

class PipelineResetFail(StandardEzqError):
    code = 10600123

    def __init__(self, awg):
        self.msg = f'{awg} pipeline rest fail.'

class SetDownloadCircuitAmountFail(StandardEzqError):
    code = 10600124

    def __init__(self, awg):
        self.msg = f'Set {awg} download circuit amount fail.'

class SetSearchChannelCircuitFail(StandardEzqError):
    code = 10600125

    def __init__(self, awg):
        self.msg = f'Set {awg} search circuit number fail.'

class GetUnexpectedAnalysisResult(StandardEzqError):
    code = 10600126

    def __init__(self, awg, result):
        self.msg = f'Get unexpected analysis result code {result} for {awg}'

class EnableChannelCircuit(StandardEzqError):
    code = 10600127

    def __init__(self, awg, channel):
        self.msg = f'Enable {awg} channel {channel} circuit fail'

class GetUnexpectedAbandonState(StandardEzqError):
    code = 10600128

    def __init__(self, awg, channel, state):
        self.msg = f'Get unexpected abandon state {state} for {awg} channel {channel}'

class SetChannelAbandonStateFail(StandardEzqError):
    code = 10600129

    def __init__(self, awg, channel):
        self.msg = f'Set {awg} channel {channel} abandon state fail'

class TrigCountOufOfRange(StandardEzqError):
    code = 10600143

    def __init__(self, awg, mini, maxi, count):
        self.msg = (f'Set {awg} trig count l1 out of range, '
                    f'which should be between {mini} and {maxi}, got {count}')

class TrigIntervalOutOfRange(StandardEzqError):
    code = 10600144

    def __init__(self, awg, mini, maxi, trig_interval):
        self.msg = (f'Set {awg} trig interval out of range, '
                    f'which should be between {mini*1e9}ns and {maxi*1e3:.3}ms, got {trig_interval}')

class TrigStartOutOfRange(StandardEzqError):
    code = 10600145

    def __init__(self, awg, mini, maxi, count):
        self.msg = (f'Set {awg} trig start external out of range, '
                    f'which should be between {mini} and {maxi}, got {count}')

class TrigStopOutOfRange(StandardEzqError):
    code = 10600146

    def __init__(self, awg, mini, maxi, count):
        self.msg = (f'Set {awg} trig stop external out of range, '
                    f'which should be between {mini} and {maxi}, got {count}')

class TrigDelayOutOfRange(StandardEzqError):
    code = 10600147

    def __init__(self, awg, mini, maxi, point):
        self.msg = (f'Set {awg} trig delay point out of range, '
                    f'which should be between {mini*1e6}us and {maxi*1e6}us, got {point}')

class MultiBoardModeError(StandardEzqError):
    code = 10600148

    def __init__(self, awg, mode):
        self.msg = (f'Set {awg} mulit board mode error, '
                    f'which should be 0 or 1, got {mode}')

class TrigSelectChannelError(StandardEzqError):
    code = 10600149

    def __init__(self, awg, ch):
        self.msg = (f'Select {awg} trig channel error, '
                    f'which should be 1, 2, 3, 4 or 0, got {ch}')

class DacStartOutOfRange(StandardEzqError):
    code = 10600150

    def __init__(self, awg, mini, maxi, count):
        self.msg = (f'Set {awg} dac start out of range, '
                    f'which should be between {mini} and {maxi}, got {count}')

class DacStopOutOfRange(StandardEzqError):
    code = 10600151

    def __init__(self, awg, mini, maxi, count):
        self.msg = (f'Set {awg} dac stop out of range, '
                    f'which should be between {mini} and {maxi}, got {count}')

class DacDelayOutOfRange(StandardEzqError):
    code = 10600152

    def __init__(self, awg, mini, maxi, delay):
        self.msg = (f'Set {awg} dac delay out of range, '
                    f'which should be between {mini} and {maxi*1e6}us, got {delay}')

class TrigDelayWrongError(StandardEzqError):
    code = 10600153

    def __init__(self, awg, trig_delay, trig_interval):
        self.msg = (f'Set {awg} trig delay value {trig_delay} wrong, '
                    f'which should be less than trig interval value {trig_interval}')

class DefaultVoltOutOfRange(StandardEzqError):
    code = 10600155

    def __init__(self, awg, mini, maxi, volt):
        self.msg = (f'Set {awg} dac default volt out of range, '
                    f'which should be between {mini} and {maxi}, got {volt}')

class WaveDataOutOfRange(StandardEzqError):
    code = 10600156

    def __init__(self, awg, mini, maxi, min_data, max_data):
        self.msg = (f'Dac {awg} data in wave out of range, '
                    f'which should be between {mini} and {maxi},'
                    f'got min data {min_data}, got max data {max_data}')

class ChannelGainOutOfRange(StandardEzqError):
    code = 10600157

    def __init__(self, awg, mini, maxi, channel, gain):
        self.msg = (f'Set {awg} dac channel {channel} gain out of range, '
                    f'which should be between {mini} and {maxi}, got {gain}')

class ChannelOffsetOutOfRange(StandardEzqError):
    code = 10600158

    def __init__(self, awg, mini, maxi, channel, offset):
        self.msg = (f'Set {awg} dac channel {channel} offset out of range, '
                    f'which should be between {mini} and {maxi}, got {offset}')

class IllegalIpAddressError(StandardEzqError):
    code = 10600159

    def __init__(self, ip_address):
        self.msg = (f'IP address {ip_address} is illegal, '
                    f'which should be suit IPV4 format, '
                    f'and start with 172 or 10')

class IllegalMacAddressError(StandardEzqError):
    code = 10600160

    def __init__(self, mac_address):
        self.msg = (
            f'AWG mac address length should be '
            f'equal to 64 bit, got {mac_address}')

class InstructionEmptyError(StandardEzqError):
    code = 10600161

    def __init__(self):
        self.msg = f'Instruction is empty'

class InstructionParaNumError(StandardEzqError):
    code = 10600162

    def __init__(self, inst_name, arg_num, given_num):
        self.msg = f'{inst_name}() takes exactly {arg_num} argument ({given_num} given)'

class InstructionNameError(StandardEzqError):
    code = 10600163

    def __init__(self, inst_name):
        self.msg = f'Instruction {inst_name} is not in instruction map'

class InstructionParaError(StandardEzqError):
    code = 10600164

    def __init__(self, inst_name, inst_para):
        self.msg = f'Instruction {inst_name} got an unexpected keyword argument "{inst_para}"'

class RegAmountNotEqualError(StandardEzqError):
    code = 10600165

    def __init__(self, address_amount, data_amount):
        self.msg = f'Instruction reg address amount {address_amount} is not equal to reg data amount {data_amount}'


class WaveTypeOrDimensionWrongError(StandardEzqError):
    code = 10600166

    def __init__(self, daq, type, dim):
        self.msg = (f'AWG {daq} download wave data fail, ' 
                   f'which wave data type should be numpy.ndarray, got {type} '
                   f'or wave data dimension is 2, got {dim}')
        
class SeqTypeOrDimensionWrongError(StandardEzqError):
    code = 10600167

    def __init__(self, daq, type, dim):
        self.msg = (f'AWG {daq} download seq data fail, ' 
                   f'which seq data type should be numpy.ndarray, got {type} '
                   f'or seq data dimension is 1, got {dim}')
