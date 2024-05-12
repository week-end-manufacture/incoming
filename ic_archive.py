import os
import zipfile
import rarfile
import py7zr
from PIL import Image

def is_image(file_path):
    try:
        Image.open(file_path)
        return True
    except IOError:
        return False

def extract_if_contains_images(archive_path, archive_type):
    image_count = 0
    if archive_type == 'zip':
        with zipfile.ZipFile(archive_path, 'r') as archive:
            for file in archive.namelist():
                if is_image(file):
                    image_count += 1
    elif archive_type == 'rar':
        with rarfile.RarFile(archive_path, 'r') as archive:
            for file in archive.namelist():
                if is_image(file):
                    image_count += 1
    elif archive_type == '7z':
        with py7zr.SevenZipFile(archive_path, mode='r') as archive:
            for file in archive.getnames():
                if is_image(file):
                    image_count += 1
    if image_count >= 2:
        if archive_type == 'zip':
            with zipfile.ZipFile(archive_path, 'r') as archive:
                archive.extractall()
        elif archive_type == 'rar':
            with rarfile.RarFile(archive_path, 'r') as archive:
                archive.extractall()
        elif archive_type == '7z':
            with py7zr.SevenZipFile(archive_path, mode='r') as archive:
                archive.extractall()

def main(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.zip'):
                extract_if_contains_images(os.path.join(root, file), 'zip')
            elif file.endswith('.rar'):
                extract_if_contains_images(os.path.join(root, file), 'rar')
            elif file.endswith('.7z'):
                extract_if_contains_images(os.path.join(root, file), '7z')

main('/your/directory/path')