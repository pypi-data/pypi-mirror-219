import logging


def get_level_name(level: int, /):
    return logging._levelToName[level]
