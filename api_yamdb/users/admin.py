from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name',)
    search_fields = ('first_name', 'last_name',)
    list_filter = ('date_joined',)
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
