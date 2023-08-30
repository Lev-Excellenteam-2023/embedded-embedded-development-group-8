import cv2
import os
import time
import consts



def capture_5_images():
    """
    :return: list of frames
    """

    frame_list = []
    # Create an object to hold reference to camera video capturing
    capture = cv2.VideoCapture(0)

    while True:

        if capture.isOpened():
            ret, frame = capture.read()  # capture a frame from live video
            time.sleep(consts.TIME_BETWEEN_IMAGES)
            if ret:
                frame_list.append(frame)
                # we can delete this after it is just to see that it take picture
                #cv2.imshow("Frame", frame)  # show captured frame

                # press 'q' to break out of the loop
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

                if len(frame_list) == consts.NUM_OF_IMAGES:
                    return frame_list

            else:
                print("Error : Failed to capture frame")

        else:
            print("Cannot open camera")

