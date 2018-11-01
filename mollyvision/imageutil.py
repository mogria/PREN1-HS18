import cv2
import glob
import os
import itertools


""" reads all images files from a folder, recursive if desired """
def read_image_folder(folder, recurse=False):
    extensions = [ "jpg", "png", "JPG", "PNG", "gif", "GIF" ]
    pattern = "**/*" if recurse else "*"

    globs = [ os.path.join(glob.escape(folder), pattern + "." + extension) for extension in extensions ]

    matches_list = [ glob.glob(glob_pattern, recursive=recurse) for glob_pattern in globs ]

    # flatten 2d list into 1d, and make it unique
    return set(itertools.chain(*matches_list))
