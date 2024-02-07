from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

def home(request):
    if request.user.is_authenticated:
        user = request.user
        records = Record.objects.all()
        return render(request, 'home.html', {'user': user,'records': records})
    else:
        messages.success(request, "Please log in first.")
        return redirect('login') 


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password'] #using name field from the input form
        #Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, "There was an error logging in, Try again!")
            return redirect('login')
    else:
        return render(request, 'login.html', {})
    
    
def logout_user(request):
    logout(request)
    return redirect('login')


def register_user(request):
    if request.method == "POST":
        form =  SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and Login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, " Account registered successfully!")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})


def cutomer_record(request, pk):
    if request.user.is_authenticated:
        #look up records
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        messages.success(request, "You must be logged in to view the records!")
        return redirect('login')

def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record Deleted Successfully!")
        return redirect('home')
    else:
        messages.success(request, "You must be logged in to do that")
        return redirect('login')

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, "Record Added Sucessfully")
                return redirect('home')
        return render(request, 'add_record.html',  {"form": form})
    else:
        messages.success(request, "You must be logged in to add a new record!")
        return redirect('login')

def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Updated Sucessfully")
            return redirect('home')
        return render(request, 'update_record.html',  {"form": form})
    else:
        messages.success(request, "You must be logged in to update record!")
        return redirect('login')





