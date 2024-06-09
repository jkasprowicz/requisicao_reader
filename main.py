import cv2
import pytesseract

# Specify the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

def process_frame(frame):
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Binarize image
    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # Remove noise
    denoised = cv2.medianBlur(binary, 3)
    # Perform OCR
    text = pytesseract.image_to_string(denoised, lang='eng')
    return text

def capture_live_video():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return

    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Failed to capture image.")
            break

        # Display the resulting frame
        cv2.imshow('Live Video Feed', frame)

        # Capture frame on 'space' key press
        if cv2.waitKey(1) & 0xFF == ord(' '):
            captured_frame = frame
            print("Frame captured")
            break

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return captured_frame

# Capture a frame from live video
captured_frame = capture_live_video()

# Process and display the extracted text if a frame was captured
if captured_frame is not None:
    text = process_frame(captured_frame)
    print("Extracted Text:")
    print(text)
