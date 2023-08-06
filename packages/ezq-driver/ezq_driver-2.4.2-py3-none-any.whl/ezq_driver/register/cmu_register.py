# coding: utf-8
_CMU_REGISTER_TABLE = [
    dict(
        name='CPU',
        base_addr=0X010000,
        registers=[
            (0x0000, 'IDNTITY', 'r'),
            (0x0004, 'FIX_DATE', 'r'),
            (0x0008, 'RESERVE', 'r'),
            (0x000C, 'TESTREG', 'rw'),
            (0x0010, 'PERMISSION', 'rw'),
            (0x0014, 'BOARD_ID', 'r'),
            (0x0018, 'OP_TIME', 'r'),
            (0x001C, 'OP_STATUS', 'r'),
            (0x0020, 'FUNCTION', 'rw'),
            (0x0024, 'EZQ_RESET', 'rw'),
            (0x0028, 'LOAD_CONFIG', 'r'),
            (0x002C, 'DATA_LEN', 'rw'),
            (0x0030, 'FLASH_ADDR', 'rw'),
            (0x0034, 'DDR_ADDR', 'rw'),
            (0x0038, 'EMMC_ADDR', 'rw'),
            (0x003C, 'TDEST', 'rw'),
            (0x0040, 'HARDWARE_RDY', 'r'),
            (0x0044, 'STATUS_EN', 'rw'),
            (0x0050, 'MONITOR_IP', 'rw'),
            (0x0054, 'MONITOR_PORT', 'rw'),
            (0x005C, 'EZQ_STATUS', 'r')
        ]
    ),
    dict(
        name='UDP',
        base_addr=0x020000,
        registers=[
            (0x0000, 'IDNTITY', 'r'),
            (0x0004, 'FIX_DATE', 'r'),
            (0x0008, 'RESERVE', 'r'),
            (0x000C, 'TESTREG', 'rw'),
            (0x0080, 'LOCAL_MAC_H_A', 'r'),
            (0x0084, 'LOCAL_MAC_L_A', 'r'),
            (0x0088, 'LOCAL_IP_A', 'r'),
            (0x00C0, 'LOCAL_MAC_H_B', 'r'),
            (0x00C4, 'LOCAL_MAC_L_B', 'r'),
            (0x00C8, 'LOCAL_IP_B', 'r'),
            (0x0100, 'LOCAL_MAC_H_C', 'r'),
            (0x0104, 'LOCAL_MAC_L_C', 'r'),
            (0x0108, 'LOCAL_IP_C', 'r'),
            (0x0140, 'LOCAL_MAC_H_D', 'r'),
            (0x0144, 'LOCAL_MAC_L_D', 'r'),
            (0x0148, 'LOCAL_IP_D', 'r'),
            (0x008C, 'GATEWAY_IP', 'r'),
            (0x0090, 'SUBNET_MASK', 'r'),
            (0x0094, 'LOCAL_PORT', 'r'),
            (0x0200, 'STATUS', 'r')
        ]
    ),
    dict(
        name='FUNC',
        base_addr=0x030000,
        registers=[
            (0x0000, 'IDNTITY', 'r'),
            (0x0004, 'FIX_DATE', 'r'),
            (0x0008, 'RESERVE', 'r'),
            (0x000C, 'TESTREG', 'rw'),
            (0x0014, 'POWER_CTRL', 'rw'),
            (0x0018, 'CAS_CLK_SEL', 'rw'),
            (0x001C, 'REF_CLK_SEL', 'rw'),
            (0x0028, 'FAN_CTRL1', 'rw'),
            (0x002C, 'FAN_CTRL2', 'rw'),
            (0x0030, 'SLOT_MONITOR', 'r'),
            (0x0034, 'GTH_CHANNEL_UP', 'r'),
            (0x0038, 'GTH_LANE_UP', 'r'),
            (0x003C, 'GTH_HARD_ERR', 'r'),
            (0x0040, 'GTH_SOFT_ERR', 'r'),
            (0x0044, 'GTH_RESET', 'rw'),
            (0x0048, 'TEMP_CONTROL', 'rw'),
            (0x004C, 'SLOT_POWER_MONITOR', 'r')
        ]
    )
]
