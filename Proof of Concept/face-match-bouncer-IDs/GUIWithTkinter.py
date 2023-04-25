import os
from datetime import datetime, date

import PIL
import cv2
import numpy as np
import pytesseract
import tkinter as tk
import sqlite3
from PIL import ImageTk, Image

# Path to the location of the Tesseract-OCR executable/command
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Set up pytesseract with the desired configuration
config = "--psm 6"  # Use page segmentation mode 6 (Assume a single uniform block of vertically aligned text of variable sizes.)

# Get the HaarCascade Classifier onto a variable for easier use
faceDetect = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# LBP(Local Binary Patterns) are one way to extract characteristic features of an object
# LBPHFaceRecognizer extracts faces
recognizer = cv2.face.LBPHFaceRecognizer_create()


# function for inserting ID, Name and Age into database
def insert(Id, Name, Age):
    conn = sqlite3.connect("FaceBase.db")
    params = (Id, Name, Age)
    # secure code using ? instead of putting in the parameters directly
    cmd = "INSERT INTO People(ID,Name,Age) Values(?, ?, ?)"
    conn.execute(cmd, params)

    conn.commit()
    conn.close()

# This function takes in one parameter, `id`, and retrieves the row from a table that matches the given `id`.
def getProfile(id):
    # Connect to the SQLite database.
    conn = sqlite3.connect("FaceBase.db")
    # create the command
    cmd = "SELECT * FROM People WHERE ID=" + str(id)
    # Execute the SQL command on the database and store the resulting rows in the `cursor` variable.
    cursor = conn.execute(cmd)
    profile = None
    # Iterate over the rows and assign the first row to the `profile` variable.
    for row in cursor:
        profile = row
    # Close the database connection.
    conn.close()
    # Return the retrieved profile row.
    return profile


# This class is the main window in the GUI application.
class MainWindow:
    # The constructor method takes in one parameter, `master`, which is the parent window of this main window.
    def __init__(self, master):
        # Store a reference to the parent window.
        self.master = master
        # Set the title of the window.
        self.master.title("Main Window")
        # Create a frame widget and pack it into the main window.
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        # Initialize a video capture object to capture video from the webcam.
        self.video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        # Create text label
        self.light = tk.Label(self.frame, text="test", bg='#fff', fg='#f00')
        self.light.pack()

        # Define a threshold value for brightness.
        threshold = 200
        # Capture a frame from the video feed.
        ret, clip = self.video.read()
        # If the frame was captured successfully,
        if ret:
            brightness = cv2.mean(clip)[0]
            print(brightness)
            # If the brightness value is below the threshold,
            if brightness < threshold:
                # Set the text of the label widget to indicate that the USB light should be turned on.
                text = "Turn on USB light"
                self.light.configure(text=text)
            else:
                # Set the text of the label widget to indicate that the USB light can be turned off.
                text = "You can leave USB light off"
                self.light.configure(text=text)

        # create the buttons needed to navigate the GUI
        self.button1 = tk.Button(self.frame, text="Get Age", command=self.open_window_text)
        self.button1.pack(side="left")
        self.button2 = tk.Button(self.frame, text="Recognise Face", command=self.open_window_get_face)
        self.button2.pack(side="left")
        self.button3 = tk.Button(self.frame, text="Train Model", command=self.open_window_train_data)
        self.button3.pack(side="left")
        self.button4 = tk.Button(self.frame, text="Face Recognition", command=self.open_window_recog_face)
        self.button4.pack(side="left")
        self.quit_button = tk.Button(self.frame, text="Quit", command=self.close_windows)
        self.quit_button.pack(side="left")

        # Create a frame to hold the text
        self.text_frame = tk.Frame(self.master)
        self.text_frame.pack(side="right", fill="both", expand=True)

        # Create a label to display what to do
        text = "Press each button from left to right, starting with \"Get Age\" as far as \"Face Recognition\".\n" \
               "Do not skip a button and follow the instructions on each page.\n" \
               "Once finished with programme press \"Quit\"."
        self.text_label = tk.Label(self.text_frame, text=text)
        self.text_label.pack(side="top", padx=10, pady=10, fill="both", expand=True)

    # This method opens a new window for text recognition.
    def open_window_text(self):
        self.new_window = tk.Toplevel(self.master)
        # Create an instance of the TextRecognitionGUI class and pass it the new window as its parent.
        self.app = TextRecognitionGUI(self.new_window)

    # This method opens a new window for face detection.
    def open_window_get_face(self):
        self.new_window2 = tk.Toplevel(self.master)
        self.app2 = GetFace(self.new_window2)

    # This method opens a new window for training data.
    def open_window_train_data(self):
        self.new_window = tk.Toplevel(self.master)
        self.app3 = TrainData(self.new_window)

    # This method opens a new window for face recognition.
    def open_window_recog_face(self):
        self.new_window = tk.Toplevel(self.master)
        self.app4 = RecogFace(self.new_window)

    # This method closes all open windows and releases the video capture object.
    def close_windows(self):
        # Destroy the parent window.
        self.master.destroy()
        # Release the video capture object.
        self.video.release()


