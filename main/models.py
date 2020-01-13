# coding=utf-8
from django.db import models

# Create your models here.

#Пользователей точно переопределять нужно? А то пароль прям так без шифровки будет...

class users(models.Model):
    iduser = models.IntegerField()
    name = models.CharField(max_length=45)
    surname = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    login = models.CharField(max_length=45)

class contacts(models.Model):
    idcontacts = models.IntegerField()
    iduser = models.IntegerField()
    their_contact = models.IntegerField()

class statuses(models.Model):
    idstatuses = models.IntegerField()
    status = models.CharField(max_length=200)
    users_iduser = models.IntegerField()

class messages(models.Model):
    idmessage = models.IntegerField()
    text = models.TextField()
    idcreate_user = models.IntegerField()
    dialogs_iddialogs = models.IntegerField()
    create_date = models.DateField()

class dialogs(models.Model):
    iddilogs = models.IntegerField()
    create_date = models.DateField()
    last_change = models.DateField()
    name = models.CharField(max_length=45)

class users_in_dialogs(models.Model):
    idusers_in_dialogs = models.IntegerField()
    users_iduser = models.IntegerField()
    dialogs_iddialogs = models.IntegerField()

class Message(models.Model):
    subject = models.CharField(max_length=200)
    body = models.TextField()
