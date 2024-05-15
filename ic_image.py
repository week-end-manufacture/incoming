import os
from PIL import Image, ImageCms

from ic_preprocessing import *

class ImageProcessor:
    def __init__(self, image_icfile, ic_image_preset):
        self.image_icfile = image_icfile
        self.iamge_preset = ic_image_preset

    def image_open(self, image_path):
        return Image.open(image_path)

    def ic_image_process(self):
        if self.iamge_preset['image_process_toggle']:
            src_image_abs_path = os.path.join(self.image_icfile.src_path, self.image_icfile.filename)
            dst_image_abs_path = os.path.join(self.image_icfile.dst_path, self.image_icfile.filename)
            dst_image_path = self.image_icfile.dst_path

            ic_image = self.image_open(src_image_abs_path)

            """
            if self.iamge_preset['assign_untagged_icc_profile_to_sRGB']:
                self.assign_untagged_icc_profile_to_sRGB()

            if self.iamge_preset['remove_only_gps_exif_data']:
                self.remove_only_gps_exif_data()

            if self.iamge_preset['remove_all_exif_data']:
                self.remove_all_exif_data()
            """

            self.save_processed_image(ic_image, dst_image_abs_path, dst_image_path)

    def assign_untagged_icc_profile_to_sRGB(self, ic_image):
        retval: Image = None

        srgb_profile = ImageCms.createProfile("sRGB")
        retval = ImageCms.profileToProfile(ic_image, srgb_profile, outputMode='RGB')

        return retval

    def remove_only_gps_exif_data(self, ic_image):
        if 'exif' in self.image.info:
            exif_dict = Image._getexif(self.image)
            if 34853 in exif_dict:  # "34853" is a pointer to the GPS information IFD
                del exif_dict[34853]
            self.image.info['exif'] = Image._makeexif(exif_dict)

    def remove_all_exif_data(self, ic_image):
        self.image.info.pop('exif', None)

    def save_processed_image(self, ic_image, dst_image_abs_path, dst_image_path):
        if not os.path.exists(dst_image_path):
            os.makedirs(dst_image_path)

        ic_image.save(dst_image_abs_path, quality=85)
