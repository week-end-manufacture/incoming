import math
import sys
import time

from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum, unique, auto

from incoming.ic_log import ic_logger_instance_ic_filehandler


class IcFileHandler:
    def __init__(self) -> None:
        self.ic_logger = ic_logger_instance_ic_filehandler.logger

    def logging_icfile(self, icfile_list, ictype=None):
        if (ictype == None):
            for (idx, icfile) in enumerate(icfile_list):
                self.ic_logger.info(f"{icfile.src_path}\
                                    |{icfile.dst_path}\
                                    |{icfile.filename}\
                                    |{icfile.extension}|\
                                    |{icfile.ictype}\
                                    |{icfile.icexttype}\
                                    |{icfile.icexttype}\
                                    |{icfile.incoming_size}\
                                    |{self.convert_size(icfile.outgoing_size)}")
        else:
            for (idx, icfile) in enumerate(icfile_list):
                if (icfile.icexttype == ictype):
                    self.ic_logger.info(f"{icfile.src_path}\
                                        |{icfile.dst_path}\
                                        |{icfile.filename}\
                                        |{icfile.extension}|\
                                        |{icfile.ictype}\
                                        |{icfile.icexttype}\
                                        |{icfile.icexttype}\
                                        |{icfile.incoming_size}\
                                        |{self.convert_size(icfile.outgoing_size)}")

    def is_video_icfile(self, icfile):
        if (icfile.icexttype == IcType.VIDEO):
            return True
        else:
            return False
        
    def is_image_icfile(self, icfile):
        if (icfile.icexttype == IcType.IMAGE):
            return True
        else:
            return False
        
    def is_archive_icfile(self, icfile):
        if (icfile.icexttype == IcType.ARCHIVE):
            return True
        else:
            return False
        
    def is_not_filtered_icfile(self, icfile):
        if (icfile.icexttype == IcType.NOT_FILTERED):
            return True
        else:
            return False
        
    def is_incoming_icfile(self, icfile):
        if (icfile.ictype == IcType.INCOMING):
            return True
        else:
            return False
        
    def is_outgoing_icfile(self, icfile):
        if (icfile.ictype == IcType.OUTGOING):
            return True
        else:
            return False
        
    def is_deleted_icfile(self, icfile):
        if (icfile.ictype == IcType.DELETED):
            return True
        else:
            return False
    
    def is_dummy_icfile(self, icfile):
        if (icfile.ictype == IcType.DUMMY):
            return True
        else:
            return False

    def get_video_icfilelist(self, icfile_list):
        retval = []

        for (idx, icfile) in enumerate(icfile_list):
            if (icfile.icexttype == IcType.VIDEO):
                retval.append(icfile)

        return retval
    
    def get_image_icfilelist(self, icfile_list):
        retval = []

        for (idx, icfile) in enumerate(icfile_list):
            if (icfile.icexttype == IcType.IMAGE):
                retval.append(icfile)  

        return retval
    

    def get_archive_icfilelist(self, icfile_list):
        retval = []

        for (idx, icfile) in enumerate(icfile_list):
            if (icfile.icexttype == IcType.ARCHIVE):
                retval.append(icfile)  

        return retval
    
    def get_not_filtered_icfilelist(self, icfile_list):
        retval = []

        for (idx, icfile) in enumerate(icfile_list):
            if (icfile.icexttype == IcType.NOT_FILTERED):
                retval.append(icfile)  

        return retval
    
    def convert_size(self, size_bytes):
        if size_bytes == 0:
            return "0B"
        
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)

        return "%s %s" % (s, size_name[i])


@unique
class IcType(Enum):
    VIDEO = auto()
    IMAGE = auto()
    ARCHIVE = auto()
    NOT_FILTERED = auto()
    DIRECTORY = auto()
    INCOMING = auto()
    OUTGOING = auto()
    UNZIPPED = auto()
    DELETED = auto()
    DUMMY = auto()


@dataclass
class IcFile:
    src_path: str
    dst_path: str
    filename: str
    extension: str
    ictype: IcType
    icexttype: IcType
    incoming_size: int
    outgoing_size: int
    