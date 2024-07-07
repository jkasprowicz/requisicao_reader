import cv2
import pytesseract
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    return thresh

def extract_text(image_path):
    preprocessed_image = preprocess_image(image_path)
    return pytesseract.image_to_string(preprocessed_image)

def identify_exams(extracted_text):
    exams = []
    lines = extracted_text.split('\n')
    for line in lines:
        if "exam" in line.lower() or "test" in line.lower():
            exams.append(line.strip())
    return exams

@csrf_exempt
def ocr_view(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        with open('uploaded_image.jpg', 'wb+') as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)
        
        extracted_text = extract_text('uploaded_image.jpg')
        exams = identify_exams(extracted_text)
        return JsonResponse({'exams': exams})

    return render(request, 'upload.html')
