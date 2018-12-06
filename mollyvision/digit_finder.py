import cv2
import numpy
import time

# cv2.matchTemplate() might also be an option if we know how far
# and from what perspective we see the digit. Eg:
#       # TM_SQDIFF TM_CCORR_NORMED works as method when using a mask
#       cv2.matchTemplate(image, self.template, result, cv2.TM_SQDIFF, self.mask)
#
# But the be other option is searching for polygons. As done there.
# Inspired by: https://stackoverflow.com/questions/37942132/opencv-detect-quadrilateral-in-python

def check_rectangle_points_diff(pdiff):
    s = pdiff[0] # short differnce (e.g. when should be on the same coordinate)
    l = pdiff[1] # long difference (this is the length of the rectangle)
    return abs(s) * 10 < abs(l)

def contour_filter(approx):
    # instead of just returning true here
    # the contour could be checked to remove 
    # countours which are obviously wrong
    area = cv2.contourArea(approx)
    print(area)
    return area > 200


    print(approx)

    pdiffs = [
        (approx[0] - approx[1])[0],
        (approx[3] - approx[2])[0],
        (approx[1] - approx[2])[0],
        (approx[3] - approx[0])[0],
    ]
    print(pdiffs)

    return len([pdiff for pdiff in pdiffs if check_rectangle_points_diff(pdiff)]) ==  4

def contour_to_transform_rect(approx):
    # taken from:
    #   https://www.pyimagesearch.com/2014/05/05/building-pokedex-python-opencv-perspective-warping-step-5-6/
    # now that we have our screen contour, we need to determine
    # the top-left, top-right, bottom-right, and bottom-left
    # points so that we can later warp the image -- we'll start
    # by reshaping our contour to be our finals and initializing
    # our output rectangle in top-left, top-right, bottom-right,
    # and bottom-left order
    pts = approx.reshape(4, 2)
    rect = numpy.zeros((4, 2), dtype = "float32")

    # the top-left point has the smallest sum whereas the
    # bottom-right has the largest sum
    s = pts.sum(axis = 1)
    rect[0] = pts[numpy.argmin(s)]
    rect[3] = pts[numpy.argmax(s)]

    # compute the difference between the points -- the top-right
    # will have the minumum difference and the bottom-left will
    # have the maximum difference
    diff = numpy.diff(pts, axis = 1)
    rect[1] = pts[numpy.argmin(diff)]
    rect[2] = pts[numpy.argmax(diff)]

    # multiply the rectangle by the original ratio
    # rect *= ratio
    print(approx)
    return rect

def find_digit(image):
    start_time = time.time()
    # cv2.imshow('orig', image)
    # cv2.waitKey()
    im_bw = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    # cv2.imshow('bw',im_bw)
    # cv2.waitKey()
    # the threshold of 75 seems to be a pretty good value
    # for pictures taken with the right configuration of
    # the raspi cam, altough in the future you might try
    # cv2.THRES_OTSU:
    # https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_thresholding/py_thresholding.html#otsus-binarization
    # but keep in mind the better the threshold (and the input image)
    # the faster the algorihm, because a lot more wrong contours
    # will be found.
    thres, im_thresh = cv2.threshold(im_bw, 75, 255, cv2.THRESH_BINARY)
    cv2.imwrite('threshold.jpg', im_thresh)
    # im_thresh = cv2.adaptiveThreshold(im_bw, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11,2)
    # cv2.imshow('bw', im_thresh)
    #cv2.waitKey()
    (im2, cnts, _) = cv2.findContours(im_thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.imshow('contour', im2)
    # cv2.waitKey()
    cnts=sorted(cnts, key = cv2.contourArea, reverse = True)[:10]

    # maybe abort here early if the contour area is too big
    # too low??

    # loop over our contours
    for c in cnts:
        # print("countour", c)
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.1 * peri, True)
        if len(approx) == 4 and contour_filter(approx):
            # cv2.drawContours(image, [approx], -1, (0,255,0), 3)
            # cv2.imshow('countours drawn', image)
            # cv2.waitKey()
            # cv2.imwrite('countour.jpg', image)
            # print("time elapsed", time.time() - start_time)
            return approx

            # this may be useful if something overlaps
            # hull = cv2.convexHull(approx,returnPoints = False)
            # defects = cv2.convexityDefects(approx,hull)

            # threshold = 1000  #? ????
            # if defects is not None:
                # sum_of_defects=0
                # for i in range(defects.shape[0]):
                    # s,e,f,d = defects[i,0]
                    # sum_of_defects=sum_of_defects+d

                # print(sum_of_defects)
                # if sum_of_defects <= threshold:
                    # print("approx is convex")
                # else:
                    # print("approx is not convex")

    return None

def transform(image, contour, image_size):
    pts1 = numpy.float32( contour_to_transform_rect(contour))
    pts2 = numpy.float32([[0,0],[image_size,0],[0,image_size],[image_size,image_size]])
    M = cv2.getPerspectiveTransform(pts1,pts2)
    return cv2.warpPerspective(image,M,(image_size,image_size))

def usage(programname):
    print("Usage: {} input-image transformed-output-image" % programname)

def main(argv):
    if len(argv) <= 2:
        usage(argv[0])
        sys.exit(1)

    img = cv2.imread(argv[1])
    position_rectangle = find_digit(img)
    transformed = transform(img, position_rectangle, 100)
    # cv2.imshow('transformed', transformed)
    # cv2.waitKey()
    cv2.imwrite(argv[2], transformed)

if __name__ == '__main__':
    import sys
    main(sys.argv)
