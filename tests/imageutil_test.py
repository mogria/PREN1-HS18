import pytest
import random
import os
import shutil

from mollyvision import imageutil

exptected_number_of_files_in_dir = 2
def make_image_folder(tmpdir):
    test_extensions = [ "jpg", "png", "PNG", "GIF" ]
    os.mkdir(os.path.join(tmpdir, "subdir")) # 10 image files
    os.mkdir(os.path.join(tmpdir, "subdir", "empty_subdir"))
    os.mkdir(os.path.join(tmpdir, "subdir2"))
    os.mkdir(os.path.join(tmpdir, "subdir2", "subdir"))
    for filenum in range(0, exptected_number_of_files_in_dir):
        extension = test_extensions[random.randrange(len(test_extensions))]
        filename = str(filenum)
        gen_file_with_extension(tmpdir, filename, extension)
        gen_file_with_extension(tmpdir, filename, "txt")
        gen_file_with_extension(os.path.join(tmpdir, "subdir") , filename, "txt")
        gen_file_with_extension(os.path.join(tmpdir, "subdir") , filename, extension)
        gen_file_with_extension(os.path.join(tmpdir, "subdir2") , filename, extension)
        gen_file_with_extension(os.path.join(tmpdir, "subdir2", "subdir") , filename, extension)
        gen_file_with_extension(os.path.join(tmpdir, "subdir2", "subdir") , filename,"pn")

    return tmpdir


def gen_file_with_extension(directory, name, extension):
    imagefile = os.path.join(directory, name + "." + extension)
    with open(imagefile, "w") as f:
        f.write("test")

def test_read_image_folder__count(tmpdir):
    image_folder = make_image_folder(tmpdir)
    actual_image_files = imageutil.read_image_folder(image_folder)
    assert exptected_number_of_files_in_dir == len(actual_image_files)

def test_read_image_folder__recursive_count(tmpdir):
    image_folder = make_image_folder(tmpdir)
    actual_image_files = imageutil.read_image_folder(image_folder, True)
    for f in actual_image_files:
        print(f)
    assert exptected_number_of_files_in_dir * 4 == len(actual_image_files)


def test_read_image_folder__no_other_files_returned(tmpdir):
    image_folder = make_image_folder(tmpdir)
    for image in imageutil.read_image_folder(image_folder):
        assert image[-4:] != ".pn"
        assert image[-4:] != ".txt"

def test_read_image_folder__recursive_no_other_files_returned(tmpdir):
    image_folder = make_image_folder(tmpdir)
    for image in imageutil.read_image_folder(image_folder, True):
        assert image[-4:] != ".pn"
        assert image[-4:] != ".txt"

