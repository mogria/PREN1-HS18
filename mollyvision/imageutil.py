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

""" reads all images files relative to the "test_images" folder."""
def read_test_image_folder(folder, recurse=False):
    this_dir = os.path.dirname(__file__)
    test_images_dir = os.path.abspath(os.path.join(this_dir, "..", "test_images"))
    return read_image_folder(os.path.join(test_images_dir, folder), recurse)
