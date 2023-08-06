from . import StandardEzqError


class ConnectFail(StandardEzqError):
    code = 200001

    def __init__(self, slot):
        self.msg = f'Connect to ezq device fail'


class ReConnectFail(StandardEzqError):
    code = 200002

    def __init__(self):
        self.msg = f'Re-connect to ezq device fail'


class InitDeviceFail(StandardEzqError):
    code = 200003

    def __init__(self, slot):
        self.msg = f'Init ezq device slot {slot} fail'


class RebootFail(StandardEzqError):
    code = 200004

    def __init__(self, slot):
        self.msg = f'Slot {slot} reboot fail'


class BinFileNotFoundError(StandardEzqError):
    code = 200005

    def __init__(self, file_path):
        self.msg = f'Could not find the bin file on path : {file_path}'


class WriteDDRTimeoutError(StandardEzqError):
    code = 200006

    def __init__(self, slot, max_times):
        self.msg = (f'Slot {slot} write ddr {max_times} times timeout, '
                    f'data written to ddr is different from read back data')


class WriteFlashTimeoutError(StandardEzqError):
    code = 200007

    def __init__(self, slot, waited_time, status):
        self.msg = (f'Write data to flash from DDR timeout ({waited_time:g} s) for slot {slot}, '
                    f'op status equals to {status}')


class ReadFlashTimeoutError(StandardEzqError):
    code = 200008

    def __init__(self, slot, waited_time, status):
        self.msg = (f'Read data from flash accroding to DDR timeout ({waited_time:g} s) for {slot}, '
                    f'op status equals to {status}')


class FlashDataNotMatch(StandardEzqError):
    code = 200009

    def __init__(self, slot):
        self.msg = f'Data read from bin file is different from data written to slot {slot} flash area'


class WriteEepromTimeoutError(StandardEzqError):
    code = 200010

    def __init__(self, slot, waited_time, status):
        self.msg = (f'Write data to eeprom from DDR timeout ({waited_time:g} s) for slot {slot}, '
                    f'op status equals to {status}')


class ReadEepromTimeoutError(StandardEzqError):
    code = 200011

    def __init__(self, slot, waited_time, status):
        self.msg = (f'Read data from eeprom accroding to DDR timeout ({waited_time:g} s) for {slot}, '
                    f'op status equals to {status}')


class EepromDataNotMatch(StandardEzqError):
    code = 200012

    def __init__(self, slot):
        self.msg = f'Data read from bin file is different from data written to slot {slot} eeprom area'


class IllegalIpAddressError(StandardEzqError):
    code = 200013

    def __init__(self, ip_address):
        self.msg = (f'IP address {ip_address} is illegal, '
                    f'which should be suit IPV4 format, '
                    f'and start with 172 or 10')
        
class DDRDataNotMatch(StandardEzqError):
    code = 200014

    def __init__(self, slot):
        self.msg = f'Data read from bin file is different from data written to slot {slot} DDR area'


class SlotPowerStatusError(StandardEzqError):
    code = 200015

    def __init__(self, slot):
        self.msg = f'The current {slot} board does not exist or is not powered on'
