from django.shortcuts import render

# Create your views here.
def message_app(request):
    # Add any context data if needed, e.g., existing messages
    context = {
        "username": "Lawrence",  # Replace with actual username if user authentication is integrated
        # Example: 'messages': [{'text': 'Hello World', 'timestamp': '10:00 AM'}]
    }
    return render(request, 'messages.html', context)