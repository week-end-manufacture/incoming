import os
import shutil
from enum import Enum, unique, auto

from incoming.ic_filehandler import *


class PostProcessing:
    def __init__(self, icfile) -> None:
        self.icfile: IcFile = icfile

        self.ic_logger_instance = IcLogger()
        self.ic_logger = self.ic_logger_instance.init_logger(__name__)

    def ic_unlink(self, option=0):
        src_path = self.icfile.src_path
        src_abs_path = os.path.join(self.icfile.src_path, self.icfile.filename)

        if (self.icfile.ictype == IcType.UNZIPPED and self.icfile.icexttype == IcType.DIRECTORY):
            shutil.rmtree(src_path)

            self.icfile.ictype = IcType.DELETED

        if (option == 1):
            if (self.icfile.ictype == IcType.OUTGOING):
                if (os.path.isfile(src_abs_path)):
                    os.unlink(src_abs_path)
                
                if (os.path.isdir(src_path)):
                    if (len(os.listdir(src_path)) == 0):
                        os.rmdir(src_path)

                self.icfile.ictype = IcType.DELETED

        return self.icfile

    def ic_copy(self, option=0):
        src_file_abs_path = os.path.join(self.icfile.src_path, self.icfile.filename)
        dst_file_abs_path = os.path.join(self.icfile.dst_path, self.icfile.filename)
        dst_file_path = self.icfile.dst_path

        if (self.icfile.ictype == IcType.INCOMING):
            if not os.path.exists(dst_file_path):
                os.makedirs(dst_file_path)

            shutil.copy(src_file_abs_path, dst_file_abs_path)

            self.icfile.ictype = IcType.OUTGOING

            return self.icfile
        
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
