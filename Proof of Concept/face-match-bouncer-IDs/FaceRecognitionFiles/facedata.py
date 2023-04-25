from datetime import datetime, date
import cv2
import sqlite3
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
config = "--psm 6"

# Get the HaarCascade Classifier onto a variable for easier use
faceDetect = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
# faceDetect = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')

# connecting to camera
cam = cv2.VideoCapture(1)


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
    cv2.destroyAllWindows()


# function for inserting ID, Name and Age into database
def insert(Id, Name, Age):
    conn = sqlite3.connect("../FaceBase.db")
    params = (Id, Name, Age)
    # secure code using ? instead of putting in the parameters directly
    cmd = "INSERT INTO People(ID,Name,Age) Values(?, ?, ?)"
    conn.execute(cmd, params)

    conn.commit()
    conn.close()


# incrementing the last id number for the next profile
conn = sqlite3.connect("../FaceBase.db")
cursor = conn.execute("SELECT * FROM People ORDER BY id DESC LIMIT 1")
result = cursor.fetchone()
# if no profiles in the database then make the id number 1
if (result == None):
    Id = 1
else:
    Id = int(result[0]) + 1
print("ID: ", Id)
conn.close()
name = input('Enter User Name: ')
age = getAge()
print("Age:", age)
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
        cv2.imwrite("../dataSet/User." + str(Id) + "." + str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.waitKey(100)
    cv2.imshow("Face", img)
    cv2.waitKey(1)

cam.release()
cv2.destroyAllWindows()
