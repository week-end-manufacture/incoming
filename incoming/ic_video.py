import subprocess
import os

from incoming.ic_filehandler import *
from incoming.ic_log import ic_logger_instance_ic_video


class VideoProcessor:
    def __init__(self, video_icfile, ic_video_preset):
        self.ic_logger = ic_logger_instance_ic_video.logger

        self.video_icfile = video_icfile
        self.video_preset = ic_video_preset

    def ic_video_process(self):
        if self.video_preset['video_process_toggle']:
            src_video_abs_path = os.path.join(self.video_icfile.src_path, self.video_icfile.filename)
            dst_video_abs_path = os.path.join(self.video_icfile.dst_path, Path(self.video_icfile.filename).stem + self.video_preset["output_video_ext"])
            dst_video_path = self.video_icfile.dst_path

            if (self.video_preset["deafult_encoder_is_HandBrake"] == None):
                hb_preset_path = self.video_preset["HandBrake_presets_path"]

                self.encode_with_handbrake(src_video_abs_path,
                                           dst_video_abs_path,
                                           dst_video_path,
                                           hb_preset_path,
                                           self.video_icfile.filename,
                                           self.video_preset)
            else:
                self.encode_with_ffmpeg(src_video_abs_path,
                                        dst_video_abs_path)

            cur_size = os.path.getsize(dst_video_abs_path)
            self.video_icfile.ictype = IcType.OUTGOING
            self.video_icfile.outgoing_size = cur_size

            return self.video_icfile
            
    def encode_with_handbrake(self,
                              src_video_abs_path,
                              dst_video_abs_path,
                              dst_video_path,
                              hb_preset_path,
                              filename,
                              video_preset):
        if not os.path.exists(dst_video_path):
            os.makedirs(dst_video_path)

        command = ["HandBrakeCLI", "-i", src_video_abs_path, "-o", dst_video_abs_path, "--preset-import-file", hb_preset_path]

        handbrake_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, universal_newlines=True)

        bar_idx = 0
        vid_loading_bar = {0: '\\', 1: '|', 2: '/', 3: '-'}

        sys.stdout.write(filename + ' ===> ' + video_preset["output_video_ext"] + ' via HandBrakeCLI\n')
        sys.stdout.flush()

        while True:
            output = handbrake_process.stdout.readline()
            if (output == '' and handbrake_process.poll() is not None) or not output:
                break
            if output:
                bar_idx %= 4
                chk = output.strip().startswith("Encoding: task")
                if (chk):
                    sys.stdout.write('\r' + '  ╰─ ' + vid_loading_bar[bar_idx] + ' [' + output.strip() + ']')
                    sys.stdout.flush()
                    bar_idx += 1
                else:
                    self.ic_logger.info(output.strip())

        sys.stdout.write('| DONE\n')
        sys.stdout.flush()
        handbrake_process.stdout.close()

    def encode_with_ffmpeg(self,
                           src_video_abs_path,
                           dst_image_abs_path,
                           dst_video_path):
        if not os.path.exists(dst_video_path):
            os.makedirs(dst_video_path)

        print("# Custom ffmpeg opttion detected.\n  '$in','$out' will be replaced with the input and output file paths.\n   You must provide extesions at last.\n   e.g. $in -c:v libx264 -crf 23 -c:a aac -b:a 128k -strict -2) $out.mp4\n")
        input("incoming >> ffmpeg ")

        command = ["ffmpeg", "-i", src_video_abs_path, dst_image_abs_path]
        ffmpeg_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        while True:
            output = ffmpeg_process.stdout.readline()
            if output == '' and ffmpeg_process.poll() is not None:
                break
            if output:
                #print(output.strip())
                self.ic_logger.info(output)
