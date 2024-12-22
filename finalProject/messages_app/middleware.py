from cryptography.fernet import Fernet
from rest_framework.response import Response
from django.conf import settings
from django.http import JsonResponse
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

            # Decode the request body
            parsed_data = json.loads(request.body.decode('utf-8'))
            
            # Encrypt the content if it exists
            if 'content' in parsed_data:
                parsed_data['content'] = self.cipher.encrypt(parsed_data['content'].encode('utf-8')).decode('utf-8')
                request._body = json.dumps(parsed_data).encode('utf-8')
                request._full_data = parsed_data  # Storing the modified data
            

        except json.JSONDecodeError:
            # Skip encryption for malformed or non-JSON payloads
            pass
        except Exception as e:
            # Log unexpected errors (optional) and continue
            print(f"Unexpected error during encryption: {e}")
        
        return request

    def _decrypt_get_content(self, request):
        try:
            decrypted_contents = []
            
            # Assuming Message model contains encrypted 'content' field
            messages = Message.objects.all()
            serializer = MessageSerializer(messages, many=True)
            
            # Decrypt each message's content
            for message in serializer.data:
                encrypted_content = message.get('content')
                if encrypted_content:
                    try:
                        decrypted_content = self.cipher.decrypt(encrypted_content.encode('utf-8')).decode('utf-8')
                        decrypted_contents.append(decrypted_content)
                    except Exception as e:
                        print(f"Decryption failed for message {message['id']}: {e}")
                        decrypted_contents.append(None)  # Append None for failed decryption
                else:
                    decrypted_contents.append(None)

            # Store decrypted content in request for use in views
            request.decrypted_contents = decrypted_contents  # Store in request object
            
        except Exception as e:
            print("Middleware decryption error:", e)  # Debugging
            request.decrypted_contents = None
        return request

    def _error_response(self, message):
        return JsonResponse({'success': False, 'error': message}, status=400)
