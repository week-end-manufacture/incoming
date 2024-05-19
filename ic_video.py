import subprocess

from ic_preprocessing import *
from ic_log import *


class VideoProcessor:
    def __init__(self, video_icfile, ic_video_preset):
        self.ic_logger_instance = IcLogger()
        self.ic_logger = self.ic_logger_instance.init_logger(__name__)

        self.video_icfile = video_icfile
        self.video_preset = ic_video_preset

    def ic_video_process(self):
        if self.video_preset['video_process_toggle']:
            src_video_abs_path = os.path.join(self.video_icfile.src_path, self.video_icfile.filename)
            dst_video_abs_path = os.path.join(self.video_icfile.dst_path, Path(self.video_icfile.filename).stem + self.video_preset["output_video_ext"])
            dst_video_path = self.video_icfile.dst_path

            if (self.video_preset["deafult_encoder_is_HandBrake"] == None):
                hb_preset_path = self.video_preset["HandBrake_presets_path"]

                self.encode_with_handbrake(src_video_abs_path, dst_video_abs_path, dst_video_path, hb_preset_path)
            else:
                self.encode_with_ffmpeg(src_video_abs_path, dst_video_abs_path)
            
    def encode_with_handbrake(self, src_video_abs_path, dst_video_abs_path, dst_video_path, hb_preset_path):
        if not os.path.exists(dst_video_path):
            os.makedirs(dst_video_path)

        print(src_video_abs_path)

        command = ["HandBrakeCLI", "-i", src_video_abs_path, "-o", dst_video_abs_path, "--preset-import-file", hb_preset_path]

        handbrake_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        while True:
            output = handbrake_process.stdout.readline()
            if output == '' and handbrake_process.poll() is not None:
                break
            if output:
                print(output.strip())
                self.ic_logger.info(output)

    def encode_with_ffmpeg(self, src_video_abs_path, dst_image_abs_path, dst_video_path):
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
                print(output.strip())
                self.ic_logger.info(output)
