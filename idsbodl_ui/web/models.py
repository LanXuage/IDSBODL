# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class NidsDatas(models.Model):
    src = models.CharField(max_length=45)
    dst = models.CharField(max_length=45)
    sport = models.IntegerField()
    dport = models.IntegerField()
    fk_nids_protocol_type = models.ForeignKey('NidsProtocolTypes', models.DO_NOTHING, blank=True, null=True)
    urgent = models.IntegerField()
    hot = models.IntegerField()
    src_bytes = models.BigIntegerField()
    dst_bytes = models.BigIntegerField()
    data_number = models.CharField(max_length=45)
    fk_nids_service = models.ForeignKey('NidsServices', models.DO_NOTHING, blank=True, null=True)
    fk_nids_flag = models.ForeignKey('NidsFlags', models.DO_NOTHING, blank=True, null=True)
    duration = models.IntegerField()
    time = models.DateTimeField()
    count = models.IntegerField()
    srv_count = models.IntegerField()
    serror_rate = models.FloatField()
    rerror_rate = models.FloatField()
    same_srv_rate = models.FloatField()
    diff_srv_rate = models.FloatField()
    srv_serror_rate = models.FloatField()
    srv_rerror_rate = models.FloatField()
    srv_diff_host_rate = models.FloatField()
    dst_host_count = models.IntegerField()
    dst_host_srv_count = models.IntegerField()
    dst_host_same_srv_rate = models.FloatField()
    dst_host_diff_srv_rate = models.FloatField()
    dst_host_same_src_port_rate = models.FloatField()
    dst_host_serror_rate = models.FloatField()
    dst_host_rerror_rate = models.FloatField()
    dst_host_srv_diff_host_rate = models.FloatField()
    dst_host_srv_serror_rate = models.FloatField()
    dst_host_srv_rerror_rate = models.FloatField()
    fk_nids_label = models.ForeignKey('NidsLabels', models.DO_NOTHING, blank=True, null=True)
    capture_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'nids_datas'


class NidsFlags(models.Model):
    flag_name = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'nids_flags'


class NidsLabels(models.Model):
    label_name = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'nids_labels'


class NidsProtocolTypes(models.Model):
    protocol_name = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'nids_protocol_types'


class NidsServices(models.Model):
    service_name = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'nids_services'


class Users(models.Model):
    username = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    phone = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'users'
