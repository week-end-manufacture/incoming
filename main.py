import os
import argparse
from pathlib import Path

from ic_preprocessing import *
from ic_log import *
from ic_image import *

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
    parser.add_argument("-s", "--src_dir_path", help="Source directory path", action="store")
    parser.add_argument("-d", "--dst_dir_path", help="Destination directory path", action="store")
    parser.add_argument("-p", "--user_preset", help="User preset", action="store")
    parser.add_argument("-e", "--user_ext", help="Extention list", action="store")
    parser.add_argument("-v", "--version", help="Version", action="version", version='%(prog)s ' + incoming_version)
    args = parser.parse_args()

    if (args.src_dir_path != None and args.dst_dir_path != None):
        src_dir_path = args(src_dir_path)
        dst_dir_path = args(dst_dir_path)

        if (not os.path.exists(src_dir_path) or not os.path.exists(src_dir_path)):
            ic_logger.warning("INVALID PATH")

            return (-1)

        print("SRC_DIR_PATH:[%s]" % src_dir_path)
        print("DST_DIR_PATH:[%s]" % dst_dir_path)

        if (args.user_ext != None):
            print(args.user_ext)
    elif (args.user_preset != None):
        print("!!!USER PRESET USE!!!")

        if (not os.path.exists(src_dir_path) or not os.path.exists(src_dir_path)):
            ic_logger.warning("INVALID PATH")

            return (-1)

        ic_preset = pre_processiong.open_ic_user_preset(args.user_preset)

        filtered_video_ext_dict = ic_preset["filterd_all_ext_dict"]["filtered_video_ext_dict"]
        filtered_image_ext_dict = ic_preset["filterd_all_ext_dict"]["filtered_image_ext_dict"]

        print("filtered_video_ext_dict", filtered_video_ext_dict)

        if (src_dir_path == dst_dir_path):
            print("!!!SAME PATH PROCEDURE ACTIVATE!!!")

            src_icfilelist = pre_processiong.ic_serach(src_dir_path,
                                                       dst_dir_path,
                                                       filtered_video_ext_dict,
                                                       filtered_image_ext_dict,
                                                       filtered_archive_ext_dict)

            print(src_icfilelist)

            print("FILE LENGTH: %d" % len(src_icfilelist))

            pre_processiong.print_video_icfile(src_icfilelist)
            pre_processiong.print_image_icfile(src_icfilelist)
            pre_processiong.print_archive_icfile(src_icfilelist)
        else:
            print("!!!COPY CAT!!!")

            src_icfilelist = pre_processiong.ic_serach(src_dir_path,
                                                       dst_dir_path,
                                                       filtered_video_ext_dict,
                                                       filtered_image_ext_dict,
                                                       filtered_archive_ext_dict)

            print(src_icfilelist)

            print("FILE LENGTH: %d" % len(src_icfilelist))

            pre_processiong.print_video_icfile(src_icfilelist)
            pre_processiong.print_image_icfile(src_icfilelist)
            pre_processiong.print_archive_icfile(src_icfilelist)
    else:
        print("!!!DEFAULT PRESET USE!!!")
        print("SRC_DIR_PATH:[%s]" % src_dir_path)
        print("DST_DIR_PATH:[%s]" % dst_dir_path)

        ic_preset = pre_processiong.open_ic_default_preset()

        filtered_video_ext_dict = ic_preset["filterd_all_ext_dict"]["filtered_video_ext_dict"]
        filtered_image_ext_dict = ic_preset["filterd_all_ext_dict"]["filtered_image_ext_dict"]

        print("filtered_video_ext_dict", filtered_video_ext_dict)

        if (src_dir_path == dst_dir_path):
            print("!!!SAME PATH PROCEDURE ACTIVATE!!!")

            src_icfilelist = pre_processiong.ic_serach(src_dir_path,
                                                       dst_dir_path,
                                                       filtered_video_ext_dict,
                                                       filtered_image_ext_dict,
                                                       filtered_archive_ext_dict)

            print(src_icfilelist)

            print("FILE LENGTH: %d" % len(src_icfilelist))

            pre_processiong.print_video_icfile(src_icfilelist)
            pre_processiong.print_image_icfile(src_icfilelist)
            pre_processiong.print_archive_icfile(src_icfilelist)
            pre_processiong.print_not_filtered_icfile(src_icfilelist)

            pre_processiong.create_dummy_icfilelist(src_icfilelist)
        else:
            print("!!!COPY CAT!!!")

            src_icfilelist = pre_processiong.ic_serach(src_dir_path,
                                                       dst_dir_path,
                                                       filtered_video_ext_dict,
                                                       filtered_image_ext_dict,
                                                       filtered_archive_ext_dict)

            print(src_icfilelist)

            print("FILE LENGTH: %d" % len(src_icfilelist))

            pre_processiong.print_video_icfile(src_icfilelist)
            pre_processiong.print_image_icfile(src_icfilelist)
            pre_processiong.print_archive_icfile(src_icfilelist)
            pre_processiong.print_not_filtered_icfile(src_icfilelist)


if __name__ == "__main__":
    main()
