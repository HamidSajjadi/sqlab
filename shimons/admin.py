from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdming
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext as _
from .models import UserProfile, Post, DashboardPost, Field


class UserAdmin(BaseUserAdming):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('email', 'first_name', 'last_name', 'education', 'field', 'is_staff')
    list_filter = ('email', 'first_name', 'last_name', 'education', 'field', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'field','education')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       )}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    ordering = ('email',)


admin.site.register(UserProfile, UserAdmin)
admin.site.register(Post)
admin.site.register(DashboardPost)
admin.site.register(Field)
