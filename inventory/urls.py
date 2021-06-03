from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginuser, name="login"),
    path('register/', views.register, name="register"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('user-page/', views.userPage, name="user-page"),
    path('logout/', views.logoutuser, name="logout"),
    # CRUD
    path('create_book/', views.create_book, name="create_book"),
    path('update_stock/<str:book_id>/', views.update_stock, name="update_stock"),
    path('view_books/', views.view_books, name="view_books"),
    path('view_book/<str:pk>', views.view_book, name="view_book"),
    path('borrow_book/<str:book_id>/', views.borrow_book, name="borrow_book"),
    path('return_book/<str:book_id>/', views.return_book, name="return_book"),
]
