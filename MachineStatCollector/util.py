import logging
import config


def set_up_logging(logger_name, loggers=[]):
    if len(loggers):
        logger = loggers[0]
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
        )
        fileh = logging.FileHandler(config.get("system", "log_file"))
        fileh.setFormatter(formatter)

        logger = logging.getLogger(logger_name)
        logger.addHandler(fileh)
        logger.setLevel(logging.DEBUG)
        loggers.append(logger)
    return logger
