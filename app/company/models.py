from django.db import models
from datetime import datetime


class Company(models.Model):
	company_id =  models.CharField(max_length=500)
	tags   =  models.CharField(max_length=500)
	company_name = models.CharField(max_length=2000,default='')
	is_deleted = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


	class Meta:
		managed = True
		db_table = 'company'
		ordering = ['id']
