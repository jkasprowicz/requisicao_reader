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
from datetime import datetime

# Initialize EasyOCR
reader = easyocr.Reader(['pt'])


def recognize_text(img_path):    
    reader = easyocr.Reader(['pt'])
    return reader.readtext(img_path)

def extract_profile_info(ocr_text):
    profile_info = {
        'name': None,
        'cpf': None,
        'birth_date': None
    }

    # Regex patterns for CPF and date extraction
    cpf_pattern = re.compile(r'\d{3}\.\d{3}\.\d{3}-\d{2}|\d{11}')
    date_pattern = re.compile(r'\d{2}/\d{2}/\d{4}')

    

    for bbox, text, prob in ocr_text:
        text = text.strip()

        # Extract CPF
        cpf_match = cpf_pattern.search(text)

        print(cpf_match)

        if cpf_match:
            profile_info['cpf'] = cpf_match.group()
        
        # Extract date (assuming it's a birth date)
        date_match = date_pattern.search(text)
        if date_match:
            try:
                profile_info['birth_date'] = datetime.strptime(date_match.group(), "%d/%m/%Y").date()
            except ValueError:
                # Handle parsing error if necessary
                pass

        # Extract name based on common name patterns
        # Assuming name is often a line with multiple words and proper case
        if len(text.split()) > 1 and not (profile_info['name'] or profile_info['cpf'] or profile_info['birth_date']):
            profile_info['name'] = text

    return profile_info


def save_user_profile(profile_info):
    try:

        print("Profile Info:", profile_info)

        profile = UserProfile(
            name=profile_info['name'],
            cpf=profile_info['cpf'],
            birth_date=profile_info['birth_date']
        )
        profile.save()
        return profile
    except Exception as e:
        print(f"Error saving user profile: {e}")
        return None

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

                profile_info = extract_profile_info(reconhecimento_texto)

                print(profile_info)
                
                if profile_info:
                    success = save_user_profile(profile_info)
                    if success:
                        print('User profile saved successfully')
                    else:
                        print('Failed to save user profile')

                salvar = TextoExtraido(texto=reconhecimento_texto, image=img)
                salvar.save()

                
                return JsonResponse({'message': 'User profile created successfully'})
            except ValueError as e:
                return JsonResponse({'error': str(e)})

    return render(request, 'upload_document.html')


def report_page(request, user_id):
    user_profile = UserProfile.objects.get(id=user_id)
    exams = user_profile.exams.all()
    return render(request, 'report.html', {'user_profile': user_profile, 'exams': exams})