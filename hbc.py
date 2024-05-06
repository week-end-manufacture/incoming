import os
import shutil
import subprocess
from datetime import datetime
import sys

def find_preset_file():
    # 스크립트가 위치한 디렉토리에서 모든 .json 파일 찾기
    script_dir = os.path.dirname(os.path.abspath(__file__))  # 스크립트 디렉토리 경로
    json_files = [f for f in os.listdir(script_dir) if f.endswith('.json')]
    if len(json_files) == 1:
        return os.path.abspath(os.path.join(script_dir, json_files[0]))  # 첫 번째 .json 파일의 절대 경로 반환
    else:
        print("Error: Found {} .json files.".format(len(json_files)))
        preset_path = input("Please enter the absolute path to the preset file, or press enter to exit: ").strip()
        if preset_path:
            return preset_path
        else:
            print("No preset path provided. Exiting.")
            sys.exit(1)  # 입력이 공백일 경우 종료

def create_target_directory(source_path, base_target_path):
    source_folder_name = os.path.basename(os.path.normpath(source_path))
    date_suffix = datetime.now().strftime("%Y-%m-%d_%H-%M")
    target_folder_name = f"{source_folder_name}-hb_{date_suffix}"
    
    if base_target_path.strip() == "":
        target_path = os.path.join(os.path.dirname(source_path), target_folder_name)
    else:
        target_path = os.path.join(base_target_path, target_folder_name)
    
    os.makedirs(target_path, exist_ok=True)
    return target_path

def copy_non_video_files(source_path, target_path):
    for root, dirs, files in os.walk(source_path):
        relative_path = os.path.relpath(root, source_path)
        target_dir = os.path.join(target_path, relative_path)
        os.makedirs(target_dir, exist_ok=True)
        
        for file in files:
            if not file.lower().endswith(tuple(extensions)):
                src_file_path = os.path.join(root, file)
                target_file_path = os.path.join(target_dir, file)
                shutil.copy2(src_file_path, target_file_path)

def encode_videos(source_path, target_path, preset_path, log_file_path):
    video_files = []
    
    for root, dirs, files in os.walk(source_path):
        for file in files:
            if file.lower().endswith(tuple(extensions)):
                video_files.append(os.path.join(root, file))
    
    video_files.sort(key=lambda x: os.path.basename(x))
    
    with open(log_file_path, "w") as log_file:
        for item in video_files:
            relative_path = os.path.relpath(os.path.dirname(item), source_path)
            output_dir = os.path.join(target_path, relative_path)
            os.makedirs(output_dir, exist_ok=True)
            
            file_name = os.path.basename(item)
            output_file = os.path.join(output_dir, f"{file_name.rsplit('.', 1)[0]}-hbc.mp4")
            
            command = ["HandBrakeCLI", "-i", item, "-o", output_file, "--preset-import-file", preset_path]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            
            # 로그 파일과 터미널에 동시에 출력
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())
                    log_file.write(output)

# 파일 확장자 목록
extensions = ['.asf', '.avi', '.flv', '.mkv', '.mov', '.mp4', '.mpeg', '.ts', '.webm', '.webp', '.wmv', '.m4v', '.mpg', '.ts', '.mts', '.m2ts', '.vob', '.evo']

# 프리셋 파일 검색 및 설정
preset_path = find_preset_file()

if preset_path:  # 프리셋 파일의 절대 경로를 성공적으로 가져올 수 있다면, 나머지 작업 수행
    # 사용자 입력
    source_folder = input("Enter the path to the source video folder: ")
    target_base_folder = input("Enter the base path for the target folder (leave blank to use source folder location): ")

    # 타겟 폴더 생성 및 설정
    target_folder = create_target_directory(source_folder, target_base_folder)
    log_file_path = os.path.join(target_folder, "hb.log")

    # 비디오 파일을 제외한 파일 복사
    copy_non_video_files(source_folder, target_folder)

    # 비디오 파일 인코딩 및 로그 파일 작성
    encode_videos(source_folder, target_folder, preset_path, log_file_path)
