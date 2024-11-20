from os.path import join
from os import getcwd

# Pick model
MODEL_NAME = "google/pegasus-xsum"
TESSERACT_PATH = join(getcwd(), join("Tesseract-OCR", "tesseract.exe"))