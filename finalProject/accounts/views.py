from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

# Create your views here.
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

    context = {'form':form}
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
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info (request, 'Username OR Password is incorrect')

        context = {}
        return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')