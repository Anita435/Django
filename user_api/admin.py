from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from .models import User, OTPDetails, UserProfile, UserLoginActivity


@admin.register(User)
class UserAdmin(ImportExportActionModelAdmin,admin.ModelAdmin):
    list_display = ('id','email','is_active','is_staff')

    def email(self, obj):
        if obj.user and obj.user.email:
            return obj.user.email
        return ''


@admin.register(OTPDetails)
class OTPDetailsAdmin(ImportExportActionModelAdmin,admin.ModelAdmin):
    list_display = ('id','otp_response','user')
    # readonly_fields = ('user',)


@admin.register(UserProfile)
class UserProfileAdmin(ImportExportActionModelAdmin,admin.ModelAdmin):
    list_display = ('id','first_name','last_name',)


@admin.register(UserLoginActivity)
class UserLoginActivityAdmin(admin.ModelAdmin):
    search_fields = ('login_IP','login_username',)
    list_display = ('login_IP','login_datetime','login_username','status',)
    list_filter = ('login_datetime','login_username','login_IP',)
