from cryptography.fernet import Fernet
from rest_framework.response import Response
from django.conf import settings
from django.http import QueryDict
from .models import Message
from .serializers import MessageSerializer
import json

class EncryptionMiddleware:
    """
    Middleware to automatically decrypt 'content' field in GET requests 
    and encrypt it in POST requests.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.cipher = Fernet(settings.ENCRYPT_KEY)  

    def __call__(self, request):
        if request.method == 'POST':
            request = self._encrypt_post_content(request)
        elif request.method == 'GET':
            request = self._decrypt_get_content(request)
        
        # Process the response
        response = self.get_response(request)
        return response

    def _encrypt_post_content(self, request):
        try:
            # Parse incoming POST body
            parsed_data = json.loads(request.body.decode('utf-8'))
            if 'content' in parsed_data:
                original_content = parsed_data['content']
                # Encrypt 'content' and replace it
                encrypted_content = self.cipher.encrypt(original_content.encode('utf-8'))
                parsed_data['content'] = encrypted_content.decode('utf-8')

                # Update request body
                request._body = json.dumps(parsed_data).encode('utf-8')
        except Exception as e:
            return self._error_response(f"Encryption error: {e}")
        return request

    def _decrypt_get_content(self, request):
        try:
            # Initialize an empty list for decrypted content
            decrypted_contents = []
            
            # Assuming Message model contains encrypted 'content' field
            messages = Message.objects.all()
            serializer = MessageSerializer(messages, many=True)
            
            for message in serializer.data:
                encrypted_content = message.get('content')
                if encrypted_content:
                    # Decrypt the content
                    decrypted_content = self.cipher.decrypt(encrypted_content.encode('utf-8')).decode('utf-8')
                    decrypted_contents.append(decrypted_content)
            
            # Store decrypted content in request for use in views
            request.decrypted_contents = decrypted_contents  # Store in request object
            
        except Exception as e:
            return self._error_response(f"Decryption error: {e}")
        return request

    def _error_response(self, message):
        return Response({'success': False, 'error': message}, status=400)
