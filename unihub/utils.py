from PIL import Image
from io import BytesIO
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

class FreemiumPagination(PageNumberPagination):
    default_limit = 10
    page_query_param = 'page'

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,  # Общее количество объектов
            'total_pages': self.page.paginator.num_pages,  # Общее количество страниц
            'current_page': self.page.number,  # Текущий номер страницы
            'next_page': self.page.next_page_number() if self.page.has_next() else None,  # Номер следующей страницы
            'previous_page': self.page.previous_page_number() if self.page.has_previous() else None,  # Номер предыдущей страницы
            'results': data,
        })

def validate_png(file_bytes):
    try:
        with Image.open(BytesIO(file_bytes)) as image:
            if image.format != 'PNG':
                return False, "Uploaded file is not a valid PNG image."
        return True, None
    except Exception as e:
        return False, f"Error processing image: {str(e)}"
    
def serializers_get_user_from_request(self):
    request = self.context.get('request')

    if not request:
        return None
    
    token = request.COOKIES.get('token')

    if not token:
        return None

    try:
        return Token.objects.get(key=token).user
    except Token.DoesNotExist:
        return None
    
def get_user_from_request(request):
    token = request.COOKIES.get("token")

    if not token:
        return None, Response({"error": "No token provided"}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        user = Token.objects.get(key=token).user
        return user, None
    except Token.DoesNotExist:
        return None, Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)