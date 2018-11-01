import cv2
import numpy
import os


"""
This class is a trainable digit detector.

 - Train it by calling train() with a list of images.
 - You can export the training model by using
 - This class will scale the passed images to a quadratic size given
   by model_resolution in the constructor

Idea taken from:
- https://medium.com/@gsari/digit-recognition-with-opencv-and-python-cbf963f7e2d0
"""
class DigitDetector:
    DIGITS = range(10)

    def __init__(self, model_resolution):
        self.digit_models = [ DigitModel(label, model_resolution) for label in self.DIGITS ]
        self.model_resolution = model_resolution

    """ get the label from the filename of the imagefile
        e.g. if it contains a 0 then the label is 0, etc. for any digit """
    def get_label(self, imagefile):
        filename = os.path.basename(imagefile)
        for digit in self.DIGITS:
            if str(digit) in filename:
                return digit

        return None

    """ save the model to a directory with an image and an info file
        for every label (e.g. 0-9)"""
    def save_model(self, directory):
        for digit_model in self.digit_models:
            with open(digit_model.make_path(directory, "info"), "w") as f:
                f.write(str(digit_model.number_of_training_images))
            cv2.imwrite(digit_model.make_path(directory, "png"), digit_model.model)

    """ load a model saved with the save_model() method """
    def load_model(self, directory):
        for digit_model in self.digit_models:
            with open(digit_model.make_path(directory, "info"), "r") as f:
                number_of_training_images = int(f.read())
                model = cv2.imread(digit_model.make_path(directory, "png"))
                digit_model.set_model(model, number_of_training_images)

    """ get the total amount of training images used to train the model """
    def get_number_of_training_images(self):
        return sum([ digit_model.number_of_training_images for digit_model in self.digit_models ])

    """ add a training image. The training label for which digit it
        is checked on the filename. See DigitDetector.get_label().
        This method only handles BGR images, but they will be converted
        to grayscale!"""
    def train(self, imagefiles):
        for imagefile in imagefiles:
            label = self.get_label(imagefile)
            image = cv2.imread(imagefile)
            self.digit_models[label].train(image)

    """ return the label of the digit model that matches
        best with image """
    def detect_digit(self, image):
        if self.get_number_of_training_images() <= 0:
            raise NotTrainedError()

        matches = [ digit_model.match(image) for digit_model in self.digit_models ]
        return max(matches)


""" Represents a model of a single digit.
    The label says which digit it is."""
class DigitModel:

    def __init__(self, label, model_resolution):
        self.label = label
        self.model_resolution = model_resolution
        self.number_of_training_images = 0
        self.model = numpy.zeros((model_resolution, model_resolution, 1))

    def make_path(self, directory, extension = "png"):
        return os.path.join(directory, str(self.label) + "." + extension)

    def set_model(self, model, number_of_training_images):
        self.number_of_training_images = number_of_training_images
        self.model = model

    """ train this digit model. The image has to belong to the
        label given in the constructor. """
    def train(self, image):
        image = cv2.resize(image, (self.model_resolution, self.model_resolution))
        self.number_of_training_images += 1

    """ returns a value between 0 and 1 how good the image matches
        this digit model. """
    def match(self, image):
        cv.matchTemplate(self.save_model)
        return 0

class DetectionError(Exception):
    pass

class NotTrainedError(DetectionError):

    def __init__(self,):
        self.message = "first train or load a model before you can match against it!"

