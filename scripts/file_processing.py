import subprocess
from scripts.general_purpose import create_dir
import os
import cv2

def pre_process(file_params: dict) -> dict:
    """
    This function splits PDF to pages and put it into ./pagination folder

    :param file_params: dictionary, that collects all information linked with file
    :type file_params: dict
    :return: extended dictionary
    :rtype: dict
    """
    
    file_location = file_params["upload_path"] + file_params["new_name"]
    file_params["dispatch_path"] = file_params["upload_path"] + "pagination/"
    create_dir(file_params["dispatch_path"])
    new_target_file = file_params["dispatch_path"] + file_params["name_without_extension"] + "-%d.png"
    new_target_file = new_target_file.replace(" ", "_")
    subprocess.call(
        'pdftoppm "%s" "%s"' % (
        file_location, new_target_file), shell=True, executable='/bin/bash')
    for img in os.listdir(file_params["dispatch_path"]):
        if img.endswith(".ppm"):
            img_path = file_params['dispatch_path'] + img
            img_no_ext = img.split(".")[0]
            img_path_new_extension = file_params['dispatch_path'] + img_no_ext + ".png"
            subprocess.call(
                'convert -density 300x300 -units PixelsPerInch "%s" -deskew 40%% -background "white" -alpha remove "%s"' % (
                    img_path, img_path_new_extension), shell=True, executable='/bin/bash')

    return file_params

DEF_ROTATE_IMG = "/home/denny_k/Documents/rotate_test.jpg"
