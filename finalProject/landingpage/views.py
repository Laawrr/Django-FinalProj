from django.shortcuts import render

def landingPage(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        login_url = 'login'  # For logged-in users, we could show 'logout'
    else:
        login_url = 'logout'  # For guests, show 'login' option
    
    context = {
        'login_url': login_url,
    }
    return render(request, 'landingpage/landing_page.html', context)
