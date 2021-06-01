from django.forms import ModelForm
from .models import Books, Borrow


class CreateBookForm(ModelForm):
    class Meta:
        model = Books
        fields = "__all__"


class BorrowForms(ModelForm):
    class Meta:
        model = Borrow
        fields = "__all__"
