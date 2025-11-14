from django.contrib import admin
from .models import Business, Task


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name', 'user__username')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'amount', 'creator', 'receiver', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    # Task.creator and Task.receiver are Business FKs; to search by user use the relation through Business.user
    search_fields = ('title', 'description', 'creator__user__username', 'receiver__user__username')
