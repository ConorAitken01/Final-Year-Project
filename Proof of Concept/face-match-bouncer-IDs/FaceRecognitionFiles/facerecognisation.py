import cv2
import sqlite3

# faceDetect = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')
faceDetect = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
# connecting to camera
cam = cv2.VideoCapture(1)

# LBP(Local Binary Patterns) are one way to extract characteristic features of an object
# LBPHFaceRecognizer extracts faces
rec = cv2.face.LBPHFaceRecognizer_create()
# then using LBPHFaceRecognizer to understand the yml file and the training data in it
rec.read("../recognizer/trainningData.yml")

# setting the font type, size and colour
fontface = cv2.FONT_HERSHEY_SIMPLEX
fontscale = 1
fontcolor = (0, 255, 0)


# this function gets the information on a person stored in the database using the ID key
def getProfile(id):
    conn = sqlite3.connect("../FaceBase.db")
    cmd = "SELECT * FROM People WHERE ID=" + str(id)
    cursor = conn.execute(cmd)
    profile = None
    for row in cursor:
        profile = row
    conn.close()
    return profile

# Close the window when Q is pressed
while (cv2.waitKey(1) != ord('q')):
    ret, img = cam.read()
    # converting face images into gray for better face recognition results
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceDetect.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        # make a rectangle around the face
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        id, conf = rec.predict(gray[y:y + h, x:x + w])
        # getting the profile of the person that the recognizer thinks it is
        print(id)
        # conf is the confidence level which is distance between the stream image and stored image
        print(conf)
        # show unknown person if not trained
        if(conf<70):
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
    cv2.imshow("Face", img)

cam.release()
cv2.destroyAllWindows()
