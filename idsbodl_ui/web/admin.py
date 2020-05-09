from django.contrib import admin

# Register your models here.
from .models import Users, NidsDatas, NidsProtocolTypes, NidsServices, NidsFlags, NidsLabels


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ['pk', 'username', 'password', 'email', 'phone']


@admin.register(NidsProtocolTypes)
class NidsProtocolTypesAdmin(admin.ModelAdmin):
    list_display = ['pk', 'protocol_name']
    

@admin.register(NidsFlags)
class NidsFlagsAdmin(admin.ModelAdmin):
    list_display = ['pk', 'flag_name']


@admin.register(NidsLabels)
class NidsLabelsAdmin(admin.ModelAdmin):
    list_display = ['pk', 'label_name']


@admin.register(NidsServices)
class NidsServicesAdmin(admin.ModelAdmin):
    list_display = ['pk', 'service_name']


@admin.register(NidsDatas)
class NidsDatasAdmin(admin.ModelAdmin):
    list_display = ['pk', 'src', 'dst', 'sport', 'dport', 'fk_nids_protocol_type', 'urgent', 'hot', 'src_bytes', 'dst_bytes', 'data_number', 'fk_nids_service', 'fk_nids_flag', 'duration', 'time', 'count']

