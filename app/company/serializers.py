from rest_framework import serializers
from app.company.models import Company


class CompanySerializer(serializers.ModelSerializer):

	class Meta:
		model = Company
		fields = ('id','company_id','tags','company_name','is_deleted','created_at','updated_at')
		