import json
import math
from dataclasses import dataclass, field
from enum import Enum, unique


class PreProcessing:
    def __init__(self) -> None:
        pass

    def open_ic_settings(self):
        with open('./config/ic_settings.json', 'r') as json_file:
            iset = json.load(json_file)
        return iset

    def open_ic_preset(self):
        with open('./config/ic-preset/ic_preset.json', 'r') as json_file:
            iset = json.load(json_file)
        return iset
    
    def print_video_icfile(self, icfile_list):
        for (idx, icfile) in enumerate(icfile_list):
            if (icfile.icexttype == IcType.VIDEO):
                print("===================================")
                print("=VIDEO ICFILE======================")
                print("ABSOLUTE PATH: %s" % icfile.abs_path)
                print("RELATIVE PATH: %s" % icfile.rel_path)
                print("FILENAME: %s" % icfile.filename)
                print("EXTENSION: %s" % icfile.extension)
                print("SIZE: %s" % self.convert_size(icfile.size))
                print("===================================")

    def print_image_icfile(self, icfile_list):
        for (idx, icfile) in enumerate(icfile_list):
            if (icfile.icexttype == IcType.IMAGE):
                print("===================================")
                print("=IMAGE ICFILE======================")
                print("ABSOLUTE PATH: %s" % icfile.abs_path)
                print("RELATIVE PATH: %s" % icfile.rel_path)
                print("FILENAME: %s" % icfile.filename)
                print("EXTENSION: %s" % icfile.extension)
                print("SIZE: %s" % self.convert_size(icfile.size))
                print("===================================")

    def print_archive_icfile(self, icfile_list):
        for (idx, icfile) in enumerate(icfile_list):
            if (icfile.icexttype == IcType.ARCHIVE):
                print("===================================")
                print("=ARCHIVE ICFILE======================")
                print("ABSOLUTE PATH: %s" % icfile.abs_path)
                print("RELATIVE PATH: %s" % icfile.rel_path)
                print("FILENAME: %s" % icfile.filename)
                print("EXTENSION: %s" % icfile.extension)
                print("SIZE: %s" % self.convert_size(icfile.size))
                print("===================================")

    def get_video_icfile(self, icfile_list):
        retval = []

        for (idx, icfile) in enumerate(icfile_list):
            if (icfile.icexttype == IcType.VIDEO):
                retval.append(icfile)

        return retval
    
    def get_image_icfile(self, icfile_list):
        retval = []

        for (idx, icfile) in enumerate(icfile_list):
            if (icfile.icexttype == IcType.IMAGE):
                retval.append(icfile)  

        return retval
    
    def get_archive_icfile(self, icfile_list):
        retval = []

        for (idx, icfile) in enumerate(icfile_list):
            if (icfile.icexttype == IcType.ARCHIVE):
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
    VIDEO = 1
    IMAGE = 2
    ARCHIVE = 3
    INCOMING = 4
    OUTGOING = 5


@dataclass
class IcFile:
    abs_path: str
    rel_path: str
    filename: str
    extension: str
    ictype: IcType
    icexttype: IcType
    size: int
