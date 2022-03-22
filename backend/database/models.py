# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ConDirRecord(models.Model):
    cd_id = models.AutoField(primary_key=True)
    con = models.ForeignKey('Consultant', models.DO_NOTHING, blank=True, null=True)
    dir = models.ForeignKey('Director', models.DO_NOTHING, blank=True, null=True)
    cd_stime = models.DateTimeField(blank=True, null=True)
    cd_duration = models.BigIntegerField(blank=True, null=True)
    cd_record = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'con_dir_record'


class ConSchedule(models.Model):
    con_sche_id = models.AutoField(primary_key=True)
    con = models.ForeignKey('Consultant', models.DO_NOTHING, blank=True, null=True)
    weekday = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'con_schedule'


class ConToday(models.Model):
    con_today_id = models.AutoField(primary_key=True)
    con = models.ForeignKey('Consultant', models.DO_NOTHING, blank=True, null=True)
    con_state = models.CharField(max_length=255, blank=True, null=True)
    con_today_num = models.IntegerField(blank=True, null=True)
    con_today_dur = models.BigIntegerField(blank=True, null=True)
    con_now_num = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'con_today'


class Consultant(models.Model):
    con_id = models.AutoField(primary_key=True)
    con_name = models.CharField(max_length=254, blank=True, null=True)
    con_sex = models.CharField(max_length=254, blank=True, null=True)
    con_age = models.IntegerField(blank=True, null=True)
    con_identity = models.CharField(max_length=254, blank=True, null=True)
    con_tele = models.CharField(max_length=254, blank=True, null=True)
    con_email = models.CharField(max_length=254, blank=True, null=True)
    con_username = models.CharField(max_length=254, blank=True, null=True)
    con_password = models.CharField(max_length=254, blank=True, null=True)
    con_unit = models.CharField(max_length=254, blank=True, null=True)
    con_title = models.CharField(max_length=254, blank=True, null=True)
    con_icon = models.TextField(blank=True, null=True)
    con_av_score = models.FloatField(blank=True, null=True)
    con_number = models.IntegerField(blank=True, null=True)
    con_duration = models.BigIntegerField(blank=True, null=True)
    dir = models.ForeignKey('Director', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'consultant'


class DirSchedule(models.Model):
    dir_sche_id = models.AutoField(primary_key=True)
    dir = models.ForeignKey('Director', models.DO_NOTHING, blank=True, null=True)
    weekday = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dir_schedule'


class DirToday(models.Model):
    dir_today_id = models.AutoField(primary_key=True)
    dir = models.ForeignKey('Director', models.DO_NOTHING, blank=True, null=True)
    dir_today_num = models.IntegerField(blank=True, null=True)
    dir_today_dur = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dir_today'


class Director(models.Model):
    dir_id = models.AutoField(primary_key=True)
    dir_name = models.CharField(max_length=254, blank=True, null=True)
    dir_sex = models.CharField(max_length=254, blank=True, null=True)
    dir_age = models.IntegerField(blank=True, null=True)
    dir_identity = models.CharField(max_length=254, blank=True, null=True)
    dir_tele = models.CharField(max_length=254, blank=True, null=True)
    dir_email = models.CharField(max_length=254, blank=True, null=True)
    dir_username = models.CharField(max_length=254, blank=True, null=True)
    dir_password = models.CharField(max_length=254, blank=True, null=True)
    dir_unit = models.CharField(max_length=254, blank=True, null=True)
    dir_title = models.CharField(max_length=254, blank=True, null=True)
    dir_qual = models.CharField(max_length=254, blank=True, null=True)
    dir_qualnum = models.CharField(max_length=254, blank=True, null=True)
    dir_icon = models.TextField(blank=True, null=True)
    dir_number = models.IntegerField(blank=True, null=True)
    dir_duration = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'director'


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=254, blank=True, null=True)
    user_tele = models.CharField(max_length=254, blank=True, null=True)
    emer_name = models.CharField(max_length=254, blank=True, null=True)
    emer_tele = models.CharField(max_length=254, blank=True, null=True)
    user_icon = models.TextField(blank=True, null=True)
    user_ban = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'


class UserConRecord(models.Model):
    uc_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    con = models.ForeignKey(Consultant, models.DO_NOTHING, blank=True, null=True)
    uc_his_state = models.IntegerField(blank=True, null=True)
    uc_stime = models.DateTimeField(blank=True, null=True)
    uc_duration = models.BigIntegerField(blank=True, null=True)
    uc_record = models.CharField(max_length=255, blank=True, null=True)
    u2c_score = models.FloatField(blank=True, null=True)
    c2u_score = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_con_record'
