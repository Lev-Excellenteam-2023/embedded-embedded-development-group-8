# change numof child when yska make push to git on the database because there is there a function that receeive number of children
import cv2
import image_processing
import consts
import numpy as np


def identify_rolling(imgs:list, num_childs:int)->bool:
    """
    Detect Baby's Rolling Behavior
    param: list of frames
    return:  true if baby has rolled over.
    """
    angle_of_rotating_image = 90
    count_of_ok_images = 0
    for source_img in imgs:
        rotated_image = source_img
        count_of_faces_detected = 0
        for _ in range(int(360 / angle_of_rotating_image)):
            rotated_image = rotate_image(rotated_image, angle_of_rotating_image)
            count_of_faces_detected = count_of_faces_detected + len(
                image_processing.detect_face_using_yunet(rotated_image))
        if count_of_faces_detected == int(num_childs):
            count_of_ok_images = count_of_ok_images + 1
    if count_of_ok_images >= consts.OK_IMAGES:
        return False
    return True


def identify_if_someone_didnt_move(images:list)->bool:
    """
    Crop images for each person and store them in the person info dictionary for each person.
    Check if the person moved.

    :param images: A list of input images.
    :return: True if movement is not detected in any person, False otherwise.
    """
    person_info = {}

    for img in images:
        full_body_results = image_processing.identify_full_body(img)

        for idx, person in enumerate(full_body_results):
            if idx in person_info:
                hip_point, full_body = person_info[idx]["landmarks"]
            else:
                person_landmarks = person[4:-1].reshape(4, 2).astype(np.int32)
                hip_point = person_landmarks[0]
                full_body = person_landmarks[1]

            radius = np.linalg.norm(hip_point - full_body).astype(np.int32)
            cropped_image = image_processing.crop_image(
                img, hip_point[0] - radius, hip_point[1] - radius, 2 * radius, 2 * radius
            )

            if idx in person_info:
                person_info[idx]["images"].append(cropped_image)
            else:
                person_info[idx] = {"images": [cropped_image], "landmarks": person_landmarks[:2]}

    for idx in person_info:
        if len(person_info[idx]["images"]) < consts.NUM_OF_IMAGES:
            continue
        if not image_processing.movement_detection(person_info[idx]["images"]):
            return True
    return False


def rotate_image(img: np.ndarray, angle: float) -> np.ndarray:
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
