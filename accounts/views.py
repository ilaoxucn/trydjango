from django.contrib import auth
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm


def register_view(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user_obj = form.save()
        return redirect("/login/")
    context = {
        "form":form
    }
    return render(request,"accounts/register.html",context)


def login_view(request):
    
    form = AuthenticationForm(request)
    if request.user.is_authenticated:
        return render(request,"accounts/already_login.html",{})
    if request.method=='POST':
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect("/")
    context = {"form":form}
    
        
    return render(request,"accounts/login.html",context)

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect("/login/")
    return render(request,"accounts/logout.html",{})