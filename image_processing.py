from typing import Sequence
import cv2
from matplotlib import pyplot as plt

def detect_face_using_yunet(frame):
    height, width, _ = frame.shape
    detector = cv2.FaceDetectorYN.create("face_detection_yunet_2023mar.onnx", "", (0, 0))
    detector.setInputSize((width, height))
    _, faces = detector.detect(frame)
    # if faces[1] is None, no face found
    faces1=[]
    if faces is not None:
        for i,face in enumerate(faces):
            # parameters: x1, y1, w, h, x_re, y_re, x_le, y_le, x_nt, y_nt, x_rcm, y_rcm, x_lcm, y_lcm
            faces1.append(face[:4])
    return faces1
def frontal_face_detection(frame) -> Sequence[Sequence[int]]:
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
def profile_face_detection(frame) -> Sequence[Sequence[int]]:
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

def nose_detection(frame):
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

#def predict_age(frame,start_x,start_y,w,h):
    """

    :param frame:
    :param start_x:
    :param start_y:
    :param w:
    :param h:
    :return:
    """
   # frame = frame.copy()
    #end_x = start_x + w
    #end_y = start_y + h
    #face_img = frame[start_y: end_y, start_x: end_x]
    # image --> Input image to preprocess before passing it through our dnn for classification.
    #blob = cv2.dnn.blobFromImage(
     #   image=face_img, scalefactor=1.0, size=(227, 227),
      #  mean=age_model.MODEL_MEAN_VALUES, swapRB=False
    #)
    # Predict Age
    #age_model.age_net.setInput(blob)
    #age_preds = age_model.age_net.forward()
    #for i in range(age_preds[0].shape[0]):
     #   print(f"{age_model.AGE_INTERVALS[i]}: {age_preds[0, i] * 100:.2f}%")
    #i = age_preds[0].argmax()
    #age = age_model.AGE_INTERVALS[i]
    #age_confidence_score = age_preds[0][i]
    #label = f"Age:{age} - {age_confidence_score * 100:.2f}%"
    #return age





