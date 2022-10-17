from django.contrib import admin

from .models import User


class AdminUser(admin.ModelAdmin):
    list_display = ('username',
                    'email',
                    'role',
                    )
    search_fields = ('username',)


admin.site.register(User, AdminUser)
