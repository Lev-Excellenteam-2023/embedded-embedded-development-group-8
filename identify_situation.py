#change numof child when yska make push to git on the database because there is there a function that receeive number of children
import cv2
import image_processing
import consts


def identify_rolling(imgs, num_childs):
    """
    Detect Baby's Rolling Behavior
    param: list of frames
    return:  true if baby has rolled over.
    """
    angle_of_rotating_image=90
    count_of_ok_images= 0
    for source_img in imgs:
        rotated_image=source_img
        count_of_faces_detected=0
        for _ in range(int(360/angle_of_rotating_image)):
            rotated_image = rotate_image(rotated_image,angle_of_rotating_image)
            count_of_faces_detected=count_of_faces_detected+len(image_processing.detect_face_using_yunet(rotated_image))
        if count_of_faces_detected==int(num_childs):
            count_of_ok_images = count_of_ok_images + 1
    if count_of_ok_images >= consts.OK_IMAGES:
        return False
    return True

def rotate_image(img,angle):
    """
    Rotate an image by a specified angle.
    :param img: the img to rotate
    :param angle:  The angle (in degrees) by which to rotate the image.
    :return: the rotated image
    """
    height, width = img.shape[:2]
    center = (width // 2, height // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_image = cv2.warpAffine(img, rotation_matrix, (width, height))
    return rotated_image