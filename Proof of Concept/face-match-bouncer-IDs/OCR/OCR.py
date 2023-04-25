import pytesseract
import cv2
from datetime import datetime, date

# Path to the location of the Tesseract-OCR executable/command
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Set up the video capture from the default camera
cam = cv2.VideoCapture(2)

# Set up pytesseract with the desired configuration
config = "--psm 6"  # Use page segmentation mode 6 (Assume a single uniform block of vertically aligned text of variable sizes.)


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
        cv2.imshow("Live Stream", frame)

    print("Extracted text:", text)
    print("End of Extracted Text")

    start_index = text.find("IRISH")
    dobWithIrish = text[start_index + 6:start_index + 21]

    dob = (dobWithIrish[:3] + dobWithIrish[7:])
    dateOfBirth = datetime.strptime(dob, '%d %b %Y')
    print("Date of Birth is:", dateOfBirth)

    today = date.today()
    age = today.year - dateOfBirth.year - ((today.month, today.day) < (dateOfBirth.month, dateOfBirth.day))
    return age


age = getAge()
print(age)
# Release the resources and close the windows
cam.release()
cv2.destroyAllWindows()
