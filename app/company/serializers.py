from rest_framework import serializers
from app.company.models import Company


class CompanySerializer(serializers.ModelSerializer):

	class Meta:
		model = Company
		fields = ('id','company_id','tags','company_name','is_deleted','created_at','updated_at')
		extra_kwargs = {
			
			'company_name': {
				'required':True,
				'error_messages':{
				'required':"Company name is required"
				}
			},
			'tags': {
				'required':True,
				'error_messages':{
				'required':"tags is required"
				}
			},
			
		}
		