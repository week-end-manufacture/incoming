import json
import math
import os
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum, unique, auto


class PreProcessing:
    def __init__(self) -> None:
        pass

    def open_ic_settings(self):
        with open('./config/ic_settings.json', 'r') as json_file:
            iset = json.load(json_file)
        return iset

    def open_ic_default_preset(self):
        with open('./config/ic-preset/ic_preset.json', 'r') as json_file:
            iset = json.load(json_file)
        return iset
    
    def open_ic_preset(self, user_preset):
        with open('./config/ic-preset/' + user_preset + '.json', 'r') as json_file:
            iset = json.load(json_file)
        return iset
    
    def ic_serach(self,
                  src_dir_path,
                  filtered_video_ext_dict,
                  filtered_image_ext_dict,
                  filtered_archive_ext_dict):
        src_icfilelist = []

        for (src_path, src_dir, src_filelist) in os.walk(src_dir_path):
                for (idx, src_file) in enumerate(src_filelist):
                    abs_path = src_path + '/' + src_file
                    cur_ext = Path(src_file).suffix
                    cur_size = os.path.getsize(abs_path)
                    rel_path = src_path.replace(src_dir_path, '')

                    print("===================================")
                    print("PATH: %s" % src_path)
                    print("DIRECTORY: %s" % src_dir)
                    print("FILENAME: %s" % src_file)
                    print("EXTENSION: %s" % cur_ext)
                    print("SIZE: %d" % cur_size)
                    print("===================================")

                    if (cur_ext in filtered_video_ext_dict):
                        src_icfilelist.append(IcFile(src_path,
                                                     rel_path,
                                                     src_file,
                                                     cur_ext,
                                                     IcType.INCOMING,
                                                     IcType.VIDEO,
                                                     cur_size))
                    elif (cur_ext in filtered_image_ext_dict):
                        src_icfilelist.append(IcFile(src_path,
                                                     rel_path,
                                                     src_file,
                                                     cur_ext,
                                                     IcType.INCOMING,
                                                     IcType.IMAGE,
                                                     cur_size))
                    elif (cur_ext in filtered_archive_ext_dict):
                        src_icfilelist.append(IcFile(src_path,
                                                     rel_path,
                                                     src_file,
                                                     cur_ext,
                                                     IcType.INCOMING,
                                                     IcType.ARCHIVE,
                                                     cur_size))
                    else:
                        src_icfilelist.append(IcFile(src_path,
                                                     rel_path,
                                                     src_file,
                                                     cur_ext,
                                                     IcType.INCOMING,
                                                     IcType.NOT_FILTERED,
                                                     cur_size))
                        
        return src_icfilelist
    
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
                print("=ARCHIVE ICFILE====================")
                print("ABSOLUTE PATH: %s" % icfile.abs_path)
                print("RELATIVE PATH: %s" % icfile.rel_path)
                print("FILENAME: %s" % icfile.filename)
                print("EXTENSION: %s" % icfile.extension)
                print("SIZE: %s" % self.convert_size(icfile.size))
                print("===================================")

    def print_not_filtered_icfile(self, icfile_list):
        for (idx, icfile) in enumerate(icfile_list):
            if (icfile.icexttype == IcType.NOT_FILTERED):
                print("===================================")
                print("=NOT FILTERED ICFILE================")
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
    
    def get_not_filtered_icfile(self, icfile_list):
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
    INCOMING = auto()
    OUTGOING = auto()


@dataclass
class IcFile:
    abs_path: str
    rel_path: str
    filename: str
    extension: str
    ictype: IcType
    icexttype: IcType
    size: int
