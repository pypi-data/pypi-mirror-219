# coding: utf-8
_DAQ_REGISTER_TABLE = [
    dict(
        name=f'STATUS',
        base_addr=0x500000,
        registers=[
            (0x0018,'UPDATE_PROCESS','r'),
        ]
    ),
    dict(
        name='CHIP_CTRL',
        base_addr=0x070000,
        registers=[
        ]
    )
] + [
    dict(
        name='DDS',
        base_addr=0x080000,
        registers=[
            (0x0000,'REG2MICR_INTR','rw'),
            (0x0004, 'CHANNEL_SEL', 'rw'),
            (0x0008,'CHANNEL_FUNC0_H','rw'),
            (0x000C,'CHANNEL_FUNC0_L','rw'),
            (0x0010, 'CHANNEL_FUNCL', 'rw'),
            (0x0014,'FULL_SCALE_CURRENT','rw'),
            (0x0018, 'FREQ_TUNING_WORD_H', 'rw'),
            (0x001C, 'FREQ_TUNING_WORD_L', 'rw'),
            (0x0020, 'PHASE_AMPLITUDE_CTRL', 'rw'),
        ]
    )
] + [
    dict(
    	name='MULT_FUNC',
    	base_addr=0x080000,
    	registers=[
            # 中断寄存器数据定义:写值1->DDS芯片配置（实时）,2->DDS芯片配置,3->DAC9164芯片配置,4->ADC芯片校准,5->远程更新,6->硬件板卡信息修改
            (0x0000,'REG2MICR_INTR','rw'),
            (0x0004,'MUL_FUNC_PARAM1','rw'),
            (0x0008,'MUL_FUNC_PARAM2','rw'),
            (0x000C,'MUL_FUNC_PARAM3','rw'),
            (0x0010,'MUL_FUNC_PARAM4','rw'),
            (0x0014,'MUL_FUNC_PARAM5','rw'),
            (0x0018,'MUL_FUNC_PARAM6','rw'),
            (0x001C,'MUL_FUNC_PARAM7','rw'),
            (0x0020,'MUL_FUNC_PARAM8','rw'),
            (0x0024,'MUL_FUNC_PARAM9','rw'),
            (0x0028,'MUL_FUNC_PARAM10','rw'),
            (0x002C,'MUL_FUNC_PARAM11','rw'),
            (0x0030,'MUL_FUNC_PARAM12','rw'),
            (0x0034,'MUL_FUNC_PARAM13','rw'),
            (0x0038,'MUL_FUNC_PARAM14','rw'),
            (0x003C,'MUL_FUNC_PARAM15','rw'),
            (0x0040,'MUL_FUNC_PARAM16','rw'),
            (0x0044,'MUL_FUNC_PARAM17','rw'),
            (0x0048,'MUL_FUNC_PARAM18','rw'),
            (0x004C,'MUL_FUNC_PARAM19','rw'),
            (0x0050,'MUL_FUNC_PARAM20','rw'),
            (0x0054,'MUL_FUNC_PARAM21','rw'),
            (0x0058,'MUL_FUNC_PARAM22','rw'),
            (0x005C,'MUL_FUNC_PARAM23','rw'),
            (0x0060,'MUL_FUNC_PARAM24','rw'),
            (0x0064,'MUL_FUNC_PARAM25','rw'),
            (0x0068,'MUL_FUNC_PARAM26','rw'),
            (0x006C,'MUL_FUNC_PARAM27','rw'),
            (0x0070,'MUL_FUNC_PARAM28','rw'),
            (0x0074,'MUL_FUNC_PARAM29','rw'),
            (0x0078,'MUL_FUNC_PARAM30','rw'),
            (0x007C,'MUL_FUNC_PARAM31','rw')
        ]
    )
] + [
    dict(
        name=f'DAQ_{j}',
        base_addr=0x100000 + 0x1000 * j,
        registers=[
            (0x0000, 'COMMAND', 'w'),
            (0x0004, 'TRIG_LEVEL', 'rw'),
            (0x0008, 'FUNCTION', 'rw'),
            (0x0020, 'WAVE_STORE_ADDR', 'rw'),
            (0x0024, 'WAVE_STORE_TS_MASK', 'rw'),
            (0x0028, 'WAVE_SAMPLE_POSITION', 'rw'),
            (0x002C, 'WAVE_SAMPLE_DEPTH', 'rw'),
            (0x0030, 'WAVE_TRIG_COUNT', 'rw'),
            (0x0034, 'WAVE_DATA_COUNT', 'r'),
            (0x0040, 'DEMOD_STORE_ADDR', 'rw'),
            (0x0044, 'DEMOD_STORE_TS_MASK', 'rw'),
            (0x0048, 'DEMOD_WINDOW_START', 'rw'),
            (0x004C, 'DEMOD_WINDOW_WIDTH', 'rw'),
            (0x0050, 'DEMOD_TRIG_COUNT', 'rw'),
            (0x0054, 'DEMOD_DATA_COUNT', 'rw'),
            (0x0060, 'RDOUT_STORE_ADDR', 'rw'),
            (0x0064, 'RDOUT_STORE_TS_MASK', 'rw'),
            (0x0068, 'RDOUT_DATA_COUNT', 'rw'),
            (0x006C, 'RDOUT_TRIG_COUNT', 'rw'),
            (0x0080, 'FB_TS_MASK', 'rw'),
            (0x0084, 'PULSE_WIDTH1', 'rw'), # IDS-20230612-change: FEEDBACK -> DAQ
            (0x0088, 'PULSE_WIDTH2', 'rw'), # IDS-20230612-change: FEEDBACK -> DAQ
        ] + [
            (0x0200 + i * 0x20, f'STATE_EST_Q{i}_AB_0', 'rw') for i in range(16)
        ] + [
            (0x0204 + i * 0x20, f'STATE_EST_Q{i}_C_0', 'rw') for i in range(16)
        ] + [
            (0x0208 + i * 0x20, f'STATE_EST_Q{i}_AB_1', 'rw') for i in range(16)
        ] + [
            (0x020C + i * 0x20, f'STATE_EST_Q{i}_C_1', 'rw') for i in range(16)
        ] + [
            (0x0210 + i * 0x20, f'STATE_EST_Q{i}_AB_2', 'rw') for i in range(16)
        ] + [
            (0x0214 + i * 0x20, f'STATE_EST_Q{i}_C_2', 'rw') for i in range(16)
        ] + [
            (0x0218 + i * 0x20, f'RSV_{2 + i * 2}', 'rw') for i in range(16)
        ] + [
            (0x021C + i * 0x20, f'RSV_{3 + i * 2}', 'rw') for i in range(16)
        ]
    ) for j in range(4)
] + [
    dict(
        name=f'DAC_WAVE_{j}',
        base_addr = 0x200000 + 0x1000 * j, # 波形发生器寄存器控制基地址
        registers = [
            (0x0000,'IDNTITY','r'),
            (0x0004,'FIX_DATE','r'),
            (0x0008,'RESERVE','r'),
            (0x000C,'TESTREG','rw'),
            (0x0020,'CTRL_REG','w'),
            (0x0030,'CNFG_REG','rw'),
            (0x0034,'LOOP_CNT','rw'),
            (0x0038,'DEFAULT_CODE','rw'),
            (0x003C,'STATUS','r')
        ]
    ) for j in range(4)
] + [
    dict(
        name=f'DAC_TIMING_{j}',
        base_addr = 0x104000 + 0x1000 * j, # 时序发生器寄存器控制基地址
        registers = [
            (0x0000,'IDNTITY','r'),
            (0x0004,'FIX_DATE','r'),
            (0x0008,'RESERVE','r'),
            (0x000C,'TESTREG','rw'),
            (0x0020,'CTRL_REG','w'),
            (0x0030,'CNFG_REG','rw'),
            (0x0034,'LOOP_CNT','rw'),
            (0x0038,'DEFAULT_CODE','rw'),
            (0x003C,'STATUS','r')
        ]
    ) for j in range(4)
] + [
    dict(
        name='SYNC', # 参考IDS-20230509
        base_addr=0x400000,
        registers=[
            (0x0000, 'COMMAND', 'w'),
            (0x0004, 'FUNCTION', 'rw'),
            (0x0008, 'SYNC_TIMER_L', 'r'),
            (0x000C, 'SYNC_TIMER_H', 'r'),
            (0x0010, 'SYNC_CTRL', 'rw'),
            (0x0014, 'RSV', 'rw'), # IDS-20230509-change: CASC_CTRL -> RSV
            (0x0018, 'INTRA_CYCLE_P', 'rw'),
            (0x001C, 'INTRA_CYCLE_C', 'rw')
            ]
        )
] + [
    dict(
        name=f'AWG_{j}',
        base_addr=0x200000 + 0x1000 * j,
        registers=[
            (0x0000, 'COMMAND', 'w'),
            (0x0004, 'FUNCTION', 'rw'),
            (0x0008, 'WAVE_DELAY', 'rw'),
            (0x000C, 'WAVE_LENGTH', 'rw'),
            (0x0010, 'TRIG_MASK', 'rw'),
            (0x0014, 'WAVE_COUNT', 'rw')
        ]
    ) for j in range(4)
]
