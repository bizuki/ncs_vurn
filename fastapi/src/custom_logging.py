import logging
import sys
from pathlib import Path
from loguru import logger
import yaml


# just inherit from the default StreamHandler and override the emit method
class InterceptHandler(logging.StreamHandler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

def _load_config(config_path: Path):
    with open(config_path) as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError as err:
            print(f'Could not parse the logging configuration at {config_path}')
            print(err)
            sys.exit(1)
    
    return config

def _customize_logging(
    filepath: Path,
    level: str,
    rotation: str,
    retention: str,
    format: str
): 
    logger.remove()
    
    # add stdout sink
    logger.add(
        sys.stdout,
        enqueue=True,
        backtrace=True,
        level=level.upper(),
        format=format,
    )

    # add file sink if specified
    if filepath:
        logger.add(
            str(filepath),
            rotation=rotation,
            retention=retention,
            enqueue=True,
            backtrace=True,
            level=level.upper(),
            format=format
        )
    
    # add interceptors to all the other loggers
    logging.basicConfig(handlers=[InterceptHandler()], level=0)
    logging.getLogger().handlers = [InterceptHandler()]
    
    # this is a very dirty hack, but it works!
    logging.StreamHandler = InterceptHandler # type: ignore

    for logger_name in logging.root.manager.loggerDict:
        l = logging.getLogger(logger_name)
        l.handlers = [InterceptHandler()]

    return logger.bind(request_id=None, method=None)

def create_logger(config_path: Path):
    config = _load_config(config_path)
    logger_config = config.get('logger')
    new_logger = _customize_logging(
        logger_config.get('path'),
        level=logger_config.get('level'),
        retention=logger_config.get('retention'),
        rotation=logger_config.get('rotation'),
        format=logger_config.get('format'),
    )

    return new_logger
