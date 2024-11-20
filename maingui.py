from cv2 import destroyAllWindows, cvtColor, COLOR_BGR2RGB
from cv2.typing import MatLike
from PIL.Image import fromarray
from pytesseract import image_to_string
from pytesseract import pytesseract
from transformers import pipeline
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
from PySimpleGUI import popup_error, Multiline, Text, Button, Window, WIN_CLOSED

from const import MODEL_NAME, TESSERACT_PATH
from camera import capture_image
from audio import transcribe_audio

def init() -> None:
	pytesseract.tesseract_cmd = TESSERACT_PATH
	# Load pretrained tokenizer
	return PegasusTokenizer.from_pretrained(MODEL_NAME)

# Define the GUI layout
layout = [
	[Text("Medication Dashboard", size=(30, 1), justification='center', font=("Helvetica", 20))],
	[Text("Choose an action:")],
	[Button("Capture Image", size=(15, 1)), Button("Transcribe Audio", size=(15, 1))],
	[Text("Output:", font=("Helvetica", 12))],
	[Multiline(size=(60, 10), key="-OUTPUT-", disabled=True)],
	[Button("Exit", size=(10, 1))]
]

pretrained_model = init()
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
		audio_text: str = transcribe_audio()

		if audio_text:
			# Display the transcribed text in the Multiline widget
			window["-OUTPUT-"].update(audio_text)

# Close the GUI window
window.close()
