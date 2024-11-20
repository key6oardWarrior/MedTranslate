from cv2 import destroyAllWindows, cvtColor, COLOR_BGR2RGB, imread
from cv2.typing import MatLike
from PIL.Image import fromarray, open as open_image
from pytesseract import image_to_string
from pytesseract import pytesseract
from PySimpleGUI import popup_error, Multiline, Text, Button, Window, WIN_CLOSED

from const import TESSERACT_PATH
from camera import capture_image
from audio import transcribe_audio
from nlp import NLP

# Define the GUI layout
layout = [
	[Text("Medication Dashboard", size=(30, 1), justification='center', font=("Helvetica", 20))],
	[Text("Choose an action:")],
	[Button("Capture Image", size=(15, 1)), Button("Transcribe Audio", size=(15, 1)), Button("From Photos")],
	[Text("Output:", font=("Helvetica", 12))],
	[Multiline(size=(60, 10), key="-OUTPUT-", disabled=True)],
	[Button("Exit", size=(10, 1))]
]

# Create the GUI window
window = Window("Medication Assistant with OCR and Audio Transcription", layout)
pytesseract.tesseract_cmd = TESSERACT_PATH
summerizer = NLP()

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
				simple_summary: str = summerizer.simple_summary(transcribed_text)

				# Display the transcribed text in the Multiline widget
				window["-OUTPUT-"].update(simple_summary)
			except Exception as e:
				popup_error("Error processing the image:", str(e))
				destroyAllWindows()
		else:
			popup_error("Error cannot capture the image")
			destroyAllWindows()

	elif event == "Transcribe Audio":
		# Transcribe audio from the microphone
		audio_text: str = transcribe_audio()

		if audio_text:
			# Display the transcribed text in the Multiline widget
			window["-OUTPUT-"].update(audio_text)

	elif event == "From Photos":
		image: MatLike = imread("C:\\Users\\Lewjb\\Engineering\\GitHub\\Personal\\Private\\MedTranslate\\TestImages\\Drug1.jpg")

		try:
			transcribed_text: str = image_to_string(fromarray(cvtColor(image, COLOR_BGR2RGB)))
			destroyAllWindows()
			simple_summary: str = summerizer.simple_summary(transcribed_text)

			# Display the transcribed text in the Multiline widget
			window["-OUTPUT-"].update(simple_summary)
		except Exception as e:
			popup_error("Error processing the image:", str(e))

# Close the GUI window
window.close()
