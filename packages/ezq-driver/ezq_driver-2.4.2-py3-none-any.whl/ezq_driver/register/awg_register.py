# coding: utf-8
_AWG_REGISTER_TABLE = [
    dict(
        name='CPU',
        base_addr=0x080000,
        registers=[
            (0x0000, 'IDNTITY', 'r'),
            (0x0004, 'FIX_DATE', 'r'),
            (0x0008, 'RESERVE', 'r'),
            (0x000C, 'TESTREG', 'rw'),
            (0x0014, 'BOARD_ID', 'r'),
            (0x0018, 'OP_TIME', 'r'),
            (0x001C, 'OP_STATUS', 'r'),
            (0x0020, 'FUNCTION', 'rw'),
            (0x0024, 'FLASH_TYPE', 'rw'),
            (0x0028, 'LOAD_CONFIG', 'r'),
            (0x002C, 'DATA_LEN', 'rw'),
            (0x0030, 'FLASH_ADDR', 'rw'),
            (0x0034, 'DDR_ADDR', 'rw'),
            (0x0038, 'TDEST', 'rw'),
            (0x0040, 'HARDWARE_RDY', 'r'),
            (0x0044, 'STATUS_EN', 'rw'),
            (0x0048, 'LOAD_WAVE', 'rw'),
            (0x004C, 'LOAD_SEQ', 'rw'),
            (0x0050, 'CALIBRATE_Z', 'w'),
            (0x0054, 'CALIBRATE_RESULT', 'r'),
            (0x0058, 'EEPROM_STATUS', 'rw'),
            (0x005C, 'TARGET_VOLT', 'rw'),
        ]
    ),
    dict(
        name='PIPELINE',
        base_addr=0x090000,
        registers=[
            (0x0000, 'IDNTITY', 'r'),
            (0x0004, 'FIX_DATE', 'r'),
            (0x0008, 'RESERVE', 'r'),
            (0x000C, 'TESTREG', 'rw'),
            (0x0010, 'PIPELINE_INIT', 'w'),
            (0x0014, 'RESERVE_1', 'r')
        ] + [
            (0x0018 + 0x20 * i, f'INSTR_FREE_SPACE_{i + 1}', 'r') for i in range(32)
        ] + [
            (0x001C + 0x20 * i, f'INSTR_CATHE_START_NUM_{i + 1}', 'r') for i in range(32)
        ] + [
            (0x0020 + 0x20 * i, f'INSTR_DOWNLOAD_{i + 1}', 'rw') for i in range(32)
        ] + [
            (0x0024 + 0x20 * i, f'CIRCUIT_NUM_INQUIRE_{i + 1}', 'rw') for i in range(32)
        ] + [
            (0x0028 + 0x20 * i, f'CIRCUIT_NUM_STATUS_{i + 1}', 'rw') for i in range(32)
        ] + [
            (0x002C + 0x20 * i, f'CIRCUIT_NUM_EXECUTE_{i + 1}', 'rw') for i in range(32)
        ] + [
            (0x0030 + 0x20 * i, f'ABANDON_ID_{i + 1}', 'rw') for i in range(32)
        ] + [
            (0x0034 + 0x20 * i, f'ABANDON_STATUS_{i + 1}', 'rw') for i in range(32)
        ]
    ),
    dict(
        name='TRIG',
        base_addr=0x240000,
        registers=[
            (0x0000, 'IDNTITY', 'r'),
            (0x0004, 'FIX_DATE', 'r'),
            (0x0008, 'RESERVE', 'r'),
            (0x000C, 'TESTREG', 'rw'),
            (0x0080, 'TRIG_CLEAR', 'rw'),
            (0x0084, 'TRIG_START', 'rw'),
            (0x0088, 'TRIG_CNT_SET', 'rw'),
            (0x008C, 'TRIG_INTERVAL_SET', 'rw'),
            (0x0090, 'TRIG_WIDTH_SET', 'rw'),
            (0x0094, 'TRIG_SEL', 'rw'),
            (0x0098, 'RECVED_TRIG_CNT', 'r'),
            (0x009C, 'GENERATED_TRIG_CNT', 'r')
        ]
    ),
    dict(
        name='FEEDBACK',
        base_addr=0x260000,
        registers=[
            (0x0000, 'IDNTITY', 'r'),
            (0x0004, 'FIX_DATE', 'r'),
            (0x0008, 'RESERVE', 'r'),
            (0x000C, 'TESTREG', 'rw'),
        ] + [
            (0x0080 + 0x04 * i, f'QUBIT_INFO_MAP[{9 + 4 * i}-{12 + 4 * i}]', 'rw') for i in range(6)
        ]
    ),
    dict(
        name='CHIP_CONFIG',
        base_addr=0x0F0000,
        registers=[
            (0x0000, 'IDNTITY', 'r'),
            (0x0004, 'FIX_DATE', 'r'),
            (0x0008, 'RESERVE', 'r'),
            (0x000C, 'TESTREG', 'rw'),
            (0x0010, 'CHANNEL_STATUS', 'r'), # 通道(1-28)工作状态
            (0x0014, 'CHIP_STATUS', 'r'), # DAC(1-19)芯片状态
            (0x0018, 'DAC_XY_TEMP', 'r'), # DAC芯片XY通道温度
            (0x001C, 'DAC_Z_TEMP', 'r'), # DAC芯片Z通道温度
            (0x00D0, 'Z_OFFSET_CONTROL', 'rw'), # Z通道校准使能、停止
            (0x0130, 'CLK_MONITOR', 'rw') # 时钟芯片锁定状态监控
        ] + [
            (0x0020 + 0x04 * i, f'CH{i+1}_GAIN', 'rw') for i in range(32) # XY通道增益
        ] + [
            (0x00B0 + 0x04 * i, f'CH{i+1}_NCO_FREQ', 'rw') for i in range(8) # XY通道NCO频率设置
        ] + [
            (0x00E0 + 0x04 * i, f'CH{i+1}_D_SET', 'rw') for i in range(8) # XY通道衰减设置 
        ] + [
            (0x0100 + 0x04 * i, f'CH{i+1}_F_VOLT', 'rw') for i in range(8) # XY通道滤波器电压设置
        ] + [
            (0x0140 + 0x04 * i, f'AD9164_{i+1}_STATUS', 'rw') for i in range(8) # 通道JESD链路状态监控
        ] + [
            (0x0160 + 0x04 * i, f'AD9154_{i+1}_STATUS', 'rw') for i in range(6) # 通道JESD链路状态监控
        ]
    )
] + [
    dict(
        name=f'AWG_A_{i+1}',
        base_addr=0x870000 + i * 0x010000,
        registers=[
            (0x0000, 'IDNTITY', 'r'),
            (0x0004, 'FIX_DATE', 'r'),
            (0x0008, 'RESERVE', 'r'),
            (0x000C, 'TESTREG', 'rw'),
            (0x0020, 'CTRL_REG', 'rw'),
        ] + [
            (0x0030 + 0x10 * i, f'CNFG_REG{i+1}', 'rw') for i in range(4)
        ] + [
            (0x0034 + 0x10 * i, f'LOOP_CNT{i+1}', 'rw') for i in range(4)
        ] + [
            (0x0038 + 0x10 * i, f'DEFAULT_CODE{i+1}', 'rw') for i in range(4)
        ] + [
            (0x0080 + 0x04 * i, f'STATUS{i+1}', 'r') for i in range(4)
        ]
    ) for i in range(2)
] + [
    dict(
        name=f'AWG_B_{i+1}',
        base_addr=0x890000 + i * 0x010000,
        registers=[
            (0x0000, 'IDNTITY', 'r'),
            (0x0004, 'FIX_DATE', 'r'),
            (0x0008, 'RESERVE', 'r'),
            (0x000C, 'TESTREG', 'rw'),
            (0x0020, 'CTRL_REG', 'rw')
        ] + [
            (0x0030 + 0x10 * i, f'CNFG_REG{i+1}', 'rw') for i in range(4)
        ] + [
            (0x0034 + 0x10 * i, f'LOOP_CNT{i+1}', 'rw') for i in range(4)
        ] + [
            (0x0038 + 0x10 * i, f'DEFAULT_CODE{i+1}', 'rw') for i in range(4)
        ] + [
            (0x0080 + 0x04 * i, f'STATUS{i+1}', 'r') for i in range(4)
        ]
    ) for i in range(6)
]
