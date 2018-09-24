from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from app.owner.serializers import OwnerSerializer
from app.owner.models import Owner
from app.lib.response import ApiResponse


class OwnerView(APIView):
	
	def post(self,request):
		try:
			owner_data = OwnerSerializer(data=request.data)
			if not(owner_data.is_valid()):
				return ApiResponse().error(owner_data.errors,400)
			owner_data.save()
			return ApiResponse().success('Owner created successfully',200)
		except Exception as err:
			print(err)
			return ApiResponse().error('Error while assign the Owner',500)

	def get(self,request,owner_id=None):
		try:
			if(owner_id):
				try:
					get_data = OwnerSerializer(Owner.objects.get(is_deleted=False, id=owner_id))
				except Exception as err:
					print(err)	
					return ApiResponse().error('please provide valid Owner id', 400)
			else:
				owner_data = Owner.objects.filter(is_deleted=False).order_by('-id')
				ownerData = OwnerSerializer(owner_data, many=True)
				return ApiResponse().success(ownerData.data,200)
		except Exception as err:
			print(err)
			return ApiResponse().error('Error while getting Owner',500)

	def put(self,request,owner_id):
		try:
			get_data = Owner.objects.get(pk=owner_id)
			update_data = OwnerSerializer(get_data,data=request.data)
			if update_data.is_valid():
				update_data.save()
				return ApiResponse().success('Owner details updated Successfully', 200)
			else:
				return ApiResponse().error('Error while updating the Owner details', 400)	
		except:
			return ApiResponse().error('Error', 500)
	
	def delete(self,request,owner_id):
		try:
			Owner.objects.filter(pk=owner_id).update(is_deleted=True)
			return ApiResponse().success('Successfully Deleted', 200)
		except Exception as err:
			print(err)
			return ApiResponse().error('Please send valid id', 500)




	

