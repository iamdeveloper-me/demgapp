from django.db import models
from datetime import datetime
from app.company.models import Company

class Job(models.Model):
	
	job_name            =  models.CharField(max_length=255)
	job_location        =  models.CharField(max_length=500)
	owner_name          =  models.CharField(max_length=255) 
	owner_location      =  models.CharField(max_length=500)
	architect           =  models.CharField(max_length=255)
	engineer_name       =  models.CharField(max_length=255)
	contractor_customer =  models.CharField(max_length=500)
	file_upload         =  models.FileField(upload_to='Jobdocuments/')
	post_local_id       =  models.CharField(max_length=900,default='')
	is_deleted = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


	class Meta:
		managed = True
		db_table = 'job'
		ordering = ['id']
