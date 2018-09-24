from django.db import models
from datetime import datetime


class Owner(models.Model):
	name = models.CharField(max_length=200)
	domain = models.CharField(max_length=200)
	email = models.EmailField(max_length=200,unique=True)
	pic = models.FileField(upload_to='Jobdocuments/')
	password = models.CharField(max_length=50)
	calendar_url = models.TextField(null=True,blank=True)
	is_admin = models.NullBooleanField(blank=True)
	is_account_owner = models.NullBooleanField(blank=True)
	is_disabled = models.NullBooleanField(blank=True)
	schedule_id = models.CharField(max_length=200)
	is_deleted = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True, blank=True)
	updated_at = models.DateTimeField(auto_now_add=True, blank=True)


