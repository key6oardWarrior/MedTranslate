from speech_recognition import Recognizer, Microphone, UnknownValueError, RequestError
from PySimpleGUI import popup, popup_error

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