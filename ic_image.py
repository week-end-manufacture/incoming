import sys
from PIL import Image, ImageCms, ExifTags

import ic_process

class ImageProcessor:
    def __init__(self, ic_file, iset):
        self.image_path = ic_file.abs_path
        self.img = Image.open(self.image_path)
        self.iset = iset

    def convert_to_rgb(self): # 이미지를 RGB 모드로 변환
        self.img = self.img.convert('RGB')
   
    def get_icc_profile(self): # 컬러 프로파일 확인
        if 'icc_profile' in self.img.info:
            return self.img.info['icc_profile']
        else: 
            if self.iset.get('assign_untagged_icc_profile_to_sRGB', False):
                srgb_profile = ImageCms.createProfile("sRGB")
                self.img.info['icc_profile'] = ImageCms.getOpenProfile(srgb_profile).tobytes()
            return self.img.info.get('icc_profile', None)

    def remove_all_exif(self): # 모든 EXIF 데이터 제거
        self.img.info.pop('exif', None)

    def remove_gps_info(self): # GPS 정보만 제거
        if hasattr(self.img, '_getexif'): # 이미지가 exif 데이터를 가지고 있는지 확인
            exif_data = self.img._getexif()
            if exif_data is not None:
                # GPS 정보가 있는지 확인하고 제거
                if 34853 in exif_data: 
                    del exif_data[34853]
                # 변경된 exif 데이터로 이미지를 저장
                self.img.save(self.image_path, exif=exif_data)
        else:
            print("No EXIF data found")

    def save_compressed_image(self, compressed_image_path):
        icc_profile = self.get_icc_profile()
        self.img.save(compressed_image_path, 'JPEG', quality=85, icc_profile=icc_profile)

iset = ic_process.open_ic_preset()

if __name__ == "__main__":
    processor = ImageProcessor(sys.argv[1])
    processor.remove_all_exif()  # 모든 EXIF 데이터 제거
    processor.remove_gps_info()  # GPS 정보만 제거
    processor.save_compressed_image("compressed_image.jpg")  # 압축된 이미지 저장