_MIX_REGISTER_TABEL = [
    dict(
        name=f'MIX',
        base_addr=0x000000,
        registers=[
            (0x0000, 'FREQ', 'wr'),
            (0x0004, 'WORK_STATUS', 'r'),
        ]
    ),
    # 需要根据郭成给的另外一个混频版开发新的MIX2以及相应的驱动程序
    # MIX2为64位指令其中57-62位6bit槽位信息以全0表示，
    # 实际指令中将接收槽位信息并返回相应槽位信息
    dict(
        name=f'MIX2',
        base_addr=0x000000,
        registers=[
            (0x100000,'FREQ','rw'),
            (0xF00000,'TEMP','r')
        ] + [
            (0x200000 + (i+1) * 0x10000, f'PUMP_FREQ_{i+1}', 'rw') for i in range(4)
        ] + [
            (0x300000 + (i+1) * 0x10000, f'PUMP_POWER_{i+1}', 'rw') for i in range(4)
        ] + [
            (0x400000 + (i+1) * 0x10000, f'PUMP_ENABLE_{i+1}', 'rw') for i in range(4)
        ]
    ),
]
