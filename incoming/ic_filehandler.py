import math

from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum, unique, auto

from incoming.ic_log import *


class IcFileHandler:
    def __init__(self) -> None:
        self.ic_logger_instance = IcLogger(__name__)
        self.ic_logger = self.ic_logger_instance.logger

    def print_all_icfile(self, icfile_list):
        for (idx, icfile) in enumerate(icfile_list):
            self.ic_logger.info("===================================")
            self.ic_logger.info("=ICFILE======================")
            self.ic_logger.info("SRC PATH: %s" % icfile.src_path)
            self.ic_logger.info("DST PATH: %s" % icfile.dst_path)
            self.ic_logger.info("FILENAME: %s" % icfile.filename)
            self.ic_logger.info("EXTENSION: %s" % icfile.extension)
            self.ic_logger.info("IC TYPE: %s" % icfile.ictype)
            self.ic_logger.info("IC EXTENTION TYPE: %s" % icfile.icexttype)
            self.ic_logger.info("INCOMING SIZE: %s" % self.convert_size(icfile.incoming_size))
            self.ic_logger.info("OUTGOING SIZE: %s" % self.convert_size(icfile.outgoing_size))
            self.ic_logger.info("===================================")

    def print_video_icfile(self, icfile_list):
        for (idx, icfile) in enumerate(icfile_list):
            if (icfile.icexttype == IcType.VIDEO):
                self.ic_logger.info("===================================")
                self.ic_logger.info("=VIDEO ICFILE======================")
                self.ic_logger.info("SRC PATH: %s" % icfile.src_path)
                self.ic_logger.info("DST PATH: %s" % icfile.dst_path)
                self.ic_logger.info("FILENAME: %s" % icfile.filename)
                self.ic_logger.info("EXTENSION: %s" % icfile.extension)
                self.ic_logger.info("INCOMING SIZE: %s" % self.convert_size(icfile.incoming_size))
                self.ic_logger.info("OUTGOING SIZE: %s" % self.convert_size(icfile.outgoing_size))
                self.ic_logger.info("===================================")

    def print_image_icfile(self, icfile_list):
        for (idx, icfile) in enumerate(icfile_list):
            if (icfile.icexttype == IcType.IMAGE):
                self.ic_logger.info("===================================")
                self.ic_logger.info("=IMAGE ICFILE======================")
                self.ic_logger.info("SRC PATH: %s" % icfile.src_path)
                self.ic_logger.info("DST PATH: %s" % icfile.dst_path)
                self.ic_logger.info("FILENAME: %s" % icfile.filename)
                self.ic_logger.info("EXTENSION: %s" % icfile.extension)
                self.ic_logger.info("INCOMING SIZE: %s" % self.convert_size(icfile.incoming_size))
                self.ic_logger.info("OUTGOING SIZE: %s" % self.convert_size(icfile.outgoing_size))
                self.ic_logger.info("===================================")

    def print_archive_icfile(self, icfile_list):
        for (idx, icfile) in enumerate(icfile_list):
            if (icfile.icexttype == IcType.ARCHIVE):
                self.ic_logger.info("===================================")
                self.ic_logger.info("=ARCHIVE ICFILE====================")
                self.ic_logger.info("SRC PATH: %s" % icfile.src_path)
                self.ic_logger.info("DST PATH: %s" % icfile.dst_path)
                self.ic_logger.info("FILENAME: %s" % icfile.filename)
                self.ic_logger.info("EXTENSION: %s" % icfile.extension)
                self.ic_logger.info("INCOMING SIZE: %s" % self.convert_size(icfile.incoming_size))
                self.ic_logger.info("OUTGOING SIZE: %s" % self.convert_size(icfile.outgoing_size))
                self.ic_logger.info("===================================")

    def print_unzipped_icfile(self, icfile_list):
        for (idx, icfile) in enumerate(icfile_list):
            if (icfile.icexttype == IcType.UNZIPPED):
                self.ic_logger.info("===================================")
                self.ic_logger.info("=UNZIPPED ICFILE===================")
                self.ic_logger.info("SRC PATH: %s" % icfile.src_path)
                self.ic_logger.info("DST PATH: %s" % icfile.dst_path)
                self.ic_logger.info("FILENAME: %s" % icfile.filename)
                self.ic_logger.info("EXTENSION: %s" % icfile.extension)
                self.ic_logger.info("INCOMING SIZE: %s" % self.convert_size(icfile.incoming_size))
                self.ic_logger.info("OUTGOING SIZE: %s" % self.convert_size(icfile.outgoing_size))
                self.ic_logger.info("===================================")

    def print_not_filtered_icfile(self, icfile_list):
        for (idx, icfile) in enumerate(icfile_list):
            if (icfile.icexttype == IcType.NOT_FILTERED):
                self.ic_logger.info("===================================")
                self.ic_logger.info("=NOT FILTERED ICFILE================")
                self.ic_logger.info("SRC PATH: %s" % icfile.src_path)
                self.ic_logger.info("DST PATH: %s" % icfile.dst_path)
                self.ic_logger.info("FILENAME: %s" % icfile.filename)
                self.ic_logger.info("EXTENSION: %s" % icfile.extension)
                self.ic_logger.info("INCOMING SIZE: %s" % self.convert_size(icfile.incoming_size))
                self.ic_logger.info("OUTGOING SIZE: %s" % self.convert_size(icfile.outgoing_size))
                self.ic_logger.info("===================================")

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
    