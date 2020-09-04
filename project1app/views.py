from django.shortcuts import render, redirect
from django.contrib import messages
from.models import User, Gift
from django.db.models import Q
import bcrypt

def index(request):
    return render(request,'main.html')

def register(request):
    errors = User.objects.registerValidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    registered_user = User.objects.create(firstName=request.POST['firstName'], lastName=request.POST['lastName'],password=pw_hash, userName=request.POST['userName'],email=request.POST['email']) 
    request.session['id'] = registered_user.id
    return redirect("/success")

def success(request):
    if 'id' not in request.session:
        return redirect('/')
    context = {
        'registeredUser': User.objects.get(id=request.session['id']),
    }
    print(User.objects.get(id=request.session['id']))
    return render(request,'registerSuccess.html',context)

def login(request):
    errors = User.objects.loginValidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    user = User.objects.filter(userName=request.POST['userName'])
    if user:
        logged_user = user[0] 
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['id'] = logged_user.id
            return redirect('/dashboard')
    return redirect("/")

def dashboard(request):
    if 'id' not in request.session:
        return redirect('/')
    context = {
        'loggedInUser': User.objects.get(id=request.session['id']),
        'newGift': Gift.objects.filter(uploader= User.objects.get(id=request.session['id']))
    }
    return render(request,'dashboard.html', context)

def share(request):
    context = {
        'newGift': Gift.objects.filter(uploader= User.objects.get(id=request.session['id']))
    }
    return render(request,'share.html',context)

def addGift(request):
    newGift = Gift.objects.create(gift = request.POST['gift'],image = request.POST['image'], uploader= User.objects.get(id=request.session['id']))
    return redirect('/dashboard')

def logout(request):
    request.session.clear()
    return redirect("/")

def delete(request, idGift):
    deletedItem = Gift.objects.get(id=idGift)
    deletedItem.delete()
    return redirect('/dashboard')
