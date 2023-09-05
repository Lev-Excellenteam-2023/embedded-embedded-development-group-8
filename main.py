
import camera


from camera import capture_5_images
import identify_situation



def main():
    num_childs = input("Enter number of babies in the class: ")
    while True:
        images = camera.capture_5_images()

        if (identify_situation.identify_rolling(images, num_childs)):  # if true there is a danger
            print("baby in danger")
        else:
            print("no baby in danger")
        if(identify_situation.identify_if_someone_didnt_move(images)):
            print("someone not moving")
        else:
            print("everyone moving")






if __name__ == "__main__":
    main()