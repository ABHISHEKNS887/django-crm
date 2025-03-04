from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, AddRecordForm
from django.contrib import messages
from .models import Record

# Create your views here.

def home(request):
    records = Record.objects.all()
    
    # Check to see if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'{user.username.capitalize()}, You are now logged in')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('home')
    return render(request, 'home.html', {'records': records})

def login_user(request):
    pass

def logout_user(request):
    logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate the user
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'{username.capitalize()}, Your account has been created')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

def custom_record(request, id):
    if request.user.is_authenticated:
        custom_record = Record.objects.get(pk=id)
        return render(request, 'records.html', {'custom_record': custom_record})
    else:
        messages.warning(request, 'You must be logged in to view that page')
        return redirect('home')
    
def delete_record(request, id):
    if request.user.is_authenticated:
        record = Record.objects.get(pk=id)
        record.delete()
        messages.success(request, 'Record deleted successfully')
    else:
        messages.warning(request, 'You must be logged in to delete that record')
    return redirect('home')

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                record = form.save(commit=False)
                record.user = request.user
                record.save()
                messages.success(request, 'Record added successfully')
                return redirect('home')
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.warning(request, 'You must be logged in to add a record')
        return redirect('home')
    
def update_record(request, id):
    if request.user.is_authenticated:
        current_record = Record.objects.get(pk=id)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record updated successfully')
            return redirect('home')
        return render(request, 'update_record.html', {'form': form})
    else:
        messages.warning(request, 'You must be logged in to update a record')
        return redirect('home')
    
def clocl(request):
    pass
    