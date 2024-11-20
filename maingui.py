from os import getcwd
from os.path import join

from cv2 import VideoCapture, waitKey, imshow, destroyAllWindows, cvtColor, COLOR_BGR2RGB
from cv2.typing import MatLike
from PySimpleGUI import popup, popup_error, Multiline, Text, Button, Window, WIN_CLOSED
from PIL.Image import fromarray
from PIL import Image
from pytesseract import image_to_string
from pytesseract import pytesseract
from speech_recognition import Recognizer, Microphone, UnknownValueError, RequestError

pytesseract.tesseract_cmd = join(getcwd(), join("Tesseract-OCR", "tesseract.exe"))

def capture_image() -> tuple[bool, MatLike] | None:
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
	is_success = False

	while get_next_frame:
		result, frame = cap.read()
		frame: MatLike

		if result:
			# Display the video feed
			imshow("Camera Feed - Press Space to Capture", frame)

			key: int = waitKey(1)
			if key == 32:  # Spacebar key
				get_next_frame = False
				is_success = True
			elif key == 27: # escape key
				cap.release()
				destroyAllWindows()
				get_next_frame = False
		else:
			get_next_frame = False

	return (is_success, frame)

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
		is_success, image = capture_image()
		image: MatLike
		if is_success:
			try:
				transcribed_text: str = image_to_string(fromarray(cvtColor(image, COLOR_BGR2RGB)))
				destroyAllWindows()

				# Display the transcribed text in the Multiline widget
				window["-OUTPUT-"].update(transcribed_text)
			except Exception as e:
				popup_error("Error processing the image:", str(e))
				destroyAllWindows()
		else:
			popup_error("Error cannot capture the image")
			destroyAllWindows()

	elif event == "Transcribe Audio":
		# Transcribe audio from the microphone
		audio_text = transcribe_audio()
		if audio_text:
			# Display the transcribed text in the Multiline widget
			window["-OUTPUT-"].update(audio_text)

# Close the GUI window
window.close()
