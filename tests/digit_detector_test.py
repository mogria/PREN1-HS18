import pytest
from mollyvision.digit_detector import DigitDetector, NotTrainedError
from mollyvision import imageutil

@pytest.fixture
def test_files():
    pass

@pytest.fixture
def training_files():
    pass

@pytest.fixture
def digit_detector():
    return DigitDetector(500);

def test_get_label(digit_detector):
    assert 0 == digit_detector.get_label("somedir1/0.jpg")
    assert 1 == digit_detector.get_label("somedir1/1.jpg")
    assert 8 == digit_detector.get_label("somedir1/8someothertext.jpg")
    assert 9 == digit_detector.get_label("somedir1/sometext9.jpg")
    assert 7 == digit_detector.get_label("somedir1/testtest7smeothertext.jpg")
    assert None == digit_detector.get_label("somedir1/testtestsmeothertext.jpg")

def test_model_resolution():
    pass

def test_get_number_of_training_images(digit_detector):
    image_files = imageutil.read_image_folder("src/poc/opencv")
    digit_detector.train(image_files)
    assert len(image_files) == digit_detector.get_number_of_training_images()

def test_get_number_of_training_images__save_and_load(digit_detector, tmpdir):
    image_files = imageutil.read_image_folder("src/poc/opencv")
    digit_detector.train(image_files)
    digit_detector.save_model(tmpdir)
    expected_number_of_training_images = digit_detector.get_number_of_training_images()
    digit_detector.load_model(tmpdir)
    assert expected_number_of_training_images == digit_detector.get_number_of_training_images()

def test_detect_digit(digit_detector):
    pass
    # digit_detector.detect_digit()

def test_detect_digit__no_model(digit_detector):
    with pytest.raises(NotTrainedError):
        digit_detector.detect_digit("some_inexistent_file")

def test_detect_digit__no_image(digit_detector):
    with pytest.raises(NotTrainedError):
        digit_detector.detect_digit(None)

def test_detect_digit__reload_model(digit_detector, tmpdir):
    with pytest.raises(NotTrainedError):
        digit_detector.detect_digit(None)
