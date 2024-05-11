import os
import argparse
from pathlib import Path

from ic_preprocessing import *

def main():
    pre_processiong = PreProcessing()
    ic_settings = pre_processiong.open_ic_settings()

    src_dir_path = ic_settings["src_dir_path"]
    dst_dir_path = ic_settings["dst_dir_path"]
    incoming_version = ic_settings["version"]

    """
        명령어 설정
    """
    parser = argparse.ArgumentParser(prog='incoming')
    parser.add_argument("-s", "--src_dir_path", help="Source directory path", action="store")
    parser.add_argument("-d", "--dst_dir_path", help="Destination directory path", action="store")
    parser.add_argument("-e", "--user_ext", help="Extention list", action="store")
    parser.add_argument("-v", "--version", help="Version", action="version", version='%(prog)s ' + incoming_version)
    args = parser.parse_args()

    if (args.src_dir_path != None and args.dst_dir_path != None):
        print(args(src_dir_path))
        print(args(dst_dir_path))

        if (args.user_ext != None):
            print(args.user_ext)
    else:
        print("!!!DEFAULT USE!!!")
        print("SRC_DIR_PATH:[%s]" % src_dir_path)
        print("DST_DIR_PATH:[%s]" % dst_dir_path)

        ic_preset = pre_processiong.open_ic_preset()

        filtered_video_ext_dict = ic_preset["filterd_all_ext_dict"]["filtered_video_ext_dict"]
        filtered_image_ext_dict = ic_preset["filterd_all_ext_dict"]["filtered_image_ext_dict"]
        filtered_archive_ext_dict = ["zip", "rar", "7z"]

        print("filtered_video_ext_dict", filtered_video_ext_dict)

        if (src_dir_path == dst_dir_path):
            print("!!!SAME PATH PROCEDURE ACTIVATE!!!")

            for (src_path, src_dir, src_file) in os.walk(src_dir_path):
                for (idx, src_file) in enumerate(src_filelist):
                    print("===================================")
                    print("PATH: %s" % src_path)
                    print("DIRECTORY: %s" % src_dir)
                    print("FILENAME: %s" % src_file)
                    print("===================================")
        else:
            print("!!!COPY CAT!!!")

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

            print(src_icfilelist)

            print("FILE LENGTH: %d" % len(src_icfilelist))

            pre_processiong.print_video_icfile(src_icfilelist)
            pre_processiong.print_image_icfile(src_icfilelist)
            pre_processiong.print_archive_icfile(src_icfilelist)


if __name__ == "__main__":
    main()