import cv2
import os
import time

# I have to change with the consts



def capture_5_images():
    """
    :return: list of frames
    """

    frame_list = []
    # Create an object to hold reference to camera video capturing
    vidcap = cv2.VideoCapture(0)

    while True:

        if vidcap.isOpened():
            ret, frame = vidcap.read()  # capture a frame from live video
            time.sleep(1)
            if ret:
                while (True):
                    frame_list.append(frame)
                    cv2.imshow("Frame", frame)  # show captured frame

                    # press 'q' to break out of the loop
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                    if len(frame_list) == 5:
                        return frame_list

            else:
                print("Error : Failed to capture frame")

        else:
            print("Cannot open camera")


def main():
    capture_5_images()

if __name__ == "__main__":
    main()








