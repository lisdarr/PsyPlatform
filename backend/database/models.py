# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ConDirRecord(models.Model):
    con_dir_id = models.IntegerField(blank=True, null=True)
    con_id = models.IntegerField(blank=True, null=True)
    dir_id = models.IntegerField(blank=True, null=True)
    stime = models.DateTimeField(blank=True, null=True)
    duration = models.BigIntegerField(blank=True, null=True)
    record = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'con_dir_record'


class ConSchedule(models.Model):
    con_id = models.IntegerField(blank=True, null=True)
    weekday = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'con_schedule'


class ConToday(models.Model):
    con_id = models.IntegerField(blank=True, null=True)
    state = models.IntegerField(blank=True, null=True)
    today_num = models.IntegerField(blank=True, null=True)
    today_dur = models.BigIntegerField(blank=True, null=True)
    now_num = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'con_today'


class Consultant(models.Model):
    con_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=254, blank=True, null=True)
    sex = models.CharField(max_length=254, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    identity = models.CharField(max_length=254, blank=True, null=True)
    tele = models.CharField(max_length=254, blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    username = models.CharField(max_length=254, blank=True, null=True)
    password = models.CharField(max_length=254, blank=True, null=True)
    unit = models.CharField(max_length=254, blank=True, null=True)
    title = models.CharField(max_length=254, blank=True, null=True)
    icon = models.TextField(blank=True, null=True)
    av_score = models.FloatField(blank=True, null=True)
    totel_num = models.IntegerField(blank=True, null=True)
    totel_dur = models.BigIntegerField(blank=True, null=True)
    dir_id = models.IntegerField(blank=True, null=True)
    u_ticket = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'consultant'


class DirSchedule(models.Model):
    dir_id = models.IntegerField(blank=True, null=True)
    weekday = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dir_schedule'


class DirToday(models.Model):
    dir_id = models.IntegerField(blank=True, null=True)
    today_num = models.IntegerField(blank=True, null=True)
    today_dur = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dir_today'


class Director(models.Model):
    dir_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=254, blank=True, null=True)
    sex = models.CharField(max_length=254, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    identity = models.CharField(max_length=254, blank=True, null=True)
    tele = models.CharField(max_length=254, blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    username = models.CharField(max_length=254, blank=True, null=True)
    password = models.CharField(max_length=254, blank=True, null=True)
    unit = models.CharField(max_length=254, blank=True, null=True)
    title = models.CharField(max_length=254, blank=True, null=True)
    qual = models.CharField(max_length=254, blank=True, null=True)
    qualnum = models.CharField(max_length=254, blank=True, null=True)
    icon = models.TextField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    duration = models.BigIntegerField(blank=True, null=True)
    u_ticket = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'director'


class Visitor(models.Model):
    vis_id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=254, blank=True, null=True)
    name = models.CharField(max_length=254, blank=True, null=True)
    tele = models.CharField(max_length=254, blank=True, null=True)
    emer_name = models.CharField(max_length=254, blank=True, null=True)
    emer_tele = models.CharField(max_length=254, blank=True, null=True)
    icon = models.TextField(blank=True, null=True)
    ban = models.IntegerField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    u_ticket = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'visitor'


class VisitorConRecord(models.Model):
    vis_con_id = models.IntegerField(blank=True, null=True)
    vis_id = models.IntegerField(blank=True, null=True)
    con_id = models.IntegerField(blank=True, null=True)
    his_state = models.IntegerField(blank=True, null=True)
    stime = models.DateTimeField(blank=True, null=True)
    duration = models.BigIntegerField(blank=True, null=True)
    record = models.CharField(max_length=254, blank=True, null=True)
    v2c_score = models.FloatField(blank=True, null=True)
    v2c_comm = models.CharField(max_length=254, blank=True, null=True)
    c2v_score = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'visitor_con_record'
