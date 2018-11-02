import pytest
from mollyvision.digit_detector import DigitDetector, NotTrainedError
from mollyvision import imageutil


@pytest.fixture
def training_files():
    return imageutil.read_image_folder("src/poc/opencv")

# TODO: use other files for validation, but as of
# now we don't have em
@pytest.fixture
def validation_files():
    return imageutil.read_image_folder("src/poc/opencv")

@pytest.fixture
def digit_detector():
    return DigitDetector(500);

@pytest.fixture
def trained_digit_detector(digit_detector, training_files):
    digit_detector.train(training_files)
    return digit_detector

def test_get_label(digit_detector):
    assert 0 == digit_detector.get_label("somedir1/0.jpg")
    assert 1 == digit_detector.get_label("somedir1/1.jpg")
    assert 8 == digit_detector.get_label("somedir1/8someothertext.jpg")
    assert 9 == digit_detector.get_label("somedir1/sometext9.jpg")
    assert 7 == digit_detector.get_label("somedir1/testtest7smeothertext.jpg")
    assert None == digit_detector.get_label("somedir1/testtestsmeothertext.jpg")

def test_model_resolution():
    pass

def test_get_number_of_training_images(trained_digit_detector, training_files):
    assert len(training_files) == trained_digit_detector.get_number_of_training_images()

def test_get_number_of_training_images__save_and_load(trained_digit_detector, tmpdir):
    trained_digit_detector.save_model(tmpdir)
    expected_number_of_training_images = trained_digit_detector.get_number_of_training_images()
    trained_digit_detector.load_model(tmpdir)
    assert expected_number_of_training_images == trained_digit_detector.get_number_of_training_images()

def test_detect_digit(trained_digit_detector, validation_files):
    for validation_file in validation_files:
        detection_result = trained_digit_detector.detect_digit(image_file=validation_file)
        label = trained_digit_detector.get_label(validation_file)
        assert label == detection_result.detected_digit
        assert detection_result.confidence > 0.98

def test_detect_digit__no_model(digit_detector):
    with pytest.raises(NotTrainedError):
        digit_detector.detect_digit("some_inexistent_file")

def test_detect_digit__no_image(trained_digit_detector):
    with pytest.raises(ValueError):
        trained_digit_detector.detect_digit(None)

def test_detect_digit__reload_model(trained_digit_detector, tmpdir):
    # this needs an easy way to compare detection results
    pass
