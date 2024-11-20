import cv2
import PySimpleGUI as sg
from PIL import Image
import pytesseract
import speech_recognition as sr
from os import getcwd


# Configure Tesseract path (update this based on your system)
# Example for Windows: pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = getcwd()

# Function to capture an image from the camera
def capture_image():
    cap = cv2.VideoCapture(0)  # Use the default camera (index 0)
    
    if not cap.isOpened():
        sg.popup_error("Error: Could not access the camera.")
        return None

    sg.popup("Press 'Spacebar' to capture the image, or 'Esc' to cancel.", title="Instructions")

    while True:
        ret, frame = cap.read()
        if not ret:
            sg.popup_error("Error: Failed to read from the camera.")
            break

        # Display the video feed
        cv2.imshow("Camera Feed - Press Space to Capture", frame)

        key = cv2.waitKey(1)
        if key == 27:  # Escape key
            cap.release()
            cv2.destroyAllWindows()
            return None
        elif key == 32:  # Spacebar key
            # Save the captured frame
            captured_image = frame
            cap.release()
            cv2.destroyAllWindows()
            return captured_image

# Function to transcribe audio from the microphone
def transcribe_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        sg.popup("Listening... Please speak clearly.", title="Microphone Active")
        try:
            # Capture audio from the microphone
            print("Mic in use...")
            audio = recognizer.listen(source)
            # Transcribe audio to text
            transcribed_text = recognizer.recognize_google(audio)
            return transcribed_text
        except sr.UnknownValueError:
            sg.popup_error("Could not understand the audio.")
        except sr.RequestError as e:
            sg.popup_error(f"Error with the speech recognition service: {e}")
        return None

# Define the GUI layout
layout = [
    [sg.Text("Medication Dashboard", size=(30, 1), justification='center', font=("Helvetica", 20))],
    [sg.Text("Choose an action:")],
    [sg.Button("Capture Image", size=(15, 1)), sg.Button("Transcribe Audio", size=(15, 1))],
    [sg.Text("Output:", font=("Helvetica", 12))],
    [sg.Multiline(size=(60, 10), key="-OUTPUT-", disabled=True)],
    [sg.Button("Exit", size=(10, 1))]
]

# Create the GUI window
window = sg.Window("Medication Assistant with OCR and Audio Transcription", layout)

# Event loop
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == "Exit":
        break

    if event == "Capture Image":
        # Capture an image from the camera
        image = capture_image()
        if image is not None:
            # Convert the OpenCV image (BGR) to PIL format (RGB)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(image_rgb)

            try:
                # Perform OCR on the image
                transcribed_text = pytesseract.image_to_string(pil_image)

                # Display the transcribed text in the Multiline widget
                window["-OUTPUT-"].update(transcribed_text)
            except Exception as e:
                sg.popup_error("Error processing the image:", str(e))

    if event == "Transcribe Audio":
        # Transcribe audio from the microphone
        audio_text = transcribe_audio()
        if audio_text:
            # Display the transcribed text in the Multiline widget
            window["-OUTPUT-"].update(audio_text)

# Close the GUI window
window.close()
