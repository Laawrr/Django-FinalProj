from cryptography.fernet import Fernet
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
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
        # Decrypt incoming request body if it's a POST or PUT request and the content is encrypted
        if request.method in ('POST', 'PUT') and request.content_type == 'application/json':
            try:
                if request.body:  # Only attempt decryption if there is a body
                    print(f"Raw request body: {request.body}")  # Debugging log
                    decrypted_body = self.cipher.decrypt(request.body)  # Keep it as bytes
                    decrypted_body = decrypted_body.decode('utf-8')  # Decode to string after decryption
                    print(f"Decrypted body: {decrypted_body}")  # Debugging log

                    # Check if decrypted data is valid JSON
                    try:
                        parsed_data = json.loads(decrypted_body)
                        request._body = decrypted_body  # Replace the raw body with the decrypted body
                        setattr(request, 'parsed_data', parsed_data)  # Add parsed data to the request object
                        print(f"Decrypted and parsed data: {request.parsed_data}")  # Debugging log
                    except json.JSONDecodeError:
                        raise ValidationError(f"Decrypted data is not valid JSON. Received: {decrypted_body}")
            except Exception as e:
                print(f"Decryption error: {e}")
                return self._error_response(f"Decryption error: {e}")

        # Get the response (Django renders the response here)
        response = self.get_response(request)

        # Encrypt response body if it's JSON
        if response['Content-Type'] == 'application/json':
            try:
                original_content = response.content.decode('utf-8')
                print(f"Original response content: {original_content}")  # Debugging log

                # Encrypt the entire response content (ensure it's in bytes)
                encrypted_content = self.cipher.encrypt(original_content.encode('utf-8'))  # Convert to bytes
                response.content = encrypted_content
                response['Content-Type'] = 'application/octet-stream'  # Change content type for encrypted data
                print(f"Encrypted response content: {response.content}")  # Debugging log
            except Exception as e:
                print(f"Encryption error during response: {e}")
                return self._error_response(f"Encryption error: {e}")

        return response

    def _error_response(self, message):
        return Response({'success': False, 'error': message}, status=400)
