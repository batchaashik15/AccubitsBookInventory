from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .forms import CreateBookForm, BorrowForms
from .models import Books, Borrow


def loginuser(request):
    if request.method == "POST":
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'inventory/login.html', {'form': AuthenticationForm(), 'error': 'Please check your credentials'})
    return render(request, 'inventory/login.html')


def register(request):
    if request.method == 'GET':
        return render(request, 'inventory/register.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['email'], first_name=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('dashboard')
            except IntegrityError:
                return render(request, 'inventory/register.html', {'form': UserCreationForm(), 'error': 'User already exists. Please choose a new username'})
        else:
            # Tell the user that password diddnt match
            return render(request, 'inventory/register.html', {'form': UserCreationForm(), 'error': 'Password did not match'})


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')


@login_required
def dashboard(request):
    books = Borrow.objects.all()

    context = {"books": books}
    return render(request, 'inventory/dashboard.html', context)


# CRUD
@login_required
def create_book(request):
    form = CreateBookForm()
    if request.method == "POST":
        form = CreateBookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    context = {'form': form}
    return render(request, 'inventory/create_book.html', context)


@login_required
def view_books(request):
    books = Books.objects.all()
    context = {"books": books}
    return render(request, 'inventory/view_books.html', context)


@login_required
def view_book(request, pk):
    books = Books.objects.get(id=pk)
    context = {"book": books}
    return render(request, 'inventory/view_book.html', context)


@login_required
def borrow_book(request):
    form = BorrowForms()
    if request.method == "POST":
        form = BorrowForms(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    context = {'form': form}
    return render(request, 'inventory/borrow_book.html', context)
