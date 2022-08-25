import re
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.conf import settings
from django.contrib import messages
from dashboard.models import *
from auth_app.models import Person
from django.contrib.auth.decorators import login_required


from auth_app.forms import PersonRegistrationForm, PersonLogin,EditRegistrationForm

# Create your views here.
def register(request):
    if request.method == 'GET':
        form = PersonRegistrationForm
        return render(request,'register.html',{'form':form })
    else:
        form = PersonRegistrationForm(request.POST)
        if form.is_valid():
            fn= form.cleaned_data['first_name']
            ln=form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            uname= form.cleaned_data['username']
            pswd=form.cleaned_data['password']

            User.objects.create_user(first_name=fn,last_name=ln,email=email,username=uname,password=pswd)
            messages.success(request,'User created successfully')
            return redirect('Login')
        else:
            return render(request, 'register.html',{'form':form})

def sign_in(request):
    if request.method == 'GET':
        form=PersonLogin()
        return render(request,'login.html',{'form':form})
    else:
        next_url = request.GET.get('next')
        form = PersonLogin(request.POST)
        uname=request.POST['username']
        pswd=request.POST['password']
        user=authenticate(username=uname,password=pswd)
        if user is not None:
            login(request, user)
            if next_url is None:
                return redirect('home')
            else:
                return redirect(next_url)
        else:
            messages.error(request,'Invalid Username or password!!')
            messages.error(request,'Please try again.')
            return render(request,'login.html',{'form':form})

def sign_out(request):
    logout(request)
    return redirect('Login')

def profile(request):
    try:
        p = Person.objects.filter(user_id = request.user.id)[0]
        return render(request,'profile.html',{'p':p})
    except:
        messages.error(request,"please add your photo")
        return render(request,'profile.html')
        

    

def profile_edit(request):
    if request.method == 'GET':
        return render(request,"editpro.html")
    else:
        i = request.FILES['pp']
        Person.objects.create(user=request.user,profile_pic = i)
        return redirect("profile")

def editpin(request,id):
    try:
        E = User.objects.get(id=request.user.id)
    except:
        return HttpResponse('404 user does not exist')
    if request.method == 'GET':
        form = EditRegistrationForm(instance = E)
        return render(request, 'editpin.html',{'form':form})
    else:
        form = EditRegistrationForm(request.POST)
        fn= request.POST['first_name']
        ln=request.POST['last_name']
        email = request.POST['email']
        E.first_name=fn
        E.last_name=ln
        E.email=email
        E.save()
        return redirect('profile')

def del_user(request, id):    
    try:
        u = User.objects.get(id=id)
        u.delete()
        messages.success(request, "The user is deleted")
        return redirect('home')            

    except User.DoesNotExist:   
        return redirect('home')  

