from django.urls import path
from .views import ocr_view

urlpatterns = [
    path('upload/', ocr_view, name='ocr_view'),
]
