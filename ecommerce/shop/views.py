from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponse
from django.shortcuts import render, redirect
from shop.models import Category,Product
from django.contrib.auth.models import User
def allcategories(request):
    c=Category.objects.all()
    return render(request,'category.html',{'c':c})
def allproducts(request,p):
    c=Category.objects.get(name=p)
    p=Product.objects.filter(category=c)
    return render(request,'product.html',{'c':c,'p':p})
def details(request,c):
    p=Product.objects.get(name=c)
    return render(request,'details.html',{'p':p})
def register(request):
    if(request.method=="POST"):
        u = request.POST.get('username', '')
        p = request.POST.get('password', '')
        e = request.POST.get('email', '')
        cp = request.POST.get('confirm password','')
        f = request.POST.get('first_name', '')
        l = request.POST.get('last_name', '')

        if (p == cp):
            a = User.objects.create_user(username=u, password=p, confirm_password=cp, email=e, first_name=f, last_name=l)
            user.save()
            return redirect('shop:allcat')
        else:
            return HttpResponse("Password are not same")
    return render(request,'register.html')
def user_login(request):
    if(request.method=="POST"):
        u=request.POST['u']
        p=request.POST['p']
        user=authenticate(user_name=u,password=p)
        if user:
            login(request,user)
            return redirect('shop:allcat')
        else:
            return HttpResponse("invalid credentials")



    return render(request,'login.html')




def user_logout(request):
    logout(request)
    return user_login(request)