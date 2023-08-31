import threading

import camera
from firbase_func import  get_nursery

from camera import capture_5_images
import identify_situation
from telgram_bot import start_notification,start_telegram_warks
# from firbase_func import update_notification


def main():

    # num_childs = int(input("Enter number of babies in the class: "))
    if get_nursery(653029654)!=None:
        num_childs = get_nursery(653029654).num_babies
    num_childs = int(input("Enter number of babies in the class: "))

    while True:
        images = camera.capture_5_images()
        if (identify_situation.identify_rolling(images, num_childs)):# if true there is a danger
            print("danger")
            start_notification(True)
        else:
            print("ok")
            start_notification(False)

            # update_notification(True)
            #send_image according to how we send the signal
    # t1.join()




if __name__ == "__main__":
    main()
    # t1 = threading.Thread(target=start_telegram_warks, args=())
    # t2 = threading.Thread(target=main, args=())
    # t1.start()
    # t2.start()
    # t1.join()
    # t2.join()