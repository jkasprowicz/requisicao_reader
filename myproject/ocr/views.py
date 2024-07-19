import os
import cv2
import easyocr
import uuid
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Exam

# Initialize EasyOCR with Portuguese language
reader = easyocr.Reader(['pt'])

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Image not loaded properly from path: {image_path}")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    return thresh

def extract_text_from_image(image_path):
    preprocessed_image = preprocess_image(image_path)
    result = reader.readtext(preprocessed_image)
    extracted_text = ' '.join([text[1] for text in result])  # Access the text element correctly
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
            image_name = f"{uuid.uuid4()}.jpg"  # Generate a unique name for the image
            image_dir = os.path.join(settings.MEDIA_ROOT, 'exam_images')
            image_path = os.path.join(image_dir, image_name)

            # Create the directory if it doesn't exist
            if not os.path.exists(image_dir):
                os.makedirs(image_dir)
            
            with open(image_path, 'wb+') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)
            
            if not os.path.exists(image_path):
                return JsonResponse({'error': 'Image file not saved properly'})

            try:
                extracted_text = extract_text_from_image(image_path)
                exams = identify_exams(extracted_text)
                
                # Save the exam data along with the image path
                exam_record = Exam(exames='; '.join(exams), image=f'exam_images/{image_name}')
                exam_record.save()
                
                return render(request, 'report.html', {'exams': exams})
            except ValueError as e:
                return JsonResponse({'error': str(e)})
    return render(request, 'upload.html')
