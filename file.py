import os
import shutil
from datetime import datetime
import load_settings #main.py 에서 했으면 여긴 안해도 돼나?

class FilesGonna: # src_dir -> incoming dst_dir -> outgoing
    # ext 필터에 안걸리는 파일들을 복사하는 함수만드는 중
    def be_copied_nonfiltered(src_dir, dst_dir):
        for root, dirs, files in os.walk(src_dir):
            relpath_from_src_dir = os.path.relpath(root, src_dir)
            outgoing = os.path.join(dst_dir, relpath_from_src_dir)
            os.makedirs(outgoing, exist_ok=True)
        
        for file in files:
            if not file.lower().endswith(filterd_ext):
                src_file_path = os.path.join(root, file)
                target_file_path = os.path.join(outgoing, file)
                shutil.copy2(src_file_path, target_file_path)
        

idset = load_settings.from_jsonc()
src_dir = idset["src_dir_path"]
dst_dir = idset["dst_dir_path"]
filterd_ext = idset["filterd_ext_dict"]