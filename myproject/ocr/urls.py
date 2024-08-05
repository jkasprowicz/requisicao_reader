from django.urls import path
from .views import upload_document, report_page

urlpatterns = [
    path('', upload_document, name='upload_document'),
    path('report/<int:user_id>/', report_page, name='report_page'),
]