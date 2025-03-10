from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from .forms import SignUpForm, AddRecordForm
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Record

# Create your views here.

def home(request):
    query = request.GET.get('q')  # Get search query from request
    records = Record.objects.filter(Q(first_name__icontains=query) |  # Search in first_name
                                    Q(last_name__icontains=query) |  # Search in last_name
                                    Q(email__icontains=query) | # Search in email
                                    Q(city__icontains=query) |
                                    Q(state__icontains=query) 
                                ) if query else Record.objects.all()
    paginator = Paginator(records, 5)  # Show 5 products per page

    page_number = request.GET.get('page')  # Get the page number from URL
    records = paginator.get_page(page_number)  # Get products for the requested pag
    
    # Check to see if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'{user.username.capitalize()}, You are now logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials... Please try again')
            return redirect('home')
    return render(request, 'home.html', {'query': query, 'records': records})

def logout_user(request):
    logout(request)
    messages.success(request, 'You are now logged out.')
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
            messages.success(request, f'{username.capitalize()}, Your account has been created.')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

def custom_record(request, id):
    if request.user.is_authenticated:
        custom_record = Record.objects.get(pk=id)
        return render(request, 'records.html', {'custom_record': custom_record})
    else:
        messages.warning(request, 'You must be logged in to view that page.')
        return redirect('home')
    
def delete_record(request, id):
    if request.user.is_authenticated:
        record = Record.objects.get(pk=id)
        record.delete()
        messages.success(request, 'Record deleted successfully.')
    else:
        messages.warning(request, 'You must be logged in to delete that record.')
    return redirect('home')

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                record = form.save(commit=False)
                record.user = request.user
                record.save()
                messages.success(request, 'Record added successfully.')
                return redirect('home')
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.warning(request, 'You must be logged in to add a record.')
        return redirect('home')
    
def update_record(request, id):
    if request.user.is_authenticated:
        current_record = Record.objects.get(pk=id)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record updated successfully.')
            return redirect('home')
        return render(request, 'update_record.html', {'form': form})
    else:
        messages.warning(request, 'You must be logged in to update a record.')
        return redirect('home')
