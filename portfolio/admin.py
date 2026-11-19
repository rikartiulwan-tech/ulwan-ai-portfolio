from django.contrib import admin
from .models import ClientInquiry

@admin.register(ClientInquiry)
class ClientInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'business_type', 'package', 'email', 'created_at')
    list_filter = ('package', 'created_at')
    search_fields = ('name', 'email', 'business_type')