from django.contrib import admin
# Register your models here.
from .models import CustomUser,Expense,Share

admin.site.register(CustomUser)
admin.site.register(Expense)
admin.site.register(Share)
