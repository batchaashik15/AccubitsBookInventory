# Generated by Django 3.2 on 2021-06-03 05:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_alter_borrow_book'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrow',
            name='book',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.books'),
        ),
    ]
