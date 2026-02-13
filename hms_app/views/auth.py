from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from ..models import User, CollectorProfile, RetailerProfile

def register_view(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        phone = request.POST.get('phone')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=fname,
            last_name=lname,
            role=role,
            phone=phone
        )

        if role == 'COLLECTOR':
            CollectorProfile.objects.create(
                user=user,
                region=request.POST.get('region'),
                license_id=request.POST.get('license_id')
            )
        elif role == 'RETAILER':
            RetailerProfile.objects.create(
                user=user,
                shop_name=request.POST.get('shop_name'),
                address=request.POST.get('address')
            )

        login(request, user)
        return redirect('/')

    return render(request, 'auth/register_page.html')

def login_view(request):
    if request.method == 'POST':
        u_name = request.POST.get('username')
        p_word = request.POST.get('password')

        user = authenticate(request, username=u_name, password=p_word)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('/')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'auth/login_page.html')

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('/')