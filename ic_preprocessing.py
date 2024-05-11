import json
from dataclasses import dataclass, field
from enum import Enum, unique


class PreProcessing:
    def __init__(self) -> None:
        pass

    def open_ic_settings(self):
        with open('./config/ic_settings.json', 'r') as json_file:
            iset = json.load(json_file)
        return iset

    def open_ic_default(self):
        with open('./config/ic-preset/ic_default.json', 'r') as json_file:
            iset = json.load(json_file)
        return iset
    
    def print_video_icfile(self, icfile_list):
        for (idx, icfile) in enumerate(icfile_list):
            if (icfile.ictype == IcType.VIDEO):
                print("===================================")
                print("=VIDEO ICFILE======================")
                print("PATH: %s" % icfile.path)
                print("FILENAME: %s" % icfile.filename)
                print("EXTENSION: %s" % icfile.extension)
                print("===================================")

    def print_image_icfile(self, icfile_list):
        for (idx, icfile) in enumerate(icfile_list):
            if (icfile.ictype == IcType.IMAGE):
                print("===================================")
                print("=IMAGE ICFILE======================")
                print("PATH: %s" % icfile.path)
                print("FILENAME: %s" % icfile.filename)
                print("EXTENSION: %s" % icfile.extension)
                print("===================================")

    def print_image_icfile(self, icfile_list):
        for (idx, icfile) in enumerate(icfile_list):
            if (icfile.ictype == IcType.ARCHIVE):
                print("===================================")
                print("=ARCHIVE ICFILE======================")
                print("PATH: %s" % icfile.path)
                print("FILENAME: %s" % icfile.filename)
                print("EXTENSION: %s" % icfile.extension)
                print("===================================")

    def get_video_icfile(self, icfile_list):
        retval = []

        for (idx, icfile) in enumerate(icfile_list):
            if (icfile.ictype == IcType.VIDEO):
                retval.append(icfile)  

        return retval
    
    def get_image_icfile(self, icfile_list):
        retval = []

        for (idx, icfile) in enumerate(icfile_list):
            if (icfile.ictype == IcType.IMAGE):
                retval.append(icfile)  

        return retval
    
    def get_archive_icfile(self, icfile_list):
        retval = []

        for (idx, icfile) in enumerate(icfile_list):
            if (icfile.ictype == IcType.ARCHIVE):
                retval.append(icfile)  

        return retval
    

@unique
class IcType(Enum):
    VIDEO = 1
    IMAGE = 2
    ARCHIVE = 3


@dataclass
class IcFile:
    path: str
    filename: str
    extension: str
    ictype: IcType
