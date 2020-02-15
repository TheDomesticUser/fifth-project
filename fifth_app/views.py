from django.shortcuts import render
from fifth_app.forms import UserForm, UserProfileInfoForm

# Login functionality
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'fifth_app/index.html')

def register(request):
    print(request.FILES)
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save() # Hash the password before storing it in the db

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user # Set the one to one field

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'fifth_app/register.html', context={
        'registered': registered,
        'user_form': user_form,
        'profile_form': profile_form
    })

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_active:
                login(request, user)
                
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('Account not active')
        else:
            print('Failed authentication')

            return HttpResponse('Invalid login details supplied')
    else:
        return render(request, 'fifth_app/login.html')

@login_required
def user_logout(request):
    logout(request)
    
    return HttpResponseRedirect(reverse('index'))