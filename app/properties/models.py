from django.db import models
from datetime import datetime


class Property(models.Model):
	name = models.CharField(max_length=200)
	ptype = models.CharField(max_length=500)
	value = models.CharField(max_length=500)
	subtype = models.TextField(null=True,blank=True)
	is_deleted = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True, blank=True)
	updated_at = models.DateTimeField(auto_now_add=True, blank=True)

