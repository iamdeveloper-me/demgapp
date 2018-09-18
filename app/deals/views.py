from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from app.deals.serializers import DealSerializer
from app.deals.models import Deals
from app.lib.response import ApiResponse
from scripts.AgileCRM import agileCRM

class DealApi(APIView):
	
	def post(self,request):
		
		deal_data = request.data.get('deal_data')
		print(deal_data)
		data = agileCRM("opportunity","POST",deal_data,"application/json")
		return ApiResponse().success(data,200)
	
	def get(self,request,deal_id=None):
	
		if(deal_id):
			deal_data = agileCRM("opportunity/"+deal_id,"GET",None,"application/json")
		else:
			deal_data = agileCRM("opportunity?page_size=10&cursor=E-ABAIICNGoRc35hZ2lsZS1jcm0tY2xvdWRyFAsSB0NvbnRhY3QYgICAgKLThAoMogEIcHJhYmF0aGuIAgAU -H","GET",None,"application/json")
		return ApiResponse().success(deal_data, 200)
		

	def put(self,request):
		update_data = request.data.get('update_data')
		contact_data = agileCRM("opportunity/partial-update","PUT",update_data,"application/json")
		return ApiResponse().success(contact_data, 200)

	# def delete(self,request,deal_id):
	# 	try:
	# 		Deals.objects.filter(pk=deal_id).update(is_deleted=True)
	# 		return ApiResponse().success("Successfully Deleted", 200)
	# 	except Exception as err:
	# 		print(err)
	# 		return ApiResponse().error("Please send valid id", 500)
		

# class DealByJobId(APIView):
	
# 	def get(self,request,job_id=None):
# 		try:
# 			if(job_id):
# 				try:
# 					deal_data = Deals.objects.filter(is_deleted=False, custom_id=job_id)
# 					get_data = DealSerializer(deal_data, many=True)
# 				except Exception as err:
# 					print(err)
# 					return ApiResponse().error("Error while getting the details", 400)
# 				return ApiResponse().success(get_data.data, 200)
# 			return ApiResponse().error("Please provide job id", 400)
# 		except Exception as err: 
# 			print(err) 
# 			return ApiResponse().error("Deal matching query does not exist", 500)
