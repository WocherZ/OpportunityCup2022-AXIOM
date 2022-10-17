from django.contrib import admin
from .models import Transaction

class TransactionAdmin(admin.ModelAdmin):
    pass

admin.register(Transaction, TransactionAdmin)
