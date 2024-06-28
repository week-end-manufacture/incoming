import os
import logging
import sys
import colorlog
from logging import handlers


class IcLogger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }

    def __init__(self,
                 filename,
                 level='info',
                 when='midnight',
                 backCount=7,):
        self.logger = logging.getLogger(filename)

        home_path = os.path.expanduser('~')
        self.filePath = os.path.join(home_path,".config/incoming/log/")

        if not os.path.exists(self.filePath):
            os.makedirs(self.filePath)

        streamFormatter = colorlog.ColoredFormatter(
            "%(log_color)s%(message)s",
            log_colors={
                'DEBUG':    'cyan',
                'INFO':     'white,bold',
                'INFOV':    'cyan,bold',
                'WARNING':  'yellow',
                'ERROR':    'red,bold',
                'CRITICAL': 'red,bg_white',
            }
        )
        
        fileFormatter = logging.Formatter(
            "[%(asctime)s|%(levelname)s|%(name)s|%(module)s|%(lineno)d]%(message)s"
        )

        #streamHandler = logging.StreamHandler()
        #streamHandler.setFormatter(streamFormatter)

        fileHandler = handlers.TimedRotatingFileHandler(
            os.path.abspath(f"{self.filePath}ic_log.log"),
            when=when,
            interval=1,
            backupCount=backCount,
            encoding='utf-8'
            )
        
        fileHandler.setFormatter(fileFormatter)
        
        #self.logger.addHandler(streamHandler)
        self.logger.addHandler(fileHandler)

        self.logger.setLevel(self.level_relations.get(level))


ic_logger_instance_main = IcLogger('main')
ic_logger_instance_ic_filehandler = IcLogger('ic_filehandler')
ic_logger_instance_ic_preprocessing = IcLogger('ic_preprocessing')
ic_logger_instance_ic_postprocessing = IcLogger('ic_postprocessing')
ic_logger_instance_ic_result = IcLogger('ic_result')
ic_logger_instance_ic_image = IcLogger('ic_image')
ic_logger_instance_ic_video = IcLogger('ic_video')
