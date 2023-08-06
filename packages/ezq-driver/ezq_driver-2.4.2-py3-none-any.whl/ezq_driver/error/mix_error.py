from . import StandardEzqError

class MixChannelWrongError(StandardEzqError):

    code = 500001

    def __init__(self, daq, channel):
        self.msg = f'Got the wrong channel {channel} for slot {daq}'

class PumpPowerOutOfRange(StandardEzqError):
    code = 500002

    def __init__(self, mix, mini, maxi, power):
        self.msg = (f'Set slot {mix} pump power out of range, '
                    f'which should be between {mini} and {maxi}, got {power}')
        
class PumpFrequencyOutOfRange(StandardEzqError):
    code = 500003

    def __init__(self, mix, mini, maxi, frequency):
        self.msg = (f'Set slot {mix} pump frequency out of range, '
                    f'which should be between {mini} and {maxi}, got {frequency}')

class MixTypeWrongError(StandardEzqError):
    code = 500004

    def __init__(self, mix, type):
        self.msg = f'Got the wrong mix type {type} for slot {mix}, '
        f'which should be mix1 or mix2, got {type}.'

class MixRegisterWriteAndReadError(StandardEzqError):
    code = 500005

    def __init__(self, slot):
        self.msg = f'The Slot {slot} write and read register data abnormally!'

class MixSelfCheckError(StandardEzqError):
    code = 500006

    def __init__(self, slot, info):
        self.msg = f'The Slot {slot} self-check error! {info}.'