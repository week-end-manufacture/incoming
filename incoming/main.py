import os
import argparse
from pathlib import Path

from incoming.ic_printer import *
from incoming.ic_filehandler import *
from incoming.ic_preprocessing import *
from incoming.ic_log import ic_logger_instance_main
from incoming.ic_image import *
from incoming.ic_video import *
from incoming.ic_postprocessing import *
from incoming.ic_result import *
from libj.verlib import __version__

def main():
    """
        LOG INIT
    """
    ic_logger = ic_logger_instance_main.logger

    pre_processiong = PreProcessing()
    ic_filehandler = IcFileHandler()
    ic_settings = pre_processiong.open_ic_settings()


    src_dir_path = ic_settings["src_dir_path"]
    dst_dir_path = ic_settings["dst_dir_path"]
    incoming_version = __version__

    filtered_archive_ext_dict = [".zip", ".rar", ".7z"]

    """
        명령어 설정
    """
    parser = argparse.ArgumentParser(prog='incoming')
    parser.add_argument("-i", "--src_dir_path", help="Source directory path", action="store")
    parser.add_argument("-o", "--dst_dir_path", help="Destination directory path", action="store")
    parser.add_argument("-p", "--user_preset", help="User preset", action="store")
    parser.add_argument("-s", "--settings", help="Open setting directory", action="store_true")
    parser.add_argument("-d", "--dummy", help="Create dummy file", action="store_true")
    parser.add_argument("-u", "--unlink", help="Unlink incoming file", action="store_true")
    parser.add_argument("-v", "--version", help="Version", action="version", version='%(prog)s version ' + incoming_version + ', built with Homebrew')
    args = parser.parse_args()

    sys.stdout.write('\nincoming version ' + incoming_version + ', built with Homebrew\n')

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

    if (args.settings):
        pre_processiong.open_ic_env_dir()

        return (1)

    if (args.user_preset != None):
        """
            IC PRESET LOADING
        """
        preset_path = args.user_preset
        ic_preset = pre_processiong.open_ic_user_preset(preset_path)
    else:
        """
            IC PRESET LOADING
        """
        preset_path = ic_settings["default_preset_path"]
        ic_preset = pre_processiong.open_ic_default_preset(ic_settings["default_preset_path"])

    ic_image_preset = ic_preset["image_process"]
    ic_video_preset = ic_preset["video_process"]
    filtered_video_ext_dict = ic_preset["filterd_all_ext_dict"]["filtered_video_ext_dict"]
    filtered_image_ext_dict = ic_preset["filterd_all_ext_dict"]["filtered_image_ext_dict"]

    print_process_start(src_dir_path,
                        dst_dir_path,
                        preset_path,
                        ic_image_preset["image_process_toggle"],
                        filtered_image_ext_dict,
                        ic_image_preset["output_ext"],
                        ic_image_preset["output_quality"],
                        ic_video_preset["video_process_toggle"],
                        filtered_video_ext_dict,
                        ic_video_preset["output_video_ext"],
                        ic_video_preset["HandBrake_presets_path"])

    main_icfilelist = pre_processiong.ic_search(src_dir_path,
                                            dst_dir_path,
                                            filtered_video_ext_dict,
                                            filtered_image_ext_dict,
                                            filtered_archive_ext_dict)

    image_icfilelist = ic_filehandler.get_image_icfilelist(main_icfilelist)
    image_icfilelist_len = len(image_icfilelist)
    video_icfilelist = ic_filehandler.get_video_icfilelist(main_icfilelist)
    video_icfilelist_len = len(video_icfilelist)

    """
        DUMMY OPTION CHECK
    """
    if (args.dummy):
        pre_processiong.create_dummy_icfilelist(main_icfilelist)

        return (True)

    """
        IC IMAGE PROCESS
    """
    for (idx, icfile) in enumerate(image_icfilelist):
        print_progressbar(idx + 1, image_icfilelist_len, '🏞️ Image Process:', '', 50)
        if (ic_filehandler.is_image_icfile(icfile)):
            ic_image_processor = ImageProcessor(icfile, ic_image_preset)

            icfile = ic_image_processor.ic_image_process()

    print_job_done()

    """
        IC VIDEO PROCESS
    """
    print_video_process_init()

    for (idx, icfile) in enumerate(main_icfilelist):
        if (ic_filehandler.is_video_icfile(icfile)):
            ic_video_processor = VideoProcessor(icfile, ic_video_preset)

            icfile = ic_video_processor.ic_video_process()

    """
        IC POST PROCESS
    """
    for (idx, icfile) in enumerate(main_icfilelist):
        if (ic_filehandler.is_incoming_icfile(icfile)):
            ic_post_processor = PostProcessing(icfile)

            icfile = ic_post_processor.ic_copy()

            del ic_post_processor

    for (idx, icfile) in enumerate(main_icfilelist):
        ic_post_processor = PostProcessing(icfile)

        icfile = ic_post_processor.ic_unlink()

        del ic_post_processor

    """
        IC RESULT
    """
    ic_result = Result()

    ic_filehandler.logging_icfile(main_icfilelist)
    ic_result.ic_result(main_icfilelist)

    return (True)


if __name__ == "__main__":
    main()
