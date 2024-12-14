from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'user', 'content', 'timestamp']
        read_only_fields = ['id', 'user', 'timestamp']  