from rest_framework import serializers
from app.company.models import Company


class CompanySerializer(serializers.ModelSerializer):

	class Meta:
		model = Company
		fields = ('id','name','tag','is_deleted','created_at','updated_at')
		