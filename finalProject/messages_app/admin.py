from django.contrib import admin
from .models import *



@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('user__username', 'content')
    readonly_fields = ('content',)