from PIL import Image
from io import BytesIO
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
import sendgrid
from sendgrid.helpers.mail import Mail, From
from unihub import settings
from unihub.settings import SENDGRID_KEY

class FreemiumPagination(PageNumberPagination):
    default_limit = 30
    page_query_param = 'page'
 
    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,  
            'total_pages': self.page.paginator.num_pages, 
            'current_page': self.page.number,  
            'next_page': self.page.next_page_number() if self.page.has_next() else None, 
            'previous_page': self.page.previous_page_number() if self.page.has_previous() else None, 
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
    
def send_email(reciever,subject="Opps",text="Looks like we have messed up"):
    if reciever.email:
        sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_KEY)
        mail = Mail(
            from_email= From(settings.SENDGRID_EMAIL,'UniHub'),
            to_emails=reciever.email,
            subject=subject,
            html_content=f"""
            <p>Hi, {reciever.first_name}!</p>
            <p>{text}</p>
            <br>
            <p>Best regards,<br>UniHub Team</p>
            """
        )
        sg.send(mail)
        
def check_user_can_pD_posts(user,post):
    from communities.views import check_user_is_admin, check_user_is_community_creator
    return post.profile == user if post.profile else check_user_is_admin(user,post.community) or check_user_is_community_creator(user,post.community)
