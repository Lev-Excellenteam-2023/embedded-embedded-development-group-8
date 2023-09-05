from typing import Sequence
import cv2
import numpy as np
from mp_persondet import MPPersonDet


def detect_face_using_yunet(frame: np.ndarray) -> list:
    """
    the function recognize faces in image using YuNet
    :param frame: image
    :return: (x, y, w, h) for all recognized faces in float type

    """
    height, width, _ = frame.shape
    detector = cv2.FaceDetectorYN.create("face_detection_yunet_2023mar.onnx", "", (0, 0))
    detector.setInputSize((width, height))
    _, faces = detector.detect(frame)
    # parameters: x1, y1, w, h, x_re, y_re, x_le, y_le, x_nt, y_nt, x_rcm, y_rcm, x_lcm, y_lcm
    # if faces[1] is None, no face found
    if faces is not None:
        return [face[:4] for face in faces]
    else:
        return []


def frontal_face_detection(frame: np.ndarray) -> Sequence[Sequence[int]]:
    """
    the function recognize frontal faces in image
    :param frame: image
    """
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_classifier = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    face = face_classifier.detectMultiScale(gray_image, scaleFactor=1.3, minNeighbors=5)
    return face


def profile_face_detection(frame: np.ndarray) -> Sequence[Sequence[int]]:
    """
    the function recognize profile faces in image
    :param frame: image
    """
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_classifier = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_profileface.xml"
    )
    face = face_classifier.detectMultiScale(gray_image, scaleFactor=1.3, minNeighbors=5)
    flipped = cv2.flip(gray_image, 1)
    right = face_classifier.detectMultiScale(flipped, scaleFactor=1.3, minNeighbors=5)
    for i in right:
        i[0] = frame.shape[0] - i[0]
    if len(face) == 0:
        return right
    if len(right) == 0:
        return face
    return face + right


def nose_detection(frame: np.ndarray):
    """
     the function recognize noses in image
     :param frame: image
     :return: (x, y, w, h) for all recognized noses
     """
    noseCascade = cv2.CascadeClassifier("../haarcascade_mcs_nose.xml")
    frame = frame.copy()
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    nose = noseCascade.detectMultiScale(gray_image, 1.7, 7)
    return nose


def crop_image(image, start_x, start_y, width, height):
    """
        Crop a region from the input image.

        :param image: The input image from which to crop.
        :param start_x: The starting X-coordinate of the crop region.
        :param start_y: The starting Y-coordinate of the crop region.
        :param width: The width of the crop region.
        :param height: The height of the crop region.
        :return: The cropped region of the input image.
    """
    if start_x < 0:
        start_x = 0
    if start_y < 0:
        start_y = 0

    end_y = start_y + height
    end_x = start_x + width

    if end_y > image.shape[0]:
        end_y = image.shape[0]
    if end_x > image.shape[1]:
        end_x = image.shape[1]

    return image[start_y:end_y, start_x:end_x]


def identify_full_body(img):
    backend_id = cv2.dnn.DNN_BACKEND_OPENCV
    target_id = cv2.dnn.DNN_TARGET_CPU

    # Instantiate MPPersonDet
    model = MPPersonDet(modelPath='./person_detection_mediapipe_2023mar.onnx',
                        nmsThreshold=0.3,
                        scoreThreshold=0.5,
                        topK=1,
                        backendId=backend_id,
                        targetId=target_id)

    return model.infer(img)


def movement_detection(imgs):
    """
        Detect movement in a sequence of images.

        :param images: A list of input images.
        :return: True if movement is detected in any of the images, False otherwise.
    """
    mog = cv2.createBackgroundSubtractorMOG2()
    total_pixels  = imgs[0].shape[0] * imgs[0].shape[1]
    for i, img in enumerate(imgs):
        if img is not None and not img.size == 0:  # Check if img is valid
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            fgmask = mog.apply(gray)
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            fgmask = cv2.erode(fgmask, kernel, iterations=1)
            fgmask = cv2.dilate(fgmask, kernel, iterations=1)

            contours, hierarchy = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if i == 0:
                continue
            for contour in contours:
                # Ignore small contours
                if cv2.contourArea(contour) < total_pixels  / 307:
                    continue
                return True

    return False
