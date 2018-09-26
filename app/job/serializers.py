from rest_framework import serializers
from app.job.models import Job


class JobSerializer(serializers.ModelSerializer):

	class Meta:
		model = Job
		fields = ('id','job_name','job_location','post_local_id','owner_name','owner_location','architect','engineer_name','contractor_customer','is_deleted','created_at','updated_at')
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
				'required':'This field is required',
				}
			},
			'engineer_name': {
				'required':True,
				'error_messages':{
				'required':'This field  is required',
				}
			},
			'contractor_customer': {
				'required':True,
				'error_messages':{
				'required':'This field is required',
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