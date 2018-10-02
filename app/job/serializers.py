from rest_framework import serializers
from app.job.models import Job


class JobSerializer(serializers.ModelSerializer):

	

	class Meta:
		model = Job
		fields = ('id','job_name','job_location','owner_name','owner_location','architect','engineer_name','contractor_customer','file_upload','is_deleted','created_at','updated_at')
		extra_kwargs = {
			'owner_name': {
				'required':True,
				'error_messages':{
				'required':'Owner name is required',
				}
			},
			'architect': {
				'required':True,
				'error_messages':{
				'required':'Architect field is required',
				}
			},
			'engineer_name': {
				'required':True,
				'error_messages':{
				'required':'Engineer name  is required',
				}
			},
			'contractor_customer': {
				'required':True,
				'error_messages':{
				'required':'contractor_customer field is required',
				}
			},
			'job_location': {
				'required':True,
				'error_messages':{
				'required':'Job location field is required',
				}
			},
			'job_name': {
				'required':True,
				'error_messages':{
				'required':'Job name is required',
				}
			},
			'owner_location': {
				'required':True,
				'error_messages':{
				'required':'Owner location is required',
				}
			},
			
		}		