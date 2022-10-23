import logging

from data import config


DATE_FORMAT = '%Y.%m.%d %H:%M:%S'
LOG_FORMAT = '%(asctime)s %(levelname)s: %(message)s (%(module)s:%(lineno)d) %(threadName)s'
LOG_FORMATTER = logging.Formatter(fmt=LOG_FORMAT,datefmt=DATE_FORMAT)


def get_level(level_name: str) -> int:
    """Возвращает уровень логгирования."""
    level_name = level_name.upper() if isinstance(level_name, str) else level_name
    return config.NAME_TO_LEVEL.get(level_name, logging.INFO)


def get_logger(logger_name: str) -> logging.Logger:
    """Возвращает логгер с указанным именем."""
    logger = logging.getLogger(logger_name)
    level = get_level(config.LEVEL)
    logger.setLevel(level)

    if config.LOG_TO_FILE:
        file_level = get_level(config.FILE_LEVEL)
        log_file = f'{config.FILE_PATH}{config.FILE_NAME}'
        log_file_handler = logging.FileHandler(log_file, encoding='utf-8')
        log_file_handler.setFormatter(LOG_FORMATTER)
        log_file_handler.setLevel(file_level)
        logger.addHandler(log_file_handler)

    log_stream_handler = logging.StreamHandler()
    log_stream_handler.setFormatter(LOG_FORMATTER)
    logger.addHandler(log_stream_handler)

    return logger
