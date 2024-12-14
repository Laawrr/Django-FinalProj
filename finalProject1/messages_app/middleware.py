from cryptography.fernet import Fernet
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.conf import settings
import json

class EncryptionMiddleware:
    """
    Middleware to encrypt the 'content' field in POST request bodies and decrypt it in GET request bodies.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.cipher = Fernet(settings.ENCRYPT_KEY)  # Ensure ENCRYPT_KEY is configured in your settings.py

    def __call__(self, request):
        # Debugging log to see the request method
        print(f"Request Method: {request.method}")

        if request.method == 'POST':
            print(f"Entered POST request block")
            try:
                if request.body:  # Only attempt encryption if there is a body
                    print(f"Raw request body: {request.body}")

                    # Parse the incoming JSON body
                    parsed_data = json.loads(request.body.decode('utf-8'))

                    # Check if 'content' key exists
                    if 'content' in parsed_data:
                        # Encrypt the 'content' field
                        original_content = parsed_data['content']
                        encrypted_content = self.cipher.encrypt(original_content.encode('utf-8'))  # Encrypt content
                        parsed_data['content'] = encrypted_content.decode('utf-8')  # Replace content with encrypted version
                        print(f"Encrypted content: {parsed_data['content']}")

                    # Reassign the modified body back to the request using _body (a mutable version of body)
                    request._body = json.dumps(parsed_data).encode('utf-8')
            except Exception as e:
                print(f"Encryption error during request: {e}")
                return self._error_response(f"Encryption error during request: {e}")

        elif request.method == 'GET':
            print(f"Entered GET request block")
            try:
                # Check if 'content' is in the query parameters
                if 'content' in request.GET:
                    encrypted_content = request.GET['content']
                    print(f"Encrypted content from query: {encrypted_content}")

                    # Decrypt the 'content' field
                    decrypted_content = self.cipher.decrypt(encrypted_content.encode('utf-8')).decode('utf-8')
                    print(f"Decrypted content: {decrypted_content}")

                    # You can now use decrypted_content in your view logic if needed
                    # Optionally, you can add the decrypted content back to the request or response
                    request.decrypted_content = decrypted_content  # Add to the request object for use in the view

            except Exception as e:
                print(f"Decryption error: {e}")
                return self._error_response(f"Decryption error: {e}")

        # Get the response (Django renders the response here)
        response = self.get_response(request)

        return response

    def _error_response(self, message):
        return Response({'success': False, 'error': message}, status=400)