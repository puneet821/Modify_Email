from django.contrib import admin
from .models import Email


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sender', 'received_date', 'is_read', 'is_starred')
    list_filter = ('is_read', 'is_starred', 'received_date')
    search_fields = ('subject', 'body', 'sender')
    ordering = ('-received_date',)
