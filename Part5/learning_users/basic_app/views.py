from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'basic_app/index.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered = False

    if request.method =="POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save()
            # Hash the password:
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False) #DO NOT COMMIT TO THE DATABASE BEFORE MAKING CHANGES IF APPLICABLE.
            profile.user = user #sets up oneToOne relationship.

            if 'profile_pics' in request.FILES:
                # Check if picture is present.
                profile.profile_pic = request.FILES['profile_pics']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'basic_app/registration.html',{'user_form': user_form,
                                                          'profile_form':profile_form,
                                                          'registered': registered})


def user_login(request):

    if request.method=="POST":
        username= request.POST.get('username')
        password=request.POST.get('password')
        # Automatically authenticate the user:
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                #redicrect back to the home page if account is active.
                return HttpResponseRedirect(reverse('index'))
            
            else:
                return HttpResponse("Account not active")
            
        else:
            print("Someone tried to login and failed.")
            print("Username",username)
            print("Password",password)
            return HttpResponse('Invalid Login details supplied.')
        
    else:
        return render(request, 'basic_app/login.html',{})

        