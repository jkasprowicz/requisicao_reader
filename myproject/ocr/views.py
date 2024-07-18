import cv2
import easyocr
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Initialize EasyOCR with Portuguese language
reader = easyocr.Reader(['pt'])

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    return thresh

def extract_text_from_image(image_path):
    preprocessed_image = preprocess_image(image_path)
    result = reader.readtext(preprocessed_image)
    extracted_text = ' '.join([text for (text, _, _) in result])
    return extracted_text

def identify_exams(extracted_text):
    exams = []
    lines = extracted_text.split('\n')
    for line in lines:
        if "exam" in line.lower() or "test" in line.lower():
            exams.append(line.strip())
    return exams

@csrf_exempt
def ocr_view(request):
    if request.method == 'POST':
        if 'live_video_submit' in request.POST:
            # Handle live video input (to be implemented)
            return JsonResponse({'message': 'Live video functionality to be implemented'})
        
        elif request.FILES.get('image'):
            image_file = request.FILES['image']
            with open('uploaded_image.jpg', 'wb+') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)
            
            extracted_text = extract_text_from_image('uploaded_image.jpg')
            exams = identify_exams(extracted_text)
            return render(request, 'report.html', {'exams': exams})

    return render(request, 'upload.html')
