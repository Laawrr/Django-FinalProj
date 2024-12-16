from cryptography.fernet import Fernet
from rest_framework.response import Response
from django.conf import settings
from django.http import QueryDict, JsonResponse
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
            # If an error response is returned, exit middleware
            if isinstance(request, JsonResponse):
                return request
        elif request.method == 'GET':
            request = self._decrypt_get_content(request)
            # If an error response is returned, exit middleware
            if isinstance(request, JsonResponse):
                return request

        # Process the response
        response = self.get_response(request)
        return response

    def _encrypt_post_content(self, request):
        try:
            # Check if the request body is empty
            if not request.body.strip():
                return request  # Continue without encryption if no body is present
            print("Original body:", request.body)
            parsed_data = json.loads(request.body.decode('utf-8'))
            if 'content' in parsed_data:
                parsed_data['content'] = self.cipher.encrypt(parsed_data['content'].encode('utf-8')).decode('utf-8')
                request._body = json.dumps(parsed_data).encode('utf-8')
                request._full_data = parsed_data
            
            print("Modified body:", request.body)

        except json.JSONDecodeError:
            # Skip encryption for malformed or non-JSON payloads
            pass
        except Exception as e:
            # Log unexpected errors (optional) and continue
            print(f"Unexpected error during encryption: {e}")
        
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
                    try: # Decrypt the content
                        decrypted_content = self.cipher.decrypt(encrypted_content.encode('utf-8')).decode('utf-8')
                        decrypted_contents.append(decrypted_content)
                    except Exception as e:
                        print(f"Decryption failed for message {message['id']}: {e}")
                else:
                    decrypted_contents.append(None) 
            # Store decrypted content in request for use in views
            request.decrypted_contents = decrypted_contents  # Store in request object
            print("Middleware decrypted contents:", decrypted_contents) 
            
        except Exception as e:
            print("Middleware decryption error:", e)  # Debugging
            request.decrypted_contents = None
        return request

    def _error_response(self, message):
        return JsonResponse({'success': False, 'error': message}, status=400)
