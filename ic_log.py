import os
import logging
import sys
import colorlog
from logging import handlers


class IcLogger:
    def __init__(self, filePath=None):
        self.className = "IcLogger"
        
        if filePath is None:
            self.filePath = "./log/"

        if not os.path.exists(self.filePath):
            os.makedirs(self.filePath)

    def init_logger(self, logname):
        ic_logger = logging.getLogger(logname)

        streamFormatter = colorlog.ColoredFormatter(
            "%(log_color)s%(bg_blue)s%(message)s"
        )
        
        fileFormatter = logging.Formatter(
            "[%(asctime)s|%(levelname)s|<%(name)s>|%(module)s|%(lineno)d]%(message)s"
        )
        
        streamHandler = colorlog.StreamHandler(sys.stdout)

        fileHandler = handlers.TimedRotatingFileHandler(
            os.path.abspath(f"{self.filePath}ic_log.log"),
            when="midnight",
            interval=1,
            backupCount=14,
            encoding="utf-8",
        )
        
        streamHandler.setFormatter(streamFormatter)
        fileHandler.setFormatter(fileFormatter)

        ic_logger.addHandler(streamHandler)
        ic_logger.addHandler(fileHandler)

        ic_logger.setLevel(logging.DEBUG)

        return ic_logger
        