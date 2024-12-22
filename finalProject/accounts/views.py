from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework.authtoken.models import Token

from .forms import CreateUserForm, ChangeUserForm

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@login_required(login_url='login')
def editPage(request):
    user = request.user
    form = ChangeUserForm(instance=user)
    if request.method == 'POST':
        form = ChangeUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been updated successfully.')
            return redirect('edit-user')
        else:
            print(form.errors)
            messages.error(request, 'There was an error updating your account.')

    context = {'form': form}
    return render(request, 'accounts/account_center.html', context)


def loginPage(request):
    # Redirect authenticated users to the home page
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Login the user
            login(request, user)

            # Generate or get the token for the logged-in user
            token, created = Token.objects.get_or_create(user=user)
            print(f"Generated Token: {token.key}")  # Log the token for debugging

            # Optionally, you can return the token as part of the response (for API-based login)
            # For now, we'll simply redirect the user to home
            messages.success(request, f'Welcome {user.username}!')
            
            # Store the token for the session (optional for front-end usage)
            request.session['token'] = token.key

            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')
