from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdming
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext as _
from .models import User, Post,DashboardPost,Field


class UserAdmin(BaseUserAdming):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('email', 'first_name', 'last_name', 'education', 'field')
    list_filter = ('email', 'first_name', 'last_name', 'education', 'field')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'field','education')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       )}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    ordering = ('email',)


admin.site.register(User, UserAdmin)
admin.site.register(Post)
admin.site.register(DashboardPost)
admin.site.register(Field)
# admin.site.register(RequestModel)
# admin.site.register(Algorithm)
