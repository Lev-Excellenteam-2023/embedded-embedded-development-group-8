#change numof child when yska make push to git on the database because there is there a function that receeive number of children

import image_processing
import consts

def identify_rolling(*imgs, num_childs):
    """
    param: list of frames
    return:  true if baby in danger
    """
    count = 0
    for img in imgs:

        if (len(image_processing.frontal_face_detection(img)) == num_childs) or \
                (len(image_processing.nose_detection(img)) == num_childs) or \
                (len(image_processing.profile_face_detection(img)) == num_childs) or \
                (len(image_processing.detect_face_using_yunet(img)) == num_childs):
            count = count + 1

    if count >= consts.OK_IMAGES:
        return False
    return True

