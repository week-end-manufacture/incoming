import json
import math
import os
import zipfile
import rarfile
import py7zr

from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum, unique, auto
from PIL import Image

from ic_log import *


class PreProcessing:
    def __init__(self) -> None:
        self.ic_logger_instance = IcLogger()
        self.ic_logger = self.ic_logger_instance.init_logger(__name__)

    def open_ic_settings(self):
        home_path = os.path.expanduser('~')
        ic_set_path = os.path.join(home_path, '.config/incoming/settings.json')
        with open(ic_set_path, 'r') as json_file:
            iset = json.load(json_file)
        return iset

    def open_ic_default_preset(self, default_preset_path):
        home_path = os.path.expanduser('~')
        with open(os.path.join(home_path, default_preset_path), 'r') as json_file:
            ipre = json.load(json_file)
        return ipre
    
    def open_ic_user_preset(self, user_preset):
        home_path = os.path.expanduser('~')
        with open(os.path.join(home_path, '.config/incoming/preset/' + user_preset + '.json'), 'r') as json_file:
            ipre = json.load(json_file)
        return ipre
        
    def extract_if_contains_images(self,
                                   abs_path,
                                   src_path,
                                   basename,
                                   archive_type,
                                   filtered_image_ext_dict):
        image_count = 0

        if archive_type == '.zip':
            with zipfile.ZipFile(abs_path, 'r') as archive:
                for file in archive.namelist():
                    cur_ext = Path(file).suffix

                    if (cur_ext in filtered_image_ext_dict):
                        image_count += 1
        elif archive_type == '.rar':
            with rarfile.RarFile(abs_path, 'r') as archive:
                for f in archive.infolist():
                    cur_ext = Path(f.filename).suffix
                    
                    if (cur_ext in filtered_image_ext_dict):
                        image_count += 1
        elif archive_type == '.7z':
            with py7zr.SevenZipFile(abs_path, mode='r') as archive:
                for file in archive.getnames():
                    cur_ext = Path(file).suffix
                    
                    if (cur_ext in filtered_image_ext_dict):
                        image_count += 1

        if image_count >= 2:
            tmp_path = src_path

            if not os.path.exists(tmp_path):
                os.makedirs(tmp_path)

            if archive_type == '.zip':
                dst_path = os.path.join(tmp_path, Path(basename).stem + '_zip')
                if not os.path.exists(dst_path):
                    os.makedirs(dst_path)

                with zipfile.ZipFile(abs_path, 'r') as archive:
                    archive.extractall(dst_path)
            elif archive_type == '.rar':
                dst_path = os.path.join(tmp_path, Path(basename).stem + '_rar')
                if not os.path.exists(dst_path):
                    os.makedirs(dst_path)

                with rarfile.RarFile(abs_path, 'r') as archive:
                    archive.extractall(dst_path)
            elif archive_type == '.7z':
                dst_path = os.path.join(tmp_path, Path(basename).stem + '_7z')
                if not os.path.exists(dst_path):
                    os.makedirs(dst_path)

                with py7zr.SevenZipFile(abs_path, mode='r') as archive:
                    archive.extractall(dst_path)

            self.ic_logger.info("OK EXTRACT ARCHIVE FILE")

            return True
        else:
            self.ic_logger.info("UNDER IMAGE FILE COUNT IN ARCHIVE")

            return False

    def ic_unzipper(self,
                    src_dir_path,
                    filtered_image_ext_dict,
                    filtered_archive_ext_dict):
        retval = []

        for (src_path, src_dir, src_filelist) in os.walk(src_dir_path):
            for (idx, src_file) in enumerate(src_filelist):
                abs_path = src_path + '/' + src_file
                cur_basename = os.path.basename(src_file)
                cur_ext = Path(src_file).suffix.lower()

                if (cur_ext in filtered_archive_ext_dict):
                    if (self.extract_if_contains_images(abs_path, src_path, cur_basename, cur_ext, filtered_image_ext_dict)):
                        retval.append(abs_path)

        return retval

    def ic_search(self,
                  src_dir_path,
                  dst_dir_path,
                  filtered_video_ext_dict,
                  filtered_image_ext_dict,
                  filtered_archive_ext_dict):
        src_icfilelist = []
        unzipped_filelist = []

        if (os.path.isfile(src_dir_path)):
            src_abs_path = os.path.abspath(src_dir_path)
            src_abs_dir_path = os.path.dirname(src_abs_path)
            src_file = os.path.basename(src_abs_path)
            cur_ext = Path(src_dir_path).suffix.lower()
            cur_size = os.path.getsize(src_abs_path)
            rel_path = '/'
            cur_dst_path = os.path.join(os.path.abspath(dst_dir_path), rel_path[1:])

            print(src_file)

            if (cur_ext in filtered_video_ext_dict):
                src_icfilelist.append(IcFile(src_abs_dir_path,
                                                cur_dst_path,
                                                src_file,
                                                cur_ext,
                                                IcType.INCOMING,
                                                IcType.VIDEO,
                                                cur_size))
            elif (cur_ext in filtered_image_ext_dict):
                src_icfilelist.append(IcFile(src_abs_dir_path,
                                                cur_dst_path,
                                                src_file,
                                                cur_ext,
                                                IcType.INCOMING,
                                                IcType.IMAGE,
                                                cur_size))
            else:
                return False
            return src_icfilelist

        unzipped_filelist = self.ic_unzipper(src_dir_path, filtered_image_ext_dict, filtered_archive_ext_dict)

        if (src_dir_path == dst_dir_path):
            dst_dir_path = os.path.join(os.path.dirname(src_dir_path), "[IC]" + os.path.basename(src_dir_path))

            if not os.path.exists(dst_dir_path):
                os.makedirs(dst_dir_path)

        for (src_path, src_dir, src_filelist) in os.walk(src_dir_path):
                for (idx, src_file) in enumerate(src_filelist):
                    src_abs_path = src_path + '/' + src_file
                    cur_ext = Path(src_file).suffix.lower()
                    cur_size = os.path.getsize(src_abs_path)
                    rel_path = src_path.replace(src_dir_path, '')
                    cur_dst_path = os.path.join(dst_dir_path, rel_path[1:])

                    self.ic_logger.debug("=IC SEARCHING...===================")
                    self.ic_logger.debug("PATH: %s" % src_path)
                    self.ic_logger.debug("DIRECTORY: %s" % src_dir)
                    self.ic_logger.debug("FILENAME: %s" % src_file)
                    self.ic_logger.debug("EXTENSION: %s" % cur_ext)
                    self.ic_logger.debug("SIZE: %d" % cur_size)
                    self.ic_logger.debug("===================================")

                    if (cur_ext in filtered_video_ext_dict):
                        src_icfilelist.append(IcFile(src_path,
                                                     cur_dst_path,
                                                     src_file,
                                                     cur_ext,
                                                     IcType.INCOMING,
                                                     IcType.VIDEO,
                                                     cur_size))
                    elif (cur_ext in filtered_image_ext_dict):
                        src_icfilelist.append(IcFile(src_path,
                                                     cur_dst_path,
                                                     src_file,
                                                     cur_ext,
                                                     IcType.INCOMING,
                                                     IcType.IMAGE,
                                                     cur_size))
                    elif (cur_ext in filtered_archive_ext_dict):
                        if (src_abs_path in unzipped_filelist):
                            src_icfilelist.append(IcFile(src_path,
                                                     cur_dst_path,
                                                     src_file,
                                                     cur_ext,
                                                     IcType.UNZIPPED,
                                                     IcType.ARCHIVE,
                                                     cur_size))
                        else:
                            src_icfilelist.append(IcFile(src_path,
                                                        cur_dst_path,
                                                        src_file,
                                                        cur_ext,
                                                        IcType.INCOMING,
                                                        IcType.ARCHIVE,
                                                        cur_size))
                    else:
                        src_icfilelist.append(IcFile(src_path,
                                                     cur_dst_path,
                                                     src_file,
                                                     cur_ext,
                                                     IcType.INCOMING,
                                                     IcType.NOT_FILTERED,
                                                     cur_size))
                        
        return src_icfilelist
    
    def print_all_icfile(self, icfile_list):
        for (idx, icfile) in enumerate(icfile_list):
            self.ic_logger.info("===================================")
            self.ic_logger.info("=ICFILE======================")
            self.ic_logger.info("SRC PATH: %s" % icfile.src_path)
            self.ic_logger.info("DST PATH: %s" % icfile.dst_path)
            self.ic_logger.info("FILENAME: %s" % icfile.filename)
            self.ic_logger.info("EXTENSION: %s" % icfile.extension)
            self.ic_logger.info("SIZE: %s" % self.convert_size(icfile.size))
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
                self.ic_logger.info("SIZE: %s" % self.convert_size(icfile.size))
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
                self.ic_logger.info("SIZE: %s" % self.convert_size(icfile.size))
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
                self.ic_logger.info("SIZE: %s" % self.convert_size(icfile.size))
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
                self.ic_logger.info("SIZE: %s" % self.convert_size(icfile.size))
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
                self.ic_logger.info("SIZE: %s" % self.convert_size(icfile.size))
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
    
    def create_dummy_icfilelist(self,
                                icfile_list):
        dummy = "ic-dummy"

        for (idx, icfile) in enumerate(icfile_list):
            if (icfile.ictype == IcType.INCOMING):
                if not os.path.exists(icfile.dst_path):
                    os.makedirs(icfile.dst_path)

                dst_icfile = open(os.path.join(icfile.dst_path, icfile.filename), "w")
                len = dst_icfile.write(dummy)
                dst_icfile.close()

                dst_icfile.ictype = IcType.DUMMY

@unique
class IcType(Enum):
    VIDEO = auto()
    IMAGE = auto()
    ARCHIVE = auto()
    NOT_FILTERED = auto()
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
    size: int
