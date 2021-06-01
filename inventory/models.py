from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email


class Books(models.Model):
    book_name = models.CharField(max_length=200)
    author = models.CharField(max_length=200, null=True, blank=True)
    book_count = models.IntegerField(null=True, blank=True, default=1)

    def __str__(self):
        return self.book_name


class Borrow(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    book = models.ForeignKey(Books, null=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.book.book_name
