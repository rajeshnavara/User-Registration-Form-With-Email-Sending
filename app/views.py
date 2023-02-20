from django.shortcuts import render
from app.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.


def Main(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'Main.html',d)
    return render(request,'Main.html')


def registration(request):
    uf=UserForm()
    pf=ProfileForm()
    d={'uf':uf,'pf':pf}
    
    if request.method=='POST' and request.FILES:
        One=UserForm(request.POST)
        Two=ProfileForm(request.POST,request.FILES)
        if One.is_valid() and Two.is_valid():
            UA=One.save(commit=False)
            password=One.cleaned_data['password']
            UA.set_password(password)
            UA.save()
            PA=Two.save(commit=False)
            PA.Pro_User=UA
            PA.save()
            
            send_mail('registration',
                      'Thanks For Registration',
                      'navararajesh39@gmail.com',
                      [UA.email],
                      fail_silently=False)
            
            return HttpResponse('Registration is Successful')
    
    return render(request,'registration.html',d)

def user_login(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']
        user=authenticate(username=username,password=password)
        
        if user and user.is_active:
            login(request,user)
            request.session['username']=username
            return HttpResponseRedirect(reverse('Main'))
        else:
            return HttpResponse('<h4>Please register before login to Website. Your Credentials are not found.</h4>')
    
        
    return render(request,'user_login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('Main'))


@login_required
def view_profie(request):
    un=request.session.get('username')
    UO=User.objects.get(username=un)
    PO=Profile.objects.get(Pro_User=UO)
    d={'UO':UO,'PO':PO}
    return render(request,'view_profie.html',d)

@login_required
def change_password(request):
    if request.method=='POST':
        un=request.session.get('username')
        pw=request.POST['password']
        UO=User.objects.get(username=un)
        UO.set_password(pw)
        UO.save()
        return HttpResponse('Password is changed successfully')
    return render(request,'change_password.html')


def forget_password(request):
    if request.method=='POST':
        un=request.POST['username']
        pw=request.POST['password']
        LUO=User.objects.filter(username=un)
        if LUO:
            UO=LUO[0]
            UO.set_password(pw)
            UO.save()
            return HttpResponse('Password reset is done Successfully')
        else:
            return HttpResponse('User not Found')
    return render(request,'forget_password.html')