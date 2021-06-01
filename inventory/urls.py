from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginuser, name="login"),
    path('register/', views.register, name="register"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('logout/', views.logoutuser, name="logout"),
    # CRUD
    path('create_book/', views.create_book, name="create_book"),
    path('view_books/', views.view_books, name="view_books"),
    path('view_book/<str:pk>', views.view_book, name="view_book"),
]
