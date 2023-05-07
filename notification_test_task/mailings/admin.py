from django.contrib import admin
from .models import *

# Register your models here.


class MailingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'start_date',
        'end_date'
    )
    list_display_links = (
        'id',
        'start_date'
    )
    search_fields = (
        'id',
        'start_date',
        'end_date',
        'message'
    )
    list_filter = (
        'start_date',
        'end_date'
    )


class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'phone_number',
        'tag',
        'timezone'
    )
    list_display_links = (
        'id',
        'phone_number'
    )
    search_fields = (
        'id',
        'phone_number',
        'tag',
        'timezone'
    )
    list_filter = (
        'phone_number',
        'tag',
        'timezone'
    )


class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'sending_date',
        'mailing_id',
        'client_id',
        'sending_status'
    )
    list_display_links = (
        'id',
        'sending_date',
        'mailing_id',
        'client_id',
    )
    search_fields = (
        'id',
        'sending_date',
        'mailing_id',
        'client_id',
    )
    list_filter = (
        'sending_date',
        'mailing_id',
        'client_id'
    )
    list_editable = ['sending_status']


admin.site.register(Mailing, MailingAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Message, MessageAdmin)