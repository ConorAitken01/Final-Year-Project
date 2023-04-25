import os
import numpy as np
from PIL import Image
import cv2
import sqlite3
import pytesseract
from datetime import datetime, date


# Path to the location of the Tesseract-OCR executable/command
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Set up pytesseract with the desired configuration
config = "--psm 6"  # Use page segmentation mode 6 (Assume a single uniform block of vertically aligned text of variable sizes.)

# make connection to database
conn = sqlite3.connect("FaceBase.db")

# Get the HaarCascade Classifier onto a variable for easier use
faceDetect = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# LBP(Local Binary Patterns) are one way to extract characteristic features of an object
# LBPHFaceRecognizer extracts faces
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("recognizer/trainningData.yml")
# set the path to the images of people folder
path = 'dataSet'

# connecting to camera
cam = cv2.VideoCapture(0)

# setting the font type, size and colour
fontface = cv2.FONT_HERSHEY_SIMPLEX
fontscale = 1
fontcolor = (0, 255, 0)


# function for inserting ID, Name and Age into database
def insert(IdIn, NameIn, AgeIn):
    params = (IdIn, NameIn, AgeIn)
    # secure code using ? instead of putting in the parameters directly
    cmd = "INSERT INTO People(ID,Name,Age) Values(?, ?, ?)"
    conn.execute(cmd, params)

    conn.commit()


def getAge():
    # Loop over frames from the video stream
    # Exit the loop if the 'q' key is pressed
    while (cv2.waitKey(1) != ord('q')):
        # Capture a frame from the video stream
        ret, frame = cam.read()

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Use pytesseract to detect text in the grayscale image
        text = pytesseract.image_to_string(gray, config=config)
        cv2.imshow("Show Passport Text to Camera", frame)

    start_index = text.find("IRISH")
    dobWithIrish = text[start_index + 6:start_index + 21]

    dob = (dobWithIrish[:3] + dobWithIrish[7:])
    dateOfBirth = datetime.strptime(dob, '%d %b %Y')

    today = date.today()
    ageOut = today.year - dateOfBirth.year - ((today.month, today.day) < (dateOfBirth.month, dateOfBirth.day))
    return ageOut


def addUser(nameIn, ageIn):
    # incrementing the last id number for the next profile
    cursor = conn.execute("SELECT * FROM People ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()
    # if no profiles in the database then make the id number 1
    if (result == None):
        Id = 1
    else:
        Id = int(result[0]) + 1
    print("ID: ", Id)
    name = nameIn
    age = ageIn
    insert(Id, name, age)

    # starting the counter for number of pictures to be taking of the person for training
    sampleNum = 0
    # tried 50 picture, found out 100 is more accurate
    while (sampleNum < 100):
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # input the image followed by the scale factor then the min neighbours
        # scale factor is how much the image size is reduced at each image scale
        # min neighbours is how many neighbours each candidate rectangle should have retain it
        faces = faceDetect.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            sampleNum = sampleNum + 1
            cv2.imwrite("dataSet/User." + str(Id) + "." + str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.waitKey(100)
        cv2.imshow("Show Passport Photo to Camera", img)
        cv2.waitKey(1)


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
            cv2.waitKey(10)
    return np.array(IDs), faces


# this function gets the information on a person stored in the database using the ID key
def getProfile(idIn):
    cmd = "SELECT * FROM People WHERE ID=" + str(idIn)
    cursor = conn.execute(cmd)
    profile = None
    for row in cursor:
        profile = row
    return profile


def FaceRecognition():
    # Close the window when Q is pressed
    while (cv2.waitKey(1) != ord('q')):
        ret, img = cam.read()
        # converting face images into gray for better face recognition results
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceDetect.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            # make a rectangle around the face
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            id, conf = recognizer.predict(gray[y:y + h, x:x + w])
            # getting the profile of the person that the recognizer thinks it is
            print(id)
            # conf is the confidence level which is distance between the stream image and stored image
            print(conf)
            # show unknown person if not trained
            if (conf < 70):
                profile = getProfile(id)
                if (profile != None):
                    cv2.putText(img, "Name : " + str(profile[1]), (x, y + h + 20), fontface, fontscale, fontcolor)
                    cv2.putText(img, "Age : " + str(profile[2]), (x, y + h + 45), fontface, fontscale, fontcolor)
            else:
                id = 0
                profile = getProfile(id)
                if (profile != None):
                    cv2.putText(img, "Name : " + str(profile[1]), (x, y + h + 20), fontface, fontscale, fontcolor)
                    cv2.putText(img, "Age : " + str(profile[2]), (x, y + h + 45), fontface, fontscale, fontcolor)
        # show the name and age of the person that it is
        cv2.imshow("Recogniser", img)


# facedata.py
name = input("Enter name: ")
cam = cv2.VideoCapture(0)
age = getAge()
print("Age:", age)
cam.release()
cv2.destroyAllWindows()
cam = cv2.VideoCapture(0)
addUser(name, age)
cam.release()
cv2.destroyAllWindows()

# facetrain.py
IDs, faces = getImagesWithID(path)
# train the recognizer with the faces and IDs so it can link them together as that face #1 is the #1 profile
recognizer.train(faces, IDs)
# save the recognizer to the trainningData.yml file
recognizer.save('recognizer/trainningData.yml')
cv2.destroyAllWindows()


# facerecognisation.py
cam = cv2.VideoCapture(0)
FaceRecognition()


# kill camera
cam.release()
cv2.destroyAllWindows()

# close connection
conn.close()
