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

    def read_image(self, image_file):
        return cv2.imread(image_file, cv2.IMREAD_GRAYSCALE)

    """ get the label from the filename of the image file
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
                model = self.read_image(digit_model.make_path(directory, "png"))
                digit_model.set_model(model, number_of_training_images)

    """ get the total amount of training images used to train the model """
    def get_number_of_training_images(self):
        return sum([ digit_model.number_of_training_images for digit_model in self.digit_models ])

    """ add a training image. The training label for which digit it
        is checked on the filename. See DigitDetector.get_label().
        This method only handles BGR images, but they will be converted
        to greyscale!"""
    def train(self, imagefiles):
        for imagefile in imagefiles:
            label = self.get_label(imagefile)
            image = self.read_image(imagefile)
            self.digit_models[label].train(image)

    def get_matches(self, image):
        return [ digit_model.match(image) for digit_model in self.digit_models ]

    """ return the label of the digit model that matches
        best with image """
    def detect_digit(self, image=None, image_file=None):
        if self.get_number_of_training_images() <= 0:
            raise NotTrainedError()

        if image_file is None and image is None:
            raise ValueError("image")

        if image is None and image_file is not None:
            image = self.read_image(image_file)

        return DetectionResult(self.get_matches(image))

class DetectionResult:
    def __init__(self, matches):
        self.matches = matches
        self.confidence = max(matches)
        self.detected_digit = matches.index(self.confidence)

    def __str__(self):
        return "confidences: " + str(self.matches) + "\nmatch: " + str(self.detected_digit) + ", confidence: " + str(self.confidence)

""" Represents a model of a single digit.
    The label says which digit it is."""
class DigitModel:

    def __init__(self, label, model_resolution):
        self.label = label
        self.model_resolution = model_resolution
        self.number_of_training_images = 0
        self.model = numpy.zeros((model_resolution, model_resolution))

    def normalize_image(self, image):
        return cv2.resize(image, (self.model_resolution, self.model_resolution))

    """ create a unique path for this DigitModel in some directory.
        Used to get the path for loading and saving the model"""
    def make_path(self, directory, extension = "png"):
        return os.path.join(directory, str(self.label) + "." + extension)

    """ instead of training the model data can be set via this method.
        Make sure the number of training images is correct, else further
        training will not work correctly."""
    def set_model(self, model, number_of_training_images):
        self.number_of_training_images = number_of_training_images
        self.model = model

    """ train this digit model. The image has to belong to the
        label given in the constructor. """
    def train(self, image):
        image = self.normalize_image(image)
        self.number_of_training_images += 1
        image_relevance = 1.0 / self.number_of_training_images
        model_relevance = 1.0 - image_relevance
        weighted_model = image * image_relevance
        self.model = (self.model * model_relevance) + (image * image_relevance)

    """ returns a value between 0 and 1 how good the image matches
        this digit model. """
    def match(self, image):
        image = self.normalize_image(image)
        return 1 - (numpy.average(numpy.abs(numpy.subtract(self.model, image))) / 256.0)

class DetectionError(Exception):
    pass

class NotTrainedError(DetectionError):

    def __init__(self,):
        self.message = "first train or load a model before you can match against it!"



def usage(name):
    print("DIGIT DETECTOR USAGE:")
    print(" ", name, "train", "training_dir/", "model_output_dir/")
    print("    trains the digit detector with training data from training_dir")
    print("    and puts the resulting model into the model_output_dir.")
    print("    It will resume training if the model_output_dir does not exist,")
    print("    else it will create the directory with the trained model in it.")
    print("")
    print(" ", name, "detect", "model_dir/", "image_dir/")
    print("    trains the digit detector with training data from training_dir")
    print("    and puts the resulting model into the model_output_dir")
    sys.exit(1)

def main(argv):
    if len(argv) <= 3:
        usage(argv[0])
        return

    digit_detector = DigitDetector(500)

    if argv[1] == "train":
        print("Starting in TRANING mode")
        if os.path.exists(argv[3]):
            print("Loading model from directory", argv[3])
            digit_detector.load_model(argv[3])
        else:
            print("Creating model output directory", argv[3])
            os.makedirs(argv[3])
        image_files = imageutil.read_image_folder(argv[2])
        print("Training with the following image files")
        for f in image_files:
            print("-", f)
        digit_detector.train(image_files)
        if not os.path.exists(argv[3]):
            os.makedirs(argv[3])
        digit_detector.save_model(argv[3])
    elif argv[1] == "detect":
        print("Starting in DETECT mode")
        print("Loading model from directory", argv[2])
        digit_detector.load_model(argv[2])
        print("Loading files from directory", argv[3])
        image_files = imageutil.read_image_folder(argv[3])
        for image_file in image_files:
            print(image_file + ":", digit_detector.detect_digit(image_file=image_file))
    else:
        usage(argv[0])
        return

if __name__ == '__main__':
    import sys
    import imageutil
    main(sys.argv)
