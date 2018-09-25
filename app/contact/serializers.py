from rest_framework import serializers
from app.contact.models import Contact



class ContactSerializer(serializers.ModelSerializer):
	class Meta:
		model = Contact
		fields = ('id','name','location','is_deleted','created_at','updated_at')