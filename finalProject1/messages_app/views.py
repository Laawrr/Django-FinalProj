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

@login_required(login_url='login')
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def message_api(request):
    try:
        if request.method == 'GET':
            # Fetch all messages from the database
            messages = Message.objects.all()
            serializer = MessageSerializer(messages, many=True)

            # Retrieve decrypted contents from middleware
            decrypted_contents = getattr(request, 'decrypted_contents', None)
            if decrypted_contents is None or len(decrypted_contents) != len(serializer.data):
                return Response({'error': 'Decryption failed or mismatch in data lengths'}, status=status.HTTP_400_BAD_REQUEST)

            # Combine serialized data with decrypted contents
            decrypted_messages = [
                {
                    'user': message['user'],
                    'content': decrypted_contents[i],
                    'timestamp': message['timestamp']
                }
                for i, message in enumerate(serializer.data)
            ]
            print("Serialized data length:", len(serializer.data))
            print("Decrypted contents length:", len(request.decrypted_contents))
            return Response({'decrypted_content': decrypted_messages}, status=status.HTTP_200_OK)

        elif request.method == 'POST':
            # Save the serialized data
            serializer = MessageSerializer(data=request.data)
            print("asd:",serializer)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)