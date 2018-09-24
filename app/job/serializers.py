from rest_framework import serializers
from app.job.models import Job


class JobSerializer(serializers.ModelSerializer):

	class Meta:
		model = Job
		fields = ('id','job_name','job_location','owner_name','owner_location','architect','engineer_name','contractor_customer','is_deleted','created_at','updated_at')
		# extra_kwargs = {
		# 	'name': {
		# 		'required':True,
		# 		'error_messages':{
		# 		'required':'Please fill this field',
		# 		}
		# 	},
			
		# 	'company': {
		# 		'required':True,
		# 		'error_messages':{
		# 		'required':'Please provide company id',
		# 		}
		# 	},
		# }		