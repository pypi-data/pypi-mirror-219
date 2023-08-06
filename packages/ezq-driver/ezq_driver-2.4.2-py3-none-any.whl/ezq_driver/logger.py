# coding: utf-8
import logging
from pathlib import Path
from logging import handlers


def get_logger(log_dir, namespace='', console=True):
    '''Get a logger instance.'''
    logger = logging.getLogger(namespace)
    logger.handlers = []  # remove previous handlers in the namespace
    logger.setLevel(logging.DEBUG)  # root logger
    logger.propagate = False

    level = logging.INFO
    log_format = '%(asctime)s.%(msecs)03d [%(name)s][%(levelname)s][%(funcName)s] %(message)s'
    time_format = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(log_format, time_format)

    if console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    if not namespace:
        namespace = 'unnamed_logger'
    log_dir_path = Path(log_dir)
    if not log_dir_path.exists():
        log_dir_path.mkdir()
    file_path = Path(log_dir) / f'{namespace}.log'
    file_handler = handlers.TimedRotatingFileHandler(filename=file_path, interval=1, when='d')
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.info('===== Log file path: %s =====', file_path)
    return logger