class TextRecognitionGUI:
    def __init__(self, master):
        # Initialize variables
        self.name = ""
        self.age = ""
        self.master = master
        self.master.title("Get Age")
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        _, self.current_frame = self.video.read()
        self.current_frame = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2RGB)
        self.text_label = tk.Label(self.frame, text="")
        self.text_label.pack()

        # Create labels and entry field for name
        self.label = tk.Label(self.frame, text="Enter Name:")
        self.label.pack()
        self.entry = tk.Entry(self.frame)
        self.entry.pack()

        self.video_label = tk.Label(self.frame)
        self.video_label.pack()

        self.button = tk.Button(self.frame, text="Recognize Text", command=self.recognize_text)
        self.button.pack()

        self.update_frame()

        self.close_button = tk.Button(self.frame, text="Close", command=self.close_window)
        self.close_button.pack()

        # Create a frame to hold the text
        self.text_frame = tk.Frame(self.master)
        self.text_frame.pack(side="right", fill="both", expand=True)
        # Create a label to display what to do
        text = "Firstly enter the name on the passport in the box above. Then hold the passport to the camera.\n" \
               "Once the passport is showing on screen press \"Recognise Text\". It may take a couple of tries.\n" \
               "You will know it worked when the top of the screen says the Name and the Age.\n" \
               "After the Name and Age is displayed, Press \"Close\""
        self.label = tk.Label(self.text_frame, text=text)
        self.label.pack(side="top", padx=10, pady=10, fill="both", expand=True)

    def close_window(self):
        # release the video capture device and close the GUI window
        self.video.release()
        self.master.destroy()
        # connect to the database and get the last inserted row to determine the next ID number
        conn = sqlite3.connect("FaceBase.db")
        cursor = conn.execute("SELECT * FROM People")
        result = cursor.fetchall()
        lastRow = result[-1]
        # if no profiles in the database then make the id number 1
        if (result == None):
            Id = 1
        else:
            # set the ID number to the last ID number + 1
            Id = int(lastRow[0]) + 1
        print("ID: ", Id)
        conn.close()
        # if both the name and age have been entered, insert a new profile into the database with the ID number
        if (self.age != "" and self.name != ""):
            insert(Id, self.name, self.age)

    def update_frame(self):
        # the first value returned by the method "self.video.read()" is not used and therefore assigned to "_"
        _, self.current_frame = self.video.read()
        # Convert the color space of the frame from BGR to RGB
        self.current_frame = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2RGB)
        # Convert the frame to an Image object using Pillow
        img = Image.fromarray(self.current_frame)
        # Convert the Image object to an ImageTk object
        imgtk = ImageTk.PhotoImage(image=img)
        # Set the video label to display the new ImageTk object
        self.video_label.configure(image=imgtk)
        self.video_label.imgtk = imgtk
        # Schedule the update_frame method to run again after 20 milliseconds
        self.frame.after(20, self.update_frame)

    def recognize_text(self):
        # Extract text from current frame using pytesseract OCR
        text = pytesseract.image_to_string(self.current_frame)
        print("Extracted text:", text)
        print("End of Extracted Text")

        # Get date of birth from extracted text
        start_index = text.find("IRISH")
        if (text[start_index + 11] == "/"):
            dobWithIrish = text[start_index + 6:start_index + 20]

            dob = (dobWithIrish[:3] + dobWithIrish[6:])
            dateOfBirth = datetime.strptime(dob, '%d %b %Y')
        else:
            dobWithIrish = text[start_index + 6:start_index + 21]

            dob = (dobWithIrish[:3] + dobWithIrish[7:])
            dateOfBirth = datetime.strptime(dob, '%d %b %Y')

        # Calculate age from date of birth and update age attribute
        today = date.today()
        self.age = today.year - dateOfBirth.year - ((today.month, today.day) < (dateOfBirth.month, dateOfBirth.day))
        print(self.age)
        # Get name from user input and display extracted text and age on GUI
        self.name = self.entry.get()
        print(self.name)
        text = ""
        if (self.age > 17):
            text = "Name: " + self.name + " Age: " + str(self.age) + "\n" + \
                   self.name + " is 18 or over"
        else:
            text = "Name: " + self.name + " Age: " + str(self.age) + "\n" + \
                   self.name + " under 18"
        self.text_label.configure(text=text)


