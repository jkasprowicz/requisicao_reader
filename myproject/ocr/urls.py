from django.urls import path
from .views import upload_document, requisition_page, report_page

urlpatterns = [
    path('', upload_document, name='upload_document'),
    path('requisition/<int:user_id>/', requisition_page, name='requisition_page'),
    path('report/<int:user_id>/', report_page, name='report_page'),
]