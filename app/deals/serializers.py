from rest_framework import serializers
from app.deals.models import Deals


class DealSerializer(serializers.ModelSerializer):

	class Meta:
		model = Deals
		fields = ('id','custom','name','tags','related_to','is_deleted','created_at','updated_at')
		