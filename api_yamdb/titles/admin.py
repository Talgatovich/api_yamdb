from django.contrib import admin

from .models import Title


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)
    search_fields = ('name', )
    list_filter = ('year',)
    


admin.site.register(Title, TitleAdmin)
