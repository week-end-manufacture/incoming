import os
import shutil
from enum import Enum, unique, auto

from .ic_filehandler import *


class Result:
    def __init__(self) -> None:
        self.ic_logger_instance = IcLogger()
        self.ic_logger = self.ic_logger_instance.init_logger(__name__)
        
    def convert_size(self, size_bytes):
        if size_bytes == 0:
            return "0B"
        
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)

        return "%s %s" % (s, size_name[i])
        
    def ic_result(self, icfilelist, option=0):
        incoming_tot_size = 0
        outgoing_tot_size = 0

        for (idx, icfile) in enumerate(icfilelist):
            incoming_tot_size += icfile.incoming_size
            outgoing_tot_size += icfile.outgoing_size

        self.ic_logger.info("=IC END OF PROGRAM=================")
        self.ic_logger.info("=RESULT============================")
        self.ic_logger.info("=INCOMING SIZE:[%s]================" % self.convert_size(incoming_tot_size))
        self.ic_logger.info("=OUTGOING SIZE:[%s]================" % self.convert_size(outgoing_tot_size))
        self.ic_logger.info("===================================")
