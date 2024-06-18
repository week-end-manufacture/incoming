import os
import argparse
from pathlib import Path

from incoming.ic_filehandler import *
from incoming.ic_preprocessing import *
from incoming.ic_log import *
from incoming.ic_image import *
from incoming.ic_video import *
from incoming.ic_postprocessing import *
from incoming.ic_result import *

def main():
    pre_processiong = PreProcessing()
    ic_logger_instance = IcLogger(__name__)
    ic_logger = ic_logger_instance.logger
    ic_filehandler = IcFileHandler()
    ic_settings = pre_processiong.open_ic_settings()


    src_dir_path = ic_settings["src_dir_path"]
    dst_dir_path = ic_settings["dst_dir_path"]
    incoming_version = "beta0.0.5"

    filtered_archive_ext_dict = [".zip", ".rar", ".7z"]

    ic_logger.debug("!!!START ICOMING PROGRAM!!!")

    """
        명령어 설정
    """
    parser = argparse.ArgumentParser(prog='incoming')
    parser.add_argument("-i", "--src_dir_path", help="Source directory path", action="store")
    parser.add_argument("-o", "--dst_dir_path", help="Destination directory path", action="store")
    parser.add_argument("-p", "--user_preset", help="User preset", action="store")
    parser.add_argument("-d", "--dummy", help="Create dummy file", action="store_true")
    parser.add_argument("-u", "--unlink", help="Unlink incoming file", action="store_true")
    parser.add_argument("-v", "--version", help="Version", action="version", version='%(prog)s ' + incoming_version)
    args = parser.parse_args()

    """
        MAIN LOGIC
    """
    if (args.src_dir_path != None and args.dst_dir_path != None):
        src_dir_path = args.src_dir_path
        dst_dir_path = args.dst_dir_path

    if (not os.path.exists(src_dir_path) or not os.path.exists(src_dir_path)):
        ic_logger.warning("INVALID PATH")

        return (-1)

    ic_logger.info("SRC_DIR_PATH:[%s]" % src_dir_path)
    ic_logger.info("DST_DIR_PATH:[%s]" % dst_dir_path)

    if (args.user_preset != None):
        ic_logger.info("!!!USER PRESET USE!!!")
        ic_logger.info("=IC PREPROCESSING START=")

        ic_preset = pre_processiong.open_ic_user_preset(args.user_preset)

        filtered_video_ext_dict = ic_preset["filterd_all_ext_dict"]["filtered_video_ext_dict"]
        filtered_image_ext_dict = ic_preset["filterd_all_ext_dict"]["filtered_image_ext_dict"]

        if (src_dir_path == dst_dir_path):
            ic_logger.info("!!!SAME PATH PROCEDURE ACTIVATE!!!")

            main_icfilelist = pre_processiong.ic_search(src_dir_path,
                                                    dst_dir_path,
                                                    filtered_video_ext_dict,
                                                    filtered_image_ext_dict,
                                                    filtered_archive_ext_dict)

            ic_logger.info("FILE LENGTH: %d" % len(main_icfilelist))

            ic_logger.info("=IC PREPROCESSING END=")
        else:
            ic_logger.info("!!!COPY CAT!!!")
            ic_logger.info("=IC PREPROCESSING START=")

            main_icfilelist = pre_processiong.ic_search(src_dir_path,
                                                    dst_dir_path,
                                                    filtered_video_ext_dict,
                                                    filtered_image_ext_dict,
                                                    filtered_archive_ext_dict)

            ic_logger.info("FILE LENGTH: %d" % len(main_icfilelist))

            ic_logger.info("=IC PREPROCESSING END=")

        """
            DUMMY OPTION CHECK
        """
        if (args.dummy):
            pre_processiong.create_dummy_icfilelist(main_icfilelist)

            return (True)

        """
            IC IMAGE PROCESS
        """
        ic_logger.info("=IC IMAGE PROCESS START=")

        for (idx, icfile) in enumerate(main_icfilelist):
            if (ic_filehandler.is_image_icfile(icfile)):
                ic_image_processor = ImageProcessor(icfile, ic_image_preset)

                icfile = ic_image_processor.ic_image_process()

        ic_logger.info("=IC IMAGE PROCESS END=")

        """
            IC VIDEO PROCESS
        """
        ic_logger.info("=IC VIDEO PROCESS START=")

        for (idx, icfile) in enumerate(main_icfilelist):
            if (ic_filehandler.is_video_icfile(icfile)):
                ic_video_processor = VideoProcessor(icfile, ic_video_preset)

                icfile = ic_video_processor.ic_video_process()

        ic_logger.info("=IC VIDEO PROCESS END=")
    else:
        """
            IC PREPROCESS
        """
        ic_logger.info("!!!DEFAULT PRESET USE!!!")
        ic_logger.info("=IC PREPROCESSING START=")

        ic_logger.info("SRC_DIR_PATH:[%s]" % src_dir_path)
        ic_logger.info("DST_DIR_PATH:[%s]" % dst_dir_path)

        """
            IC PRESET LOADING
        """
        ic_preset = pre_processiong.open_ic_default_preset(ic_settings["default_preset_path"])
        ic_image_preset = ic_preset["image_process"]
        ic_video_preset = ic_preset["video_process"]
        filtered_video_ext_dict = ic_preset["filterd_all_ext_dict"]["filtered_video_ext_dict"]
        filtered_image_ext_dict = ic_preset["filterd_all_ext_dict"]["filtered_image_ext_dict"]

        if (src_dir_path == dst_dir_path):
            ic_logger.info("!!!SAME PATH PROCEDURE ACTIVATE!!!")

            main_icfilelist = pre_processiong.ic_search(src_dir_path,
                                                    dst_dir_path,
                                                    filtered_video_ext_dict,
                                                    filtered_image_ext_dict,
                                                    filtered_archive_ext_dict)

        else:
            ic_logger.info("!!!COPY CAT!!!")

            main_icfilelist = pre_processiong.ic_search(src_dir_path,
                                                    dst_dir_path,
                                                    filtered_video_ext_dict,
                                                    filtered_image_ext_dict,
                                                    filtered_archive_ext_dict)

        ic_logger.info("FILE LENGTH: %d" % len(main_icfilelist))
        ic_filehandler.print_all_icfile(main_icfilelist)

        ic_logger.info("=IC PREPROCESSING END=")

        """
            DUMMY OPTION CHECK
        """
        if (args.dummy):
            pre_processiong.create_dummy_icfilelist(main_icfilelist)

            return (True)

        """
            IC IMAGE PROCESS
        """
        ic_logger.info("=IC IMAGE PROCESS START=")

        for (idx, icfile) in enumerate(main_icfilelist):
            if (ic_filehandler.is_image_icfile(icfile)):
                ic_image_processor = ImageProcessor(icfile, ic_image_preset)

                icfile = ic_image_processor.ic_image_process()

        ic_logger.info("=IC IMAGE PROCESS END=")

        """
            IC VIDEO PROCESS
        """
        ic_logger.info("=IC VIDEO PROCESS START=")

        for (idx, icfile) in enumerate(main_icfilelist):
            if (ic_filehandler.is_video_icfile(icfile)):
                ic_video_processor = VideoProcessor(icfile, ic_video_preset)

                icfile = ic_video_processor.ic_video_process()

        ic_logger.info("=IC VIDEO PROCESS END=")

        """
            IC POST PROCESS
        """
        ic_logger.info("=IC COPY PROCESS START=")

        for (idx, icfile) in enumerate(main_icfilelist):
            if (ic_filehandler.is_incoming_icfile(icfile)):
                ic_post_processor = PostProcessing(icfile)

                icfile = ic_post_processor.ic_copy()

                del ic_post_processor

        ic_logger.info("=IC COPY PROCESS END=")

        ic_logger.info("=IC UNLINK PROCESS START=")

        for (idx, icfile) in enumerate(main_icfilelist):
            ic_post_processor = PostProcessing(icfile)

            icfile = ic_post_processor.ic_unlink()

            del ic_post_processor

        ic_logger.info("=IC UNLINK PROCESS END=")

        """
            IC RESULT
        """
        ic_result = Result()

        ic_filehandler.print_all_icfile(main_icfilelist)
        ic_result.ic_result(main_icfilelist)

        return (True)


if __name__ == "__main__":
    main()
