import os
from PIL import Image, ImageCms

from ic_preprocessing import *


class ImageProcessor:
    def __init__(self, image_icfile, ic_image_preset):
        self.image_icfile = image_icfile
        self.image_preset = ic_image_preset

    def image_open(self, image_path):
        return Image.open(image_path)
    
    def image_mode_converter(self, ic_image):
        retval = ic_image

        if (self.image_preset["output_ext"] == ".jpg" and ic_image.mode == "RGBA"):
            retval = retval.convert('RGB')
        elif (self.image_preset["output_ext"] == ".png" and ic_image.mode == "RGB"):
            retval = retval.convert('RGBA')

        return retval

    def ic_image_process(self):
        if self.image_preset['image_process_toggle']:
            src_image_abs_path = os.path.join(self.image_icfile.src_path, self.image_icfile.filename)
            dst_image_abs_path = os.path.join(self.image_icfile.dst_path, Path(self.image_icfile.filename).stem + self.image_preset["output_ext"])
            dst_image_path = self.image_icfile.dst_path

            ic_image = self.image_open(src_image_abs_path)

            ic_image = self.image_mode_converter(ic_image)

            if self.image_preset['remove_only_gps_exif_data']:
                ic_image = self.remove_only_gps_exif_data(ic_image)

            if self.image_preset['remove_all_exif_data']:
                self.save_processed_image(ic_image,
                                        dst_image_abs_path,
                                        dst_image_path,
                                        True)
            else:
                self.save_processed_image(ic_image,
                                        dst_image_abs_path,
                                        dst_image_path,
                                        False)
            
            cur_size = os.path.getsize(dst_image_abs_path)
            self.image_icfile.ictype = IcType.OUTGOING
            self.image_icfile.outgoing_size = cur_size
            
            return self.image_icfile

    def assign_untagged_icc_profile_to_sRGB(self, ic_image):
        retval = None

        retval = ic_image.info.get("icc_profile")

        if (retval == None):
            srgb_profile = ImageCms.createProfile("sRGB")
            retval = ImageCms.ImageCmsProfile(srgb_profile).tobytes()

            return retval
        else:
            return retval

    def remove_only_gps_exif_data(self, ic_image):
        retval = ic_image

        if 'exif' in retval.info:
            exif_dict = Image._getexif(retval)
            if 34853 in exif_dict:  # "34853" is a pointer to the GPS information IFD
                del exif_dict[34853]
            retval.info['exif'] = Image._makeexif(exif_dict)

        return retval

    def remove_all_exif_data(self, ic_image):
        retval = ic_image

        retval.info.pop('exif', None)

        return retval

    def save_processed_image(self, ic_image,
                             dst_image_abs_path,
                             dst_image_path,
                             exif_rm_flag):
        if not os.path.exists(dst_image_path):
            os.makedirs(dst_image_path)

        output_quality = self.image_preset["output_quality"]
        output_icc_profile = ic_image.info.get("icc_profile")

        if (exif_rm_flag):
            ic_image.save(dst_image_abs_path, quality=output_quality, icc_profile=output_icc_profile)
        else:
            org_exif = ic_image.getexif()
            ic_image.save(dst_image_abs_path, quality=output_quality, exif=org_exif, icc_profile=output_icc_profile)
