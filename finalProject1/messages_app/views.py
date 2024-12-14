from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Message
from .serializers import MessageSerializer

@login_required(login_url='login')
def message_app(request):
    return render(request, 'messages.html')

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def message_api(request):
    try:
        if request.method == 'GET':
            # # Decrypted content is now stored in request.decrypted_contents by the middleware
            messages = Message.objects.all()
            serializer = MessageSerializer(messages, many=True)
            print(messages)
            decrypted_contents = getattr(request, 'decrypted_contents', None)
            
            if decrypted_contents:
                # Return the decrypted contents as a response
                decrypted_messages = [
                {
                    'user': message['user'],
                    'content': decrypted_contents[i], 
                    'timestamp': message['timestamp']
                }
                for i, message in enumerate(serializer.data)
            ]
                return Response({'decrypted_content': decrypted_messages}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'No decrypted content found'}, status=status.HTTP_404_NOT_FOUND)

        elif request.method == 'POST':
            # Handle POST request to create a new message
            serializer = MessageSerializer(data=request.data)
            if serializer.is_valid():
                # Associate the message with the current user
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Handle method not allowed for other HTTP methods
        else:
            return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    except Exception as e:
        # Handle other unexpected errors
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
