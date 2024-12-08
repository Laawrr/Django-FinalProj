from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import MessageForm
from .models import Message

@login_required(login_url='login')
def message_app(request):
    form = MessageForm()
    messages = Message.objects.all().order_by('timestamp')  # Fetch messages for the template

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.save()
            return JsonResponse({
                'success': True,
                'username': message.user.username,
                'content': message.content,
                'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            })
        else:
            return JsonResponse({'success': False, 'message': 'Failed to send message'}, status=400)

    return render(request, 'messages.html', {'form': form, 'messages': messages})


@login_required(login_url='login')
def get_messages(request):
    # Fetch all messages and order them by timestamp (oldest first)
    messages_list = Message.objects.all().order_by('timestamp')

    # Prepare the messages to return as JSON
    messages_data = [
        {
            'username': message.user.username,
            'content': message.content,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        }
        for message in messages_list
    ]

    return JsonResponse({'messages': messages_data})
