from os import getcwd

from cv2 import VideoCapture, waitKey, imshow, destroyAllWindows, cvtColor, COLOR_BGR2RGB
from cv2.typing import MatLike
from PySimpleGUI import popup, popup_error, Multiline, Text, Button, Window, WIN_CLOSED
from PIL.Image import fromarray
from PIL import Image
from pytesseract import image_to_string
from pytesseract.pytesseract import tesseract_cmd
from speech_recognition import Recognizer, Microphone, UnknownValueError, RequestError

# Configure Tesseract path (update this based on your system)
# Example for Windows: tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
tesseract_cmd = getcwd()

def capture_image() -> MatLike | None:
	'''
	# Description:
	Capture an image from the camera

	# Returns:
	MatLike object that represents the image or None if error
	'''
	cap = VideoCapture(0)  # Use the default camera (index 0)

	if cap.isOpened() == False:
		return None

	popup("Press 'Spacebar' to capture the image, or 'Esc' to cancel.", title="Instructions")
	get_next_frame = True
	frame = None

	while get_next_frame:
		result, frame = cap.read()
		frame: MatLike

		if result == None:
			get_next_frame = False

		# Display the video feed
		imshow("Camera Feed - Press Space to Capture", frame)

		key: int = waitKey(1)
		if key == 32:  # Spacebar key
			get_next_frame = False
		elif key == 27: # escape key
			cap.release()
			destroyAllWindows()
			get_next_frame = False

	return frame

def transcribe_audio() -> str | None:
	'''
	# Description:
	Transcribe audio from the microphone

	# Returns:
	The transcribed text or None if error
	'''
	recognizer = Recognizer()
	with Microphone() as source:
		popup("Listening... Please speak clearly.", title="Microphone Active")
		try:
			# Capture audio from the microphone
			print("Mic in use...")
			audio = recognizer.listen(source)
			# Transcribe audio to text
			transcribed_text = recognizer.recognize_google(audio)
			return transcribed_text
		except UnknownValueError:
			popup_error("Could not understand the audio.")
		except RequestError as e:
			popup_error(f"Error with the speech recognition service: {e}")

# Define the GUI layout
layout = [
	[Text("Medication Dashboard", size=(30, 1), justification='center', font=("Helvetica", 20))],
	[Text("Choose an action:")],
	[Button("Capture Image", size=(15, 1)), Button("Transcribe Audio", size=(15, 1))],
	[Text("Output:", font=("Helvetica", 12))],
	[Multiline(size=(60, 10), key="-OUTPUT-", disabled=True)],
	[Button("Exit", size=(10, 1))]
]

# Create the GUI window
window = Window("Medication Assistant with OCR and Audio Transcription", layout)

# Event loop
while True:
	event, values = window.read()

	if((event == WIN_CLOSED) or (event == "Exit")):
		break

	if event == "Capture Image":
		# Capture an image from the camera
		image: MatLike = capture_image()
		if image:
			# Convert the OpenCV image (BGR) to PIL format (RGB)
			image_rgb: MatLike = cvtColor(image, COLOR_BGR2RGB)
			pil_image: Image = fromarray(image_rgb)

			try:
				# Perform OCR on the image
				transcribed_text: str = image_to_string(pil_image)

				# Display the transcribed text in the Multiline widget
				window["-OUTPUT-"].update(transcribed_text)
			except Exception as e:
				popup_error("Error processing the image:", str(e))
		else:
			popup_error("Error cannot capture the image")

	elif event == "Transcribe Audio":
		# Transcribe audio from the microphone
		audio_text = transcribe_audio()
		if audio_text:
			# Display the transcribed text in the Multiline widget
			window["-OUTPUT-"].update(audio_text)

# Close the GUI window
window.close()
