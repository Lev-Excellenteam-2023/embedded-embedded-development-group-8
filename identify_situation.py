#change numof child when yska make push to git on the database because there is there a function that receeive number of children
import cv2

import image_processing
import consts
from scipy.ndimage import rotate

def identify_rolling(imgs, num_childs):
    """
    param: list of frames
    return:  true if baby in danger
    """
    angle=90
    count = 0
    for source_img in imgs:
        new=source_img
        count_rotate_image = 0
        count_face=0
        for i in range(int(360/angle)):
            new = rotate_image(new,angle*i)
            count_face=count_face+len(image_processing.detect_face_using_yunet(new))
        if count_face==int(num_childs):
            count = count + 1
    if count >= consts.OK_IMAGES:
        return False
    return True

def rotate_image(img,angle):
    height, width = img.shape[:2]
    center = (width // 2, height // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_image = cv2.warpAffine(img, rotation_matrix, (width, height))
    return rotated_image