class GetFace():
    def __init__(self, master):
        self.master = master
        self.master.title("Get Face")
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        # Create a VideoCapture object to capture video from the webcam
        self.video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        # Create a canvas widget
        self.canvas = tk.Canvas(self.frame, width=640, height=480)
        self.canvas.pack()

        # Create a button to save the detected face to a folder
        self.save_button = tk.Button(self.frame, text="Save Face", command=self.save_face)
        self.save_button.pack()

        # Start the update_frame function to begin capturing and displaying frames
        self.update_frame()

        self.sampleNum = 1

        self.close_button = tk.Button(self.master, text="Close", command=self.close_window)
        self.close_button.pack()

        # Create a frame to hold the text
        self.text_frame = tk.Frame(self.master)
        self.text_frame.pack(side="right", fill="both", expand=True)
        # Create a label to display what to do
        text = "Firstly, hold Passport photo up to screen. Once box is seen around the passport photo press \"Save " \
               "Face\".\nSpam the button around 50 times to ensure high chance of being recognised.\n" \
               "Once done press \"Close\"."
        self.label = tk.Label(self.text_frame, text=text)
        self.label.pack(side="top", padx=10, pady=10, fill="both", expand=True)

    def close_window(self):
        self.video.release()
        self.master.destroy()

    # Define a function to update the canvas with the current frame
    def update_frame(self):
        # Capture a frame from the webcam
        ret, self.frame = self.video.read()

        # Convert the frame to grayscale
        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

        # Apply the Haar Cascade to detect faces
        self.faces = faceDetect.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        # Draw rectangles around the detected faces
        for (x, y, w, h) in self.faces:
            cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # Convert the frame to a PIL Image and display it in the tkinter canvas widget
        img = PIL.Image.fromarray(self.frame)
        img_tk = PIL.ImageTk.PhotoImage(image=img)
        self.canvas.img_tk = img_tk
        self.canvas.create_image(0, 0, image=img_tk, anchor=tk.NW)

        # Schedule the update_frame function to run again after 10 milliseconds
        self.canvas.after(20, self.update_frame)

    # Save the detected face to a folder when the "Save Face" button is pressed
    def save_face(self):
        conn = sqlite3.connect("FaceBase.db")
        cursor = conn.execute("SELECT * FROM People")
        result = cursor.fetchall()
        lastRow = result[-1]
        Id = int(lastRow[0])
        print("ID:", Id)
        print("Sample Number:", self.sampleNum)
        if len(self.faces) > 0:
            # Crop the detected face from the frame and save it to a folder
            x, y, w, h = self.faces[0]
            face = self.frame[y:y + h, x:x + w]
            cv2.imwrite("dataSet/User." + str(Id) + "." + str(self.sampleNum) + ".jpg", face)
            self.sampleNum = self.sampleNum + 1


