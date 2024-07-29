from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

def userLogin(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        if (email and password):
            try:
                user = authenticate(request, username=email, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, "Login Successful")
                    return redirect('home')
                
                else:
                    messages.info(request, "Invalid credentials.")
            except Exception as e:
                messages.info(request, "An error occurred: {}".format(e))

        else:
            messages.info(request, "Email ID or Password can't be null")
        
    return render(request, "login.html")

def userSignup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        password = request.POST.get('password')
        retypePassword = request.POST.get('retypePassword')
        gender = request.POST.get('gender')
        dob = '-'.join(request.POST.get('dob').split('-')[::-1])

        #empty feilds?
        if (email and firstName and lastName and password and retypePassword and gender and dob):
            #passwords matched?
            if password == retypePassword:
                #user exists?
                if not User.objects.filter(username=email).exists():
                    newUser = User.objects.create_user(email=email, username=email, password=password, first_name= firstName, last_name= lastName,)
                    newUser.save()
                    login(request, newUser)
                    return redirect('home')
                else:
                    messages.info(request, "An account with this email already exists.")
            else:
                messages.info(request, "Passwords did not match.")
        else:
            messages.info(request, "Invalid Information!")
        
    return render(request, "signup.html")

def userLogout(request):
    logout(request)
    print('logging out')
    return redirect(userLogin)