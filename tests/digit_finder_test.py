import pytest
import numpy
import cv2
from mollyvision.digit_finder import find_digit
from mollyvision import imageutil

def raspicam_no_digit_images():
    return imageutil.read_test_image_folder('uncut/raspicam/no_digit')

def raspicam_digit_8_images():
    return imageutil.read_test_image_folder('uncut/raspicam/8')

@pytest.mark.parametrize('image', raspicam_no_digit_images())
def test_find_no_digit(image):
    img = cv2.imread(image)
    assert find_digit(img) is None

@pytest.mark.parametrize('image', raspicam_digit_8_images())
def test_find_image(image):
    img = cv2.imread(image)
    result = find_digit(img)
    assert result is not None

