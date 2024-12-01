from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
# Create your views here.

dashboard = [
    {
        "id":1,
        "title": 'Let\'s explore python',
        "content": 'Python Is INterpreded'
    },
    {
        "id":2,
        "title": 'balbalbalbalba',
        "content":'hahahahahaahahaha'
    },
]

def home(request):
    html = ""
    for post in dashboard:
        html += f'''
            <div>
            <a href="/post/{post['id']}/"
                <h1>{post['id']} - {post['title']}</h1></a>
                <p>{post['content']}</p>
            </div>

'''
    return render(request,'dashboard/home.html')

def post(request, id):
    valid_id = False
    for post in dashboard:
        if post['id'] == id:
            post_dict = post
            valid_id = True
            break
    if valid_id:
        html = f'''
                <h1>{post_dict['title']}</h1>
                <p>{post_dict['content']}</p>
            '''
        return HttpResponse(html)
    else: 
        return HttpResponseNotFound("Post Not Available :<")
    
def google(request, id):
    url = reverse("post",args=[id])
    return HttpResponseRedirect(f'/post/{id}/')