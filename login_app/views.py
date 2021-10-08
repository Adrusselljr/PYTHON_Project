from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User
import bcrypt

def index(request):
    return render(request, "index.html")

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if errors:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect('/')

    pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()

    User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email_address = request.POST['email_address'],
        password = pw_hash
    )
    messages.info(request, "REGISTRATION COMPLETE - Please login")

    return redirect('/')

def login(request):
    try:
        user = User.objects.get(email_address = request.POST['email_address'])
    except:
        messages.error(request, "This user does not exist!")
        return redirect('/')

    if not bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        messages.error(request, "Password incorrect!")
        return redirect('/')

    request.session['user_id'] = user.id
    request.session['email'] = user.email_address
    request.session['first_name'] = user.first_name
    request.session['last_name'] = user.last_name

    return redirect('/movies')

def success(request):
    if not 'user_id' in request.session:
        messages.error(request, "Log in to view this page!")
        return redirect('/')
    return render(request, "success.html")

def logout(request):
    request.session.clear()
    return redirect('/')