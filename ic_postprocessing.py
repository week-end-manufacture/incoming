import os

from ic_preprocessing import *


class PostProcessing:
    def __init__(self, icfile) -> None:
        self.icfile = icfile

        self.ic_logger_instance = IcLogger()
        self.ic_logger = self.ic_logger_instance.init_logger(__name__)

    def ic_unlink(self, icfile, option):
        src_abs_path = os.path.join(self.icfile.src_path, self.icfile.filename)

        os.unlink(src_abs_path)
        os.rmdir(self.icfile.src_path)