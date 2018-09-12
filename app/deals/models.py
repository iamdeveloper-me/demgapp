from django.db import models
from datetime import datetime
from app.job.models import Job

class Deals(models.Model):
	custom = models.ForeignKey(Job,on_delete=models.DO_NOTHING)
	name  =  models.CharField(max_length=500)
	tags   =  models.CharField(max_length=500)
	related_to = models.CharField(max_length=500)
	is_deleted = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


	class Meta:
		managed = True
		db_table = 'deal'
		ordering = ['id']

