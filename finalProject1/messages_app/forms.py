from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']  

    content = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'flex-1 px-4 py-2 bg-white border border-gray-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500',
            'placeholder': 'Type a message...'
        })
    )
