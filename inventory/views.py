from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .forms import CreateBookForm, BorrowForms
from .models import Books, Borrow
from django.forms import inlineformset_factory
from .decorators import *
from django.db.models import F
from .filters import *


@unauthorized_users
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


@unauthorized_users
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


@login_required(login_url="login")
@admin_only
def dashboard(request):
    users = User.objects.all()
    borrows = Borrow.objects.all()

    myFilter = BorrowFilter(request.GET, queryset=borrows)
    borrows = myFilter.qs

    books = Books.objects.all().order_by('-book_count')

    context = {"users": users, "borrows": borrows,
               "books": books, "myFilter": myFilter}
    return render(request, 'inventory/dashboard.html', context)


@login_required(login_url="login")
def userPage(request):
    borrows = request.user.borrow_set.filter(quantity__gte=1)

    books = Books.objects.filter(book_count__gte=1).order_by('-book_count')
    context = {"borrows": borrows, "books": books}
    return render(request, 'inventory/userPage.html', context)

# CRUD


@login_required(login_url="login")
def create_book(request):
    form = CreateBookForm()
    if request.method == "POST":
        form = CreateBookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    context = {'form': form}
    return render(request, 'inventory/create_book.html', context)


@login_required(login_url="login")
def update_stock(request, book_id):
    book = Books.objects.get(id=book_id)
    form = CreateBookForm(instance=book)
    if request.method == "POST":
        form = CreateBookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    context = {'form': form}
    return render(request, 'inventory/create_book.html', context)


@login_required(login_url="login")
def view_books(request):
    books = Books.objects.all()
    context = {"books": books}
    return render(request, 'inventory/view_books.html', context)


@login_required(login_url="login")
def view_book(request, pk):
    books = Books.objects.get(id=pk)
    context = {"book": books}
    return render(request, 'inventory/view_book.html', context)


def adjust_stock(book_id, do="reduce"):
    # To reduce the count from the Book class
    book = Books.objects.get(id=book_id)
    if do == "add":
        book.book_count = F("book_count") + 1
    else:
        book.book_count = F("book_count") - 1
    book.save(update_fields=["book_count"])


@login_required(login_url="login")
def borrow_book(request, book_id):
    user = User.objects.get(id=request.user.id)
    books = user.borrow_set.all()
    for book in books:
        if str(book.book.id) == book_id:
            # To increment the count in user's borrow class
            print(book.id)
            borrow_obj = Borrow.objects.get(id=book.id)
            borrow_obj.quantity = F("quantity") + 1
            borrow_obj.save(update_fields=["quantity"])

            adjust_stock(book_id)
            return redirect('user-page')

    book = Books.objects.get(id=book_id)
    borrows = Borrow(user=request.user, book=book)
    adjust_stock(book_id)
    borrows.save()
    return redirect("user-page")


@login_required(login_url="login")
def return_book(request, book_id):
    user = User.objects.get(id=request.user.id)
    books = user.borrow_set.all()
    for book in books:
        if str(book.book.id) == book_id:
            # To increment the count in user's borrow class
            print(book.id)
            borrow_obj = Borrow.objects.get(id=book.id)
            borrow_obj.quantity = F("quantity") - 1
            borrow_obj.save(update_fields=["quantity"])

            adjust_stock(book_id, "add")
            return redirect('user-page')

    return redirect("user-page")
