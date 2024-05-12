import shutil
from enum import Enum

from ic_preprocessing import *
import ic_archive
import ic_image
import ic_video

def process_ic_file(ic_file: IcFile, rel_path: str):
    if ic_file.ictype == IcType.NOT_FILTERED:
        shutil.copy(ic_file.abs_path, rel_path)
#    elif ic_file.ictype == IcType.ARCHIVE:
#        ic_archive(ic_file)    
    elif ic_file.ictype == IcType.IMAGE:
        ic_image(ic_file)
#    elif ic_file.ictype == IcType.VIDEO:
#        ic_video(ic_file)
