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
		try:
			deal_data = DealSerializer(data=request.data)
			if not(deal_data.is_valid()):
				return ApiResponse().error(deal_data.errors,400)
			deal_data.save()
			return ApiResponse().success("deal created successfully",200)
		except Exception as err:
			print(err)
			return ApiResponse().error("Error while assign the deal",500)

	def get(self,request,deal_id=None):
		try:
			if(deal_id):
				try:
					deal_data = agileCRM("opportunity/"+deal_id,"GET",None,"application/json")
				except Exception as err:
					print(err)	
					return ApiResponse().error("please provide valid deal id", 400)
			else:
				deal_data = agileCRM("opportunity/","GET",None,"application/json")
			return ApiResponse().success(deal_data, 200)
		except Exception as err: 
			print(err) 
			return ApiResponse().error("Deal data does not exists", 500)

	def put(self,request):
		try:
			deal_id = request.data.get('id')
			get_data = Deals.objects.get(pk=deal_id)
			update_data = DealSerializer(get_data,data=request.data)
			if update_data.is_valid():
				update_data.save()
				return ApiResponse().success("Deals details updated Successfully", 200)
			else:
				return ApiResponse().error("Error while updating the Deals details", 400)	
		except:
			return ApiResponse().error("Error", 500)

	def delete(self,request,deal_id):
		try:
			Deals.objects.filter(pk=deal_id).update(is_deleted=True)
			return ApiResponse().success("Successfully Deleted", 200)
		except Exception as err:
			print(err)
			return ApiResponse().error("Please send valid id", 500)
		

class DealByJobId(APIView):
	
	def get(self,request,job_id=None):
		try:
			if(job_id):
				try:
					deal_data = Deals.objects.filter(is_deleted=False, custom_id=job_id)
					get_data = DealSerializer(deal_data, many=True)
				except Exception as err:
					print(err)
					return ApiResponse().error("Error while getting the details", 400)
				return ApiResponse().success(get_data.data, 200)
			return ApiResponse().error("Please provide job id", 400)
		except Exception as err: 
			print(err) 
			return ApiResponse().error("Deal matching query does not exist", 500)
