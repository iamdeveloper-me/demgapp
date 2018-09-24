from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from app.properties.serializers import PropertySerializer
from app.properties.models import Property
from app.lib.response import ApiResponse


class PropertyView(APIView):
	
	def post(self,request):
		try:
			property_data = PropertySerializer(data=request.data)
			if not(property_data.is_valid()):
				return ApiResponse().error(property_data.errors,400)
			property_data.save()
			return ApiResponse().success('Property created successfully',200)
		except Exception as err:
			print(err)
			return ApiResponse().error('Error while assign the property',500)

	def get(self,request,property_id=None):
		try:
			if(property_id):
				try:
					get_data = PropertySerializer(Property.objects.get(is_deleted=False, id=property_id))
				except Exception as err:
					print(err)	
					return ApiResponse().error('please provide valid property id', 400)
			else:
				property_data = Property.objects.filter(is_deleted=False).order_by('-id')
				propertyData = PropertySerializer(property_data, many=True)
				return ApiResponse().success(propertyData.data,200)
		except Exception as err:
			print(err)
			return ApiResponse().error('Error while getting property',500)

	def put(self,request,property_id):
		try:
			get_data = Property.objects.get(pk=property_id)
			update_data = PropertySerializer(get_data,data=request.data)
			if update_data.is_valid():
				update_data.save()
				return ApiResponse().success('Property details updated Successfully', 200)
			else:
				return ApiResponse().error('Error while updating the property details', 400)	
		except:
			return ApiResponse().error('Error', 500)

	
	def delete(self,request,property_id):
		try:
			Property.objects.filter(pk=property_id).update(is_deleted=True)
			return ApiResponse().success('Successfully Deleted', 200)
		except Exception as err:
			print(err)
			return ApiResponse().error('Please send valid id', 500)




	

