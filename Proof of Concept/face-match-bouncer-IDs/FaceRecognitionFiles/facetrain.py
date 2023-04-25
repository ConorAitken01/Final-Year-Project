import os
import cv2
import numpy as np
from PIL import Image

# LBP(Local Binary Patterns) are one way to extract characteristic features of an object
# LBPHFaceRecognizer extracts faces
recognizer = cv2.face.LBPHFaceRecognizer_create()
# set the path to the images of people folder
path = '../dataSet'


# Function to get Images with the ID
def getImagesWithID(path):
    imagepaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    IDs = []
    for imagepath in imagepaths:
        # if there is a .DS_Store file in the dataSet folder then this if statement ignores it
        if ".DS_Store" in imagepath:
            print("Junk!")
        else:
            faceImg = Image.open(imagepath).convert('L')
            faceNp = np.array(faceImg, 'uint8')
            ID = int(os.path.split(imagepath)[-1].split('.')[1])
            faces.append(faceNp)
            IDs.append(ID)
            # show the training
            cv2.imshow("training", faceNp)
            cv2.waitKey(1)
    return np.array(IDs), faces


IDs, faces = getImagesWithID(path)
# train the recognizer with the faces and IDs so it can link them together as that face #1 is the #1 profile
recognizer.train(faces, IDs)
# save the recognizer to the trainningData.yml file
recognizer.save('../recognizer/trainningData.yml')
cv2.destroyAllWindows()
