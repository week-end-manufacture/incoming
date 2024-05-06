'''# 이미지 파일 열기
img = Image.open(image_path)

# 이미지를 RGB 모드로 변환

img = img.convert('RGB')

# 컬러 프로파일 확인
if 'icc_profile' in img.info:
    icc_profile = img.info['icc_profile']
else:
    # 컬러 프로파일이 없을 경우 sRGB로 설정
    srgb_profile = ImageCms.createProfile("sRGB")
    icc_profile = ImageCms.getOpenProfile(srgb_profile).tobytes()

# 파일 이름과 확장자 분리
file_name, file_ext = os.path.splitext(image_path)

# 파일 이름에 '[pil]' 접미어 추가하고 다시 결합
compressed_image_path = f"{file_name}[pil].jpg"

# 이미지를 압축하여 저장하면서 컬러 프로파일 유지
img.save(compressed_image_path, 'JPEG', quality=85, icc_profile=icc_profile)'''

import os
import sys
from PIL import Image, ImageCms


class ImgProcessor:
    def __init__(self, image_path):
        self.image_path = image_path
        self.img = Image.open(image_path)

    def convert_to_rgb(self): # 이미지를 RGB 모드로 변환
        self.img = self.img.convert('RGB')

    def get_icc_profile(self): # 컬러 프로파일 확인
        if 'icc_profile' in self.img.info:
            return self.img.info['icc_profile']
        else: # 컬러 프로파일이 없을 경우 sRGB로 설정
            srgb_profile = ImageCms.createProfile("sRGB")
            return ImageCms.getOpenProfile(srgb_profile).tobytes()

    def save_compressed_image(self, compressed_image_path):
        icc_profile = self.get_icc_profile()
        self.img.save(compressed_image_path, 'JPEG', quality=85, icc_profile=icc_profile)


if __name__ == "__main__":
    result = ImgProcessor(sys.argv[1])