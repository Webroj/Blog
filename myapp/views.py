from django.shortcuts import render, HttpResponseRedirect
from .forms import SignUpForm, LoginForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Post
from django.contrib.auth.models import Group


# Create your views here.

# Home 
def home(request):
    postdata=Post.objects.all()
    return render(request, 'home.html', {'post':postdata})

# About 
def about(request):
    return render(request, 'about.html')

# Contact
def contact(request):
    return render(request, 'contact.html')

# Dashboard
def dashboard(request):
    if request.user.is_authenticated:
        userdashboard=Post.objects.all()
        duser=request.user
        fullname=duser.get_full_name() 
        dgroups=duser.groups.all()
        return render(request, 'dashboard.html', {'dashboard':userdashboard, 'compname':fullname, 'grp':dgroups})
    else:
        return HttpResponseRedirect('/login/')


# Signup 
def user_signup(request):
    if request.method=="POST":
        userform=SignUpForm(request.POST)
        if userform.is_valid():
            messages.success(request, 'Congratulations you have Successfully SignUp !!')
            user=userform.save()
            userform=SignUpForm()
            group=Group.objects.get(name='Author')
            user.groups.add(group)
    else:
        userform=SignUpForm()
    return render(request, 'signup.html',{'form':userform})
    
# Login 
def user_login(request):
    # if user login nhi h tb ye process follow hoga
    if not request.user.is_authenticated:
        if request.method=="POST":
            loginform=LoginForm(request=request, data=request.POST)
            if loginform.is_valid():
                uname=loginform.cleaned_data['username']
                upass=loginform.cleaned_data['password']
                user=authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in Successfully !!')
                    return HttpResponseRedirect('/dashboard/')
        else:
            loginform=LoginForm()
        return render(request, 'login.html', {'form':loginform})
    else:
        return HttpResponseRedirect('/dashboard/')

# logout 
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

# Add New Post
def add_post(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            addform=PostForm(request.POST)
            if addform.is_valid():
                titledata=addform.cleaned_data['title']
                descdata=addform.cleaned_data['desc']
                compform=Post(title=titledata, desc=descdata)
                compform.save() 
                addform=PostForm()
        else:
            addform=PostForm()
        return render(request, 'add.html',{'addsform':addform})
    else:
        return HttpResponseRedirect('/login/')


# Update Post
def update_post(request, id):
    if request.user.is_authenticated:
        if request.method=="POST":
            pi=Post.objects.get(pk=id)
            uform=PostForm(request.POST, instance=pi)
            if uform.is_valid():
                uform.save()
        else:
            pi=Post.objects.get(pk=id)
            uform=PostForm(instance=pi)
        return render(request, 'update.html',{'uuform':uform})
    else:
        return HttpResponseRedirect('/login/')


# Delete Post
def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method=="POST":
            pi=Post.objects.get(pk=id)
            pi.delete()
        return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')
