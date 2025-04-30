from django.contrib import admin
from .models import CustomUser, OTP

admin.site.register(CustomUser)


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ["email", "created_at", "expires_at"]
    readonly_fields = ["created_at", "expires_at"]
