import os
import shutil
from enum import Enum, unique, auto

from ic_preprocessing import *


class PostProcessing:
    def __init__(self, icfile) -> None:
        self.icfile = icfile

        self.ic_logger_instance = IcLogger()
        self.ic_logger = self.ic_logger_instance.init_logger(__name__)

    def ic_unlink(self, option):
        src_path = self.icfile.src_path
        src_abs_path = os.path.join(self.icfile.src_path, self.icfile.filename)

        if (os.path.isfile(src_abs_path)):
            os.unlink(src_abs_path)
        
        if (os.path.isdir(src_path)):
            os.rmdir(src_path)

    def ic_copy(self, option):
        src_file_abs_path = os.path.join(self.icfile.src_path, self.icfile.filename)
        dst_file_abs_path = os.path.join(self.icfile.dst_path, self.icfile.filename)
        dst_file_path = self.icfile.dst_path

        if not os.path.exists(dst_file_path):
            os.makedirs(dst_file_path)

        shutil.copy(src_file_abs_path, dst_file_abs_path)