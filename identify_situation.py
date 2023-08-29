#change numof child when yska make push to git on the database because there is there a function that receeive number of children
def identify_rolling(*imgs, num_childs):
    """
    param: list of frames
    return:  true if baby in danger
    """
    count = 0
    for img in imgs:
        if len(identifyFrontalFaces(img))==num_childs || len(identifyNose(img))==num_childs || len(identifyProfileFaces(img))==num_childs:
            count = count + 1

    if count >= 3:
        return False
    return True

