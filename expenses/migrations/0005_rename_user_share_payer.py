# Generated by Django 5.0.4 on 2024-04-14 15:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0004_remove_expense_amount_currency_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='share',
            old_name='user',
            new_name='payer',
        ),
    ]
