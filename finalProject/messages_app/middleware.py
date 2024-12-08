from cryptography.fernet import Fernet
from django.http import JsonResponse
from django.conf import settings
import json


class EncryptionMiddleware:
    """
    Middleware to encrypt API responses and decrypt incoming request bodies for JSON data.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.cipher = Fernet(settings.ENCRYPT_KEY)  # Ensure ENCRYPT_KEY is configured in your settings.py

    def __call__(self, request):
        # Decrypt incoming request body if method and content type match
        if request.method in ('POST', 'PUT') and request.content_type == 'application/json':
            try:
                if request.body:  # Only attempt decryption if there is a body
                    decrypted_body = self.cipher.decrypt(request.body).decode('utf-8')
                    request._body = decrypted_body  # Replace the raw body with the decrypted body
                    setattr(request, 'parsed_data', json.loads(decrypted_body))  # Add parsed data to the request object
                    print(f"Decrypted data: {request.parsed_data}")  # Debugging log
            except Exception as e:
                print(f"Decryption error: {e}")
                return self._error_response(f"Decryption error: {e}")

        # Get the response
        response = self.get_response(request)

        # Encrypt response body if it's JSON
        if response['Content-Type'] == 'application/json':
            try:
                original_content = response.content.decode('utf-8')
                response_data = json.loads(original_content)  # Parse the JSON response data

                # Encrypt the entire response content
                encrypted_content = self.cipher.encrypt(original_content.encode('utf-8'))
                response.content = encrypted_content
                response['Content-Type'] = 'application/octet-stream'  # Change content type for encrypted data
            except Exception as e:
                print(f"Encryption error: {e}")
                return self._error_response(f"Encryption error: {e}")

        return response

    def _error_response(self, message):
        return JsonResponse({'success': False, 'error': message}, status=400)
