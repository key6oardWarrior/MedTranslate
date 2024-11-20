from cv2 import VideoCapture, waitKey, imshow, destroyAllWindows
from cv2.typing import MatLike
from PySimpleGUI import popup

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