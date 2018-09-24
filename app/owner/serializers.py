from rest_framework import serializers
from app.owner.models import Owner

class OwnerSerializer(serializers.ModelSerializer):
	class Meta:
		model =  Owner
		fields = ('id','name','domain','email','password','calendar_url','is_admin','is_account_owner','is_disabled','schedule_id','is_deleted','created_at','updated_at')
		# extra_kwargs = {
		# 	'name': {
		# 		'required':True,
		# 		'error_messages':{
		# 		'required':'Please insert name',
		# 		}
		# 	'ptype': {
		# 		'required':True,
		# 		'error_messages':{
		# 		'required':'Please insert ptype',
		# 		}
		# 	}
		# }