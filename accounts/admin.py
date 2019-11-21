
# Register your models here.
from django.contrib import admin

from . models import MyUser
@admin.register(MyUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'student_id']
    list_display_links = ['username']