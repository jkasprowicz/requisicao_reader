import os
import uuid
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile, Exam, TextoExtraido
import easyocr
import numpy as np
from pdf2image import convert_from_path
import cv2
import re
import matplotlib.pyplot as plt

# Initialize EasyOCR
reader = easyocr.Reader(['pt'])


def recognize_text(img_path):    
    reader = easyocr.Reader(['en'])
    return reader.readtext(img_path)

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    return thresh

def extract_text_from_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Image not loaded properly from path: {image_path}")
    preprocessed_image = preprocess_image(image)
    result = reader.readtext(preprocessed_image)
    extracted_text = ' '.join([text[1] for text in result])
    return extracted_text

def extract_text_from_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    text = ''
    for image in images:
        image_np = np.array(image)
        preprocessed_image = preprocess_image(image_np)
        result = reader.readtext(preprocessed_image)
        text += ' '.join([text[1] for text in result]) + ' '
    return text

def extract_text_from_file(file_path):
    if file_path.lower().endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    return extract_text_from_image(file_path)

@csrf_exempt
def upload_document(request):
    if request.method == 'POST':
        if 'live_video_submit' in request.POST:
            # Handle live video input (to be implemented)
            return JsonResponse({'message': 'Live video functionality to be implemented'})
        
        elif request.FILES.get('document'):
            file = request.FILES['document']
            file_name = f"{file.name.split('.')[-1]}"  
            file_path = os.path.join(settings.MEDIA_ROOT, 'user_documents', file_name)


            if not os.path.exists(os.path.dirname(file_path)):
                os.makedirs(os.path.dirname(file_path))
            
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            try:

                reconhecimento_texto = recognize_text(file_path)
                print(reconhecimento_texto)



                img = cv2.imread(file_path)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                
                dpi = 80

                for (bbox, text, prob) in reconhecimento_texto:
                    if prob >= 0.5:
                        # display 
                        print(f'Detected text: {text} (Probability: {prob:.2f})')
                        (top_left, top_right, bottom_right, bottom_left) = bbox
                        top_left = (int(top_left[0]), int(top_left[1]))
                        bottom_right = (int(bottom_right[0]), int(bottom_right[1]))
                        cv2.rectangle(img=img, pt1=top_left, pt2=bottom_right, color=(255, 0, 0), thickness=10)

                        cv2.putText(img=img, text=text, org=(top_left[0], top_left[1] - 10), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255, 0, 0), thickness=8)
                    

                cv2.imwrite('document.png', cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

                salvar = TextoExtraido(texto=reconhecimento_texto, image=img)
                salvar.save()

                
                return JsonResponse({'message': 'User profile created successfully'})
            except ValueError as e:
                return JsonResponse({'error': str(e)})

    return render(request, 'upload_document.html')


@csrf_exempt
def requisition_page(request, user_id):
    user_profile = UserProfile.objects.get(id=user_id)
    if request.method == 'POST':
        requisition_file = request.FILES.get('requisition')
        exam_image_file = request.FILES.get('exam_image')
        if requisition_file:
            # Save the requisition file
            requisition_file_name = f"{uuid.uuid4()}.{requisition_file.name.split('.')[-1]}"
            requisition_file_path = os.path.join(settings.MEDIA_ROOT, 'requisitions', requisition_file_name)

            with open(requisition_file_path, 'wb+') as destination:
                for chunk in requisition_file.chunks():
                    destination.write(chunk)

            # Process the requisition file (mocked here)
            exam1 = Exam(exames="Blood Test", image=exam_image_file)
            exam1.save()
            user_profile.exams.add(exam1)
            return redirect('report_page', user_id=user_profile.id)
        else:
            return JsonResponse({'error': 'No requisition file uploaded'})
    
    return render(request, 'requisition.html', {'user_id': user_id})

def report_page(request, user_id):
    user_profile = UserProfile.objects.get(id=user_id)
    exams = user_profile.exams.all()
    return render(request, 'report.html', {'user_profile': user_profile, 'exams': exams})