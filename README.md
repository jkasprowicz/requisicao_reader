# requisicao_reader

Medical Requisition Text Extraction

This Django application extracts text from medical requisitions using EasyOCR, allowing users to upload photos or use live video for real-time identification.

Goals

Text Extraction: Extract text from medical requisitions (handwritten or printed) to identify exams and tests listed.
Input Methods: Support photo upload and live video input for real-time text identification.
Reporting: Generate a report of identified exams/tests from the extracted text.
Implementation

Technologies Used

Backend: Django, Python
Text Extraction: EasyOCR for accurate optical character recognition (OCR).
Frontend: HTML, CSS (minimal for form handling and display).

Directory Structure
|-- manage.py
|-- requirements.txt
|-- myportfolio/
|   |-- settings.py
|   |-- urls.py
|   |-- ...
|-- static/
|   |-- css/
|   |   |-- style.css
|   |-- js/
|   |-- ...
|-- templates/
|   |-- upload.html
|   |-- report.html
|-- uploaded_images/
|-- main.py (or views.py)
|-- README.md

Usage
Upload Photo: Navigate to the homepage and upload a photo of the medical requisition. Click on "Upload Photo" to extract text and view identified exams.

Live Video Identification: Click on "Live Video Identification" to use your device's camera for real-time text extraction from medical requisitions.

Notes
Ensure your environment has opencv-python and easyocr installed for image processing and text extraction capabilities.
Adjust frontend templates (upload.html and report.html) and styles (style.css) as per your design preferences.
