<h1>DoseDecoder</h1> 

Medication Jargon Translator with OCR and Audio Transcription
This application provides an intuitive interface for extracting medication-related information using Optical Character Recognition (OCR) and audio transcription. This tool relieves the stress of understanding drugs and decoding complex medical jargon. It simplifies instructions, helping people from all walks of life. By focusing on accessibility, the application invests in users of all education levels, ensuring healthcare information is understandable for everyone. Also Includes text to speech and speech to text with a file lookup in ui.


<h3>Features</h3>
<table> <thead> <tr> <th>Features</th> <th>Description</th> </tr> </thead> <tbody> <tr> <td><strong>OCR</strong></td> <td>Extracts text from prescription labels or images using Tesseract.</td> </tr> <tr> <td><strong>Audio Transcription</strong></td> <td>Converts spoken notes into text using advanced speech-to-text processing.</td> </tr> <tr> <td><strong>Summarization</strong></td> <td>Generates concise, understandable summaries of extracted text or audio.</td> </tr> </tbody> </table>


<h3>Dependencies:</h3>
<ul>
  <li>opencv-python==4.10.0.84</li>
  <li>PySimpleGUI==5.0.7</li>
  <li>pillow==11.0.0</li>
  <li>pytesseract==0.3.13</li>
  <li>SpeechRecognition==3.11.0</li>
  <li>transformers==4.46.3</li>
  <li>pytorch-lightning==2.4.0</li>
  <li>sentencepiece==0.2.0</li>
  <li>pegasus==0.1.3</li>
</ul>


<h4>File Structure</h4>
<ul>
  <li>app.py: Main application file containing GUI logic</li>
  <li>camera.py: Module for handling camera capture functionality</li>
  <li>audio.py: Module for audio recording and transcription</li>
  <li>nlp.py: NLP module for text summarization</li>
  <li>const.py: Contains configuration constants like the Tesseract path</li>
</ul>
