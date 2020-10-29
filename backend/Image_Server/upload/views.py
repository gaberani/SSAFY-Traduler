from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.core.files.storage import FileSystemStorage  # 이미지 저장

# Create your views here.
@api_view(['POST'])
def image_upload(request):
    uploaded_file = request.FILES['image']

    fs = FileSystemStorage()
    filename = fs.save(uploaded_file.name, uploaded_file)
    uploaded_file_url = fs.url(filename)

    return Response({'uploaded_url': uploaded_file_url})