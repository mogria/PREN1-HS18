import cv2
import numpy

class DigitFinder:

    def __init__(self, template):
        self.template = template
        self.mask = self.create_mask(template)

    def create_mask(self, template):
        shape = template.shape
        print(shape)
        mask = numpy.zeros(shape)
        return mask

    def find_digit(self, image):
        result = None
        # TM_SQDIFF TM_CCORR_NORMED works as method when using a mask
        cv2.matchTemplate(image, self.template, result, cv2.TM_SQDIFF, self.mask)


def usage(programname):
    print("Usage: {} image" % programname)

def main(argv):
    if len(argv) <= 1:
        usage(argv[0])
        sys.exit(1)

    digit_finder = DigitFinder()
    find_digit(sys.argv[1])

if __name__ == '__main__':
    import sys
    main(sys.argv[0])
