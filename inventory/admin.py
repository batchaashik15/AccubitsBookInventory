from django.contrib import admin
from .models import Books, Borrow, Customer

# Register your models here.
admin.site.register(Books)
admin.site.register(Borrow)
admin.site.register(Customer)
