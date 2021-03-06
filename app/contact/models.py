from django.db import models
from datetime import datetime

class Contact(models.Model):
	name       =  models.CharField(max_length=500)
	location   =  models.CharField(max_length=500)
	is_deleted = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


	class Meta:
		managed = True
		db_table = 'contact'
		ordering = ['id']