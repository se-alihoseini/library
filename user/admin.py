from django.contrib import admin
from user.models import User, OtpCode
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from user.forms import UserCreationForm, UserChangeForm


class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'created_at')


admin.site.register(OtpCode, OtpCodeAdmin)


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('email', 'phone_number', 'is_admin')
    list_filter = ('is_admin',)

    fieldsets = (
        ('personal information', {'fields': ('email', 'first_name', 'phone_number', 'image', 'password', 'last_login')}),
        ('permissions', {'fields': ('status', 'is_admin', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        ('personal information', {'fields': ('email', 'first_name', 'phone_number', 'image', 'password', 'last_login')}),
        ('permissions', {'fields': ('status', 'is_admin', 'is_superuser', 'groups', 'user_permissions')}),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')


admin.site.register(User, UserAdmin)
