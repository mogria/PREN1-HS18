import cv2
import random
import numpy


class DigitGenerator:

    def get_fonts(self):
        fonts = {
           'hershey_triplex': cv2.FONT_HERSHEY_TRIPLEX,
           'hershey_plain': cv2.FONT_HERSHEY_PLAIN,
           'hershey_duplex': cv2.FONT_HERSHEY_DUPLEX,
           'hershey_complex': cv2.FONT_HERSHEY_COMPLEX,
           'hershey_simplex': cv2.FONT_HERSHEY_SIMPLEX,
           'hershey_script_complex': cv2.FONT_HERSHEY_SCRIPT_COMPLEX,
           'hershey_script_simplex': cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
        }

        for font_name, font in fonts:
            fonts[font_name + "_italic"] = font | cv2.FONT_ITALIC

        return fonts

    def generate_digit_image(self, size, font, font_size, digit):
        image = numpy.zeros((size, size), numpy.uint8)
        image[:] = 255 # make background white
        position = (0, 0) # from bottom left
        color = 0
        thickness = 2
        cv2.putText(image, str(number), position, font, font_size, 255, thickness, cv2.LINE_AA)

if __name__ == '__main__':

