import cv2

def main():
    cam = cv2.VideoCapture(0);
    while True:
        ret_val, img = cam.read()
        cv2.imshow('opencv capture', img);
        if cv2.waitKey(1) == 27:
            break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
