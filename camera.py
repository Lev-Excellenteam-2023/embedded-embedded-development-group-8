import cv2
import os
import time


def take_image():

    while True:
        yield capture_of_5_images()


def capture_of_5_images():
    frame_list = []
    # Create an object to hold reference to camera video capturing
    vidcap = cv2.VideoCapture(0)

    while True:  # every second

        # check if connection with camera is successfully
        if vidcap.isOpened():
            ret, frame = vidcap.read()  # capture a frame from live video
            time.sleep(1)
            # check whether frame is successfully captured
            if ret:
                # continue to display window until 'q' is pressed
                while (True):
                    frame_list.append(frame)
                    cv2.imshow("Frame", frame)  # show captured frame

                    # press 'q' to break out of the loop
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                    if len(frame_list) == 5:
                        return frame_list



            # print error if frame capturing was unsuccessful
            else:
                print("Error : Failed to capture frame")
        # print error if the connection with camera is unsuccessful
        else:
            print("Cannot open camera")


def main():
    capture_of_5_images()

if __name__ == "__main__":
    main()








