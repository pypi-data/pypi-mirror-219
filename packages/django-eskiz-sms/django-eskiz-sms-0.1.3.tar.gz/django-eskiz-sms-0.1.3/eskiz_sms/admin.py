from django.contrib import admin
from .models import EskizSMS, SMSLog


@admin.register(EskizSMS)
class EskizSMSAdmin(admin.ModelAdmin):
    list_display = ('email', 'password', 'from_name', 'callback_url', 'last_updated', 'eskiz_token')


@admin.register(SMSLog)
class SMSLogAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'message', 'from_name', 'status', 'status_date', 'error_message', 'from_app')
    list_filter = ['status', 'from_app', 'from_name', 'status_date' ]
    search_fields = ['phone_number', 'message' ]