class TrainData:
    def __init__(self, master):
        self.master = master
        self.master.title("Train the Model")
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.label = tk.Label(self.frame, text="This is where the model will be trained with the data.\n"
                                               "Press \"Train Model\"")
        self.label.pack()

        self.photo_label = tk.Label()
        self.photo_label.pack()

        self.button = tk.Button(self.frame, text="Train Model", command=self.train_model)
        self.button.pack()

        self.close_button = tk.Button(self.frame, text="Close", command=self.close_window)
        self.close_button.pack()

    def close_window(self):
        self.master.destroy()

    # Function to get Images with the ID
    def getImagesWithID(self, path):
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

    # function to train model
    def train_model(self):
        IDs, faces = self.getImagesWithID("dataSet")
        # train the recognizer with the faces and IDs so it can link them together as that face #1 is the #1 profile
        recognizer.train(faces, IDs)
        # save the recognizer to the trainningData.yml file
        recognizer.save('recognizer/trainningData.yml')
        self.label.configure(text="Model has been trained.\nPress \"Close\"")
        cv2.destroyAllWindows()


class RecogFace:
    def __init__(self, master):
        self.master = master
        self.master.title("Face Recogniser")
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        # LBP(Local Binary Patterns) are one way to extract characteristic features of an object
        # LBPHFaceRecognizer extracts faces
        self.rec = cv2.face.LBPHFaceRecognizer_create()
        # then using LBPHFaceRecognizer to understand the yml file and the training data in it
        self.rec.read("recognizer/trainningData.yml")

        # Create a VideoCapture object to capture video from the webcam
        self.video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        self.text_label = tk.Label(self.frame, text="")
        self.text_label.pack()

        # Create a canvas widget
        self.canvas = tk.Canvas(self.frame, width=640, height=480)
        self.canvas.pack()

        # Create a button to save the detected face to a folder
        self.recog_button = tk.Button(self.frame, text="Recognise Face", command=self.recog_face)
        self.recog_button.pack()

        # Start the update_frame function to begin capturing and displaying frames
        self.update_frame()

        self.close_button = tk.Button(self.master, text="Close", command=self.close_window)
        self.close_button.pack()

        # Create a frame to hold the text
        self.text_frame = tk.Frame(self.master)
        self.text_frame.pack(side="right", fill="both", expand=True)
        # Create a label to display what to do
        text = "Stand in front of camera. Once box is around the face press \"Recognise Face\".\n" \
               "You may need to move closer or further away from the camera in order to be recognised.\n" \
               "Once recognised press \"Close\"."
        self.label = tk.Label(self.text_frame, text=text)
        self.label.pack(side="top", padx=10, pady=10, fill="both", expand=True)

    def close_window(self):
        self.video.release()
        self.master.destroy()

    # Define a function to update the canvas with the current frame
    def update_frame(self):
        # Capture a frame from the webcam
        ret, self.frame = self.video.read()

        # Convert the frame to grayscale
        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

        # Apply the Haar Cascade to detect faces
        self.faces = faceDetect.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        # Draw rectangles around the detected faces
        for (x, y, w, h) in self.faces:
            cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # Convert the frame to a PIL Image and display it in the tkinter canvas widget
        img = PIL.Image.fromarray(self.frame)
        img_tk = PIL.ImageTk.PhotoImage(image=img)
        self.canvas.img_tk = img_tk
        self.canvas.create_image(0, 0, image=img_tk, anchor=tk.NW)

        # Schedule the update_frame function to run again after 10 milliseconds
        self.canvas.after(20, self.update_frame)

    def recog_face(self):
        if len(self.faces) > 0:
            # Crop the detected face from the frame and save it to a folder
            x, y, w, h = self.faces[0]
            face = self.frame[y:y + h, x:x + w]
            gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            id, conf = self.rec.predict(gray)
            print(id)
            print(conf)
            if (conf < 50):
                profile = getProfile(id)
                if (profile != None):
                    if (int(profile[2]) > 17):
                        text = "Name: " + str(profile[1]) + " Age: " + str(profile[2]) + "\n" + str(profile[1]) + \
                               " is 18 or Over"
                    else:
                        text = "Name: " + str(profile[1]) + " Age: " + str(profile[2]) + "\n" + str(profile[1]) + \
                               " is under 18"
                    self.text_label.configure(text=text)
            else:
                id = 0
                profile = getProfile(id)
                if (profile != None):
                    text = "Name: " + str(profile[1]) + " Age: " + str(profile[2]) + "\n" + "Do not allow into " \
                                                                                            "establishment"
                    self.text_label.configure(text=text)


def main():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()


if __name__ == '__main__':
    main()
