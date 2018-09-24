from rest_framework import serializers
from app.properties.models import Property

class PropertySerializer(serializers.ModelSerializer):
	class Meta:
		model =  Property
		fields = ('id','name','ptype','value','subtype','is_deleted','created_at','updated_at')
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