import subprocess

from ic_preprocessing import *

incoming = IcFile["src_path"]
outgoing = IcFile["dst_path"]
hb_preset = None #?

def encode_with_handbrake(incoming, outgoing, hb_preset_path):

    command = ["HandBrakeCLI", "-i", incoming, "-o", outgoing, "--preset-import-file", hb_preset_path]
    subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

def encode_with_ffmpeg(incoming, outgoing): # "custom_batch_command_input_toggle":"true" 이면 사용자가 직접 입력한 커맨드를 사용, $in $out으로 문자열 검출해서 대치


    
    print("# Custom ffmpeg opttion detected.\n  '$in','$out' will be replaced with the input and output file paths.\n   You must provide extesions at last.\n   e.g. $in -c:v libx264 -crf 23 -c:a aac -b:a 128k -strict -2) $out.mp4\n")
    input("incoming >> ffmpeg ")

    command = ["ffmpeg", "-i", incoming, outgoing]
    subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)


'''
import subprocess

# 커맨드라인 명령을 나타내는 문자열의 리스트
command = ["handbrakecli", "--version"]

# subprocess.check_output을 사용하여 명령의 출력을 얻
output = subprocess.check_output(command)

# 출력을 디코딩하여 출력
print(output.decode())
==
import subprocess

# 커맨드라인 명령을 나타내는 문자열의 리스트
command = ["HandBrakeCLI", "--version"]

# subprocess.Popen을 사용하여 새로운 프로세스 생성
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# communicate 메서드를 사용하여 출력과 오류 메시지를 얻음
stdout, stderr = process.communicate()

# 출력과 오류 메시지를 출력
print(stdout)
#print(stderr)
'''