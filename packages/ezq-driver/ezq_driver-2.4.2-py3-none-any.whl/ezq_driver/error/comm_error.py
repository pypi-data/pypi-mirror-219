# coding: utf-8
from . import StandardEzqError

class RegRetransmissionTimeout(StandardEzqError):
    code = 100001

    def __init__(self, awg, times):
        self.msg = f'DAC {awg} send registers commads {times} times retransmission timeout'

class TooManyRegisterEnriesError(StandardEzqError):
    code = 100002

    def __init__(self, count, expected):
        self.msg = (
            f'Too many register entries in one frame, '
            f'should not be more than {expected}, '
            f'got {count}')

class WriteMemRetransmissionTimeout(StandardEzqError):
    code = 100003

    def __init__(self, slot, times):
        self.msg = f'Ezq slot {slot} write memory {times} times retransmission timeout'

class ReadMemRetransmissionTimeout(StandardEzqError):
    code = 100004

    def __init__(self, slot, times):
        self.msg = f'Ezq slot {slot} read memory {times} times retransmission timeout'

class IllegalResponseError(StandardEzqError):
    code = 100005

    def __init__(self, tag):
        self.msg = (
            f'Tag in memory writing command '
            f'response should be USTC, got {tag}')

class IllegalMemoryAddressError(StandardEzqError):
    code = 100006

    def __init__(self, address, segment):
        self.msg = (
            f'AWG memory address should be '
            f'divided by {segment}, got {address}')

class IllegalMemoryFrameLengthError(StandardEzqError):
    code = 100007

    def __init__(self, count, expected):
        self.msg = (
            f'Length of memory frames should be '
            f'divided by {expected}, got {count}')

class RecvTimeoutError(StandardEzqError):
    code = 100008

    def __init__(self, awg, recv=None, expect=None, waited_time=None):
        if isinstance(awg, list):
            awg = ', '.join([str(a) for a in awg])

        if None in {recv, expect, waited_time}:
            self.msg = f'Recv timeout for {awg}'
        else:
            self.msg = (
                f'Recv timeout ({waited_time:g} s) for {awg}, '
                f'expecting {expect} bytes, '
                f'{recv} bytes received')

class SendNotMatchRecvError(StandardEzqError):
    code = 100009

    def __init__(self, awg, sent, recv):
        self.msg = f'Sent {sent} frames to {awg}, only {recv} received by awg'

class ReadRegisterPermissionError(StandardEzqError):
    code = 100010

    def __init__(self, name):
        self.msg = f'Read Permission Denied for register module {name}'

class WriteRegisterPermissionError(StandardEzqError):
    code = 100011

    def __init__(self, name):
        self.msg = f'Write Permission Denied for register module {name}'

class RegisterMapKeyError(StandardEzqError):
    code = 100012

    def __init__(self, reg, device_type):
        self.msg = f'Key {reg} is not in {device_type} register map'

class RegisterWriteAndReadDataError(StandardEzqError):
    code = 100013

    def __init__(self, slot):
        self.msg = f'The Slot {slot} write and read register data abnormally!'

class DDRWriteAndReadDataError(StandardEzqError):
    code = 100014

    def __init__(self, slot, test_type, data_type,length,addr):
        self.msg = f'The Slot {slot} write and read ddr data abnormally! '
        f'check type:{test_type}, data type:{data_type},date length:{length},check address:{addr}'