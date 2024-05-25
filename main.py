import os
import argparse
from pathlib import Path

from ic_preprocessing import *
from ic_log import *
from ic_image import *
from ic_video import *

def main():
    pre_processiong = PreProcessing()
    ic_logger_instance = IcLogger()
    ic_logger = ic_logger_instance.init_logger(__name__)
    ic_settings = pre_processiong.open_ic_settings()


    src_dir_path = ic_settings["src_dir_path"]
    dst_dir_path = ic_settings["dst_dir_path"]
    incoming_version = ic_settings["version"]

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
            ic_image_preset = ic_preset["image_process"]
            ic_video_preset = ic_preset["video_process"]
            filtered_video_ext_dict = ic_preset["filterd_all_ext_dict"]["filtered_video_ext_dict"]
            filtered_image_ext_dict = ic_preset["filterd_all_ext_dict"]["filtered_image_ext_dict"]

            ic_logger.info("=IC PREPROCESSING START=")

            if (src_dir_path == dst_dir_path):
                ic_logger.info("!!!SAME PATH PROCEDURE ACTIVATE!!!")

                src_icfilelist = pre_processiong.ic_search(src_dir_path,
                                                        dst_dir_path,
                                                        filtered_video_ext_dict,
                                                        filtered_image_ext_dict,
                                                        filtered_archive_ext_dict)

                ic_logger.info("FILE LENGTH: %d" % len(src_icfilelist))

                pre_processiong.print_video_icfile(src_icfilelist)
                pre_processiong.print_image_icfile(src_icfilelist)
                pre_processiong.print_archive_icfile(src_icfilelist)
                ic_logger.info("=IC PREPROCESSING END=")
            else:
                ic_logger.info("!!!COPY CAT!!!")
                ic_logger.info("=IC PREPROCESSING START=")

                src_icfilelist = pre_processiong.ic_search(src_dir_path,
                                                        dst_dir_path,
                                                        filtered_video_ext_dict,
                                                        filtered_image_ext_dict,
                                                        filtered_archive_ext_dict)

                ic_logger.info("FILE LENGTH: %d" % len(src_icfilelist))

                pre_processiong.print_video_icfile(src_icfilelist)
                pre_processiong.print_image_icfile(src_icfilelist)
                pre_processiong.print_archive_icfile(src_icfilelist)

            ic_logger.info("=IC PREPROCESSING END=")

            """
                DUMMY OPTION CHECK
            """
            if (args.dummy):
                pre_processiong.create_dummy_icfilelist(src_icfilelist)

            """
                IC IMAGE PROCESS
            """
            ic_logger.info("=IC IMAGE PROCESS START=")

            image_icfilelist = pre_processiong.get_image_icfilelist(src_icfilelist)

            for (idx, image_icfile) in enumerate(image_icfilelist):
                ic_image_processor = ImageProcessor(image_icfile, ic_image_preset)

                ic_image_processor.ic_image_process()

            ic_logger.info("=IC IMAGE PROCESS END=")

            """
                IC VIDEO PROCESS
            """
            ic_logger.info("=IC VIDEO PROCESS START=")

            video_icfilelist = pre_processiong.get_video_icfilelist(src_icfilelist)

            for (idx, video_icfile) in enumerate(video_icfilelist):
                ic_video_processor = VideoProcessor(video_icfile, ic_video_preset)

                ic_video_processor.ic_video_process()

            ic_logger.info("=IC VIDEO PROCESS END=")
        else:
            """
                IC PREPROCESS
            """
            ic_logger.info("!!!DEFAULT PRESET USE!!!")
            ic_logger.info("=IC PREPROCESSING START=")

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

                src_icfilelist = pre_processiong.ic_search(src_dir_path,
                                                        dst_dir_path,
                                                        filtered_video_ext_dict,
                                                        filtered_image_ext_dict,
                                                        filtered_archive_ext_dict)

                pre_processiong.print_video_icfile(src_icfilelist)
                pre_processiong.print_image_icfile(src_icfilelist)
                pre_processiong.print_archive_icfile(src_icfilelist)
                pre_processiong.print_not_filtered_icfile(src_icfilelist)

                if (args.dummy):
                    pre_processiong.create_dummy_icfilelist(src_icfilelist)

            else:
                ic_logger.info("!!!COPY CAT!!!")

                src_icfilelist = pre_processiong.ic_search(src_dir_path,
                                                        dst_dir_path,
                                                        filtered_video_ext_dict,
                                                        filtered_image_ext_dict,
                                                        filtered_archive_ext_dict)

                ic_logger.info("FILE LENGTH: %d" % len(src_icfilelist))

                pre_processiong.print_video_icfile(src_icfilelist)
                pre_processiong.print_image_icfile(src_icfilelist)
                pre_processiong.print_archive_icfile(src_icfilelist)
                pre_processiong.print_not_filtered_icfile(src_icfilelist)

            ic_logger.info("=IC PREPROCESSING END=")

            """
                DUMMY OPTION CHECK
            """
            if (args.dummy):
                pre_processiong.create_dummy_icfilelist(src_icfilelist)

            """
                IC IMAGE PROCESS
            """
            ic_logger.info("=IC IMAGE PROCESS START=")

            image_icfilelist = pre_processiong.get_image_icfilelist(src_icfilelist)

            for (idx, image_icfile) in enumerate(image_icfilelist):
                ic_image_processor = ImageProcessor(image_icfile, ic_image_preset)

                ic_image_processor.ic_image_process()

            ic_logger.info("=IC IMAGE PROCESS END=")

            """
                IC VIDEO PROCESS
            """
            ic_logger.info("=IC VIDEO PROCESS START=")

            video_icfilelist = pre_processiong.get_video_icfilelist(src_icfilelist)

            for (idx, video_icfile) in enumerate(video_icfilelist):
                ic_video_processor = VideoProcessor(video_icfile, ic_video_preset)

                ic_video_processor.ic_video_process()

            ic_logger.info("=IC VIDEO PROCESS END=")
    else:
        if (args.user_preset != None):
            ic_logger.info("!!!USER PRESET USE!!!")
            ic_logger.info("=IC PREPROCESSING START=")

            if (not os.path.exists(src_dir_path) or not os.path.exists(src_dir_path)):
                ic_logger.warning("INVALID PATH")

                return (-1)

            ic_preset = pre_processiong.open_ic_user_preset(args.user_preset)

            filtered_video_ext_dict = ic_preset["filterd_all_ext_dict"]["filtered_video_ext_dict"]
            filtered_image_ext_dict = ic_preset["filterd_all_ext_dict"]["filtered_image_ext_dict"]

            if (src_dir_path == dst_dir_path):
                ic_logger.info("!!!SAME PATH PROCEDURE ACTIVATE!!!")

                src_icfilelist = pre_processiong.ic_search(src_dir_path,
                                                        dst_dir_path,
                                                        filtered_video_ext_dict,
                                                        filtered_image_ext_dict,
                                                        filtered_archive_ext_dict)

                ic_logger.info("FILE LENGTH: %d" % len(src_icfilelist))

                pre_processiong.print_video_icfile(src_icfilelist)
                pre_processiong.print_image_icfile(src_icfilelist)
                pre_processiong.print_archive_icfile(src_icfilelist)
                ic_logger.info("=IC PREPROCESSING END=")
            else:
                ic_logger.info("!!!COPY CAT!!!")
                ic_logger.info("=IC PREPROCESSING START=")

                src_icfilelist = pre_processiong.ic_search(src_dir_path,
                                                        dst_dir_path,
                                                        filtered_video_ext_dict,
                                                        filtered_image_ext_dict,
                                                        filtered_archive_ext_dict)

                ic_logger.info("FILE LENGTH: %d" % len(src_icfilelist))

                pre_processiong.print_video_icfile(src_icfilelist)
                pre_processiong.print_image_icfile(src_icfilelist)
                pre_processiong.print_archive_icfile(src_icfilelist)
                ic_logger.info("=IC PREPROCESSING END=")

            """
                DUMMY OPTION CHECK
            """
            if (args.dummy):
                pre_processiong.create_dummy_icfilelist(src_icfilelist)

            """
                IC IMAGE PROCESS
            """
            ic_logger.info("=IC IMAGE PROCESS START=")

            image_icfilelist = pre_processiong.get_image_icfilelist(src_icfilelist)

            for (idx, image_icfile) in enumerate(image_icfilelist):
                ic_image_processor = ImageProcessor(image_icfile, ic_image_preset)

                ic_image_processor.ic_image_process()

            ic_logger.info("=IC IMAGE PROCESS END=")

            """
                IC VIDEO PROCESS
            """
            ic_logger.info("=IC VIDEO PROCESS START=")

            video_icfilelist = pre_processiong.get_video_icfilelist(src_icfilelist)

            for (idx, video_icfile) in enumerate(video_icfilelist):
                ic_video_processor = VideoProcessor(video_icfile, ic_video_preset)

                ic_video_processor.ic_video_process()

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

                icfilelist = pre_processiong.ic_search(src_dir_path,
                                                        dst_dir_path,
                                                        filtered_video_ext_dict,
                                                        filtered_image_ext_dict,
                                                        filtered_archive_ext_dict)

                pre_processiong.print_video_icfile(icfilelist)
                pre_processiong.print_image_icfile(icfilelist)
                pre_processiong.print_archive_icfile(icfilelist)
                pre_processiong.print_not_filtered_icfile(icfilelist)
            else:
                ic_logger.info("!!!COPY CAT!!!")

                icfilelist = pre_processiong.ic_search(src_dir_path,
                                                        dst_dir_path,
                                                        filtered_video_ext_dict,
                                                        filtered_image_ext_dict,
                                                        filtered_archive_ext_dict)

                ic_logger.info("FILE LENGTH: %d" % len(icfilelist))

                pre_processiong.print_video_icfile(icfilelist)
                pre_processiong.print_image_icfile(icfilelist)
                pre_processiong.print_archive_icfile(icfilelist)
                pre_processiong.print_not_filtered_icfile(icfilelist)

            ic_logger.info("=IC PREPROCESSING END=")

            """
                DUMMY OPTION CHECK
            """
            if (args.dummy):
                pre_processiong.create_dummy_icfilelist(icfilelist)

            """
                IC IMAGE PROCESS
            """
            ic_logger.info("=IC IMAGE PROCESS START=")

            for (idx, icfile) in enumerate(icfilelist):
                if (pre_processiong.is_image_icfile(icfile)):
                    ic_image_processor = ImageProcessor(icfile, ic_image_preset)

                    if (ic_image_processor.ic_image_process()):
                        icfile.ictype = IcType.OUTGOING

            ic_logger.info("=IC IMAGE PROCESS END=")

            """
                IC VIDEO PROCESS
            """
            ic_logger.info("=IC VIDEO PROCESS START=")

            for (idx, icfile) in enumerate(icfilelist):
                if (pre_processiong.is_video_icfile(icfile)):
                    ic_video_processor = VideoProcessor(icfile, ic_video_preset)

                    if (ic_video_processor.ic_video_process()):
                        icfile.ictype = IcType.OUTGOING

            ic_logger.info("=IC VIDEO PROCESS END=")

            """
                IC POST PROCESS
            """
            pre_processiong.print_all_icfile(icfilelist)


if __name__ == "__main__":
    main()
