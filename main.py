from camera import capture_5_images
import identify_situation


def main():
    while True:
        num_childs = input("Enter number of babies in the class: ")
        images = capture_5_images()

        if (identify_rolling(images, num_childs)):# if true there is a danger
            pass
            #send_image according to how we send the signal




if __name__ == "__main__":
    main()