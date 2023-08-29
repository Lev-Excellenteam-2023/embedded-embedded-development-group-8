from typing import Sequence
import cv2
import numpy as np



def detect_face_using_yunet(frame:np.ndarray)->list:
    """
    the function recognize faces in image
    :param frame:
    :return:
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
def frontal_face_detection(frame:np.ndarray) -> Sequence[Sequence[int]]:
    """
    the function recognize frontal faces in image
    :param img: image
    :return: (x, y, w, h) for all recognized faces
    """
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_classifier = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    face = face_classifier.detectMultiScale(gray_image, scaleFactor=1.3, minNeighbors=5)
    return face
def profile_face_detection(frame:np.ndarray) -> Sequence[Sequence[int]]:
    """
    the function recognize profile faces in image
    :param img: image
    :return: (x, y, w, h) for all recognized faces
    """
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_classifier = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_profileface.xml"
    )
    face = face_classifier.detectMultiScale(gray_image, scaleFactor=1.3, minNeighbors=5)
    flipped = cv2.flip(gray_image, 1)
    right=face_classifier.detectMultiScale(flipped, scaleFactor=1.3, minNeighbors=5)
    for i in right:
        i[0]=frame.shape[0]-i[0]
    if len(face)==0:
        return right
    if len(right)==0:
        return face
    return face+right

def nose_detection(frame:np.ndarray):
    """
     the function recognize noses in image
     :param img: image
     :return: (x, y, w, h) for all recognized noses
     """
    noseCascade = cv2.CascadeClassifier("../haarcascade_mcs_nose.xml")
    frame = frame.copy()
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    nose = noseCascade.detectMultiScale(gray_image, 1.7, 7)
    return nose

