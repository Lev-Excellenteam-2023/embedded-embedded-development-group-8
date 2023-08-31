import camera
from firbase_func import  get_num_babies
import identify_situation
from telgram_bot import start_notification


def main():
    num_childs=get_num_babies()
    while True:
        images = camera.capture_5_images()
        if (identify_situation.identify_rolling(images, num_childs)):# if true there is a danger
            print("danger")
            start_notification(True)
        else:
            print("ok")
            start_notification(False)




if __name__ == "__main__":
    main()