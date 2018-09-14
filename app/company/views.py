from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from app.company.serializers import CompanySerializer
from app.company.models import Company
from app.lib.response import ApiResponse
from scripts.AgileCRM import agileCRM

class CompanyApi(APIView):
	
	def post(self,request):
		try:
			company_data = CompanySerializer(data=request.data)
			if not(company_data.is_valid()):
				return ApiResponse().error(company_data.errors,400)
			company_data.save()
			# agileCRM("contacts","POST",company_data,"application/json")
			return ApiResponse().success("company created successfully",200)
		except Exception as err:
			print(err)
			return ApiResponse().error("Error while assign the company",500)

	def get(self,request,company_id=None):
		try:
			if(company_id):
				try:
					company_data = agileCRM("contacts/"+company_id,"GET",None,"application/json")
				except Exception as err:
					print(err)	
					return ApiResponse().error("please provide valid company id", 400)
				# data = agileCRM("contacts/4767592208138240","GET",None,"application/json")
			else:
				# company_data = Company.objects.filter(is_deleted=False)
				# get_data = CompanySerializer(company_data, many=True)
				company_data = agileCRM("contacts","GET",None,"application/json")
			return ApiResponse().success(company_data, 200)
		except Exception as err: 
			print(err) 
			return ApiResponse().error("Company does not exists", 500)

	def put(self,request):
		try:
			company_id = request.data.get('id')
			get_data = Company.objects.get(pk=company_id)
			update_data = CompanySerializer(get_data,data=request.data)
			if update_data.is_valid():
				update_data.save()
				return ApiResponse().success("Company details updated Successfully", 200)
			else:
				return ApiResponse().error("Error while updating the Company details", 400)	
		except:
			return ApiResponse().error("Error", 500)

	def delete(self,request,company_id):
		try:
			Company.objects.filter(pk=company_id).update(is_deleted=True)
			return ApiResponse().success("Successfully Deleted", 200)
		except Exception as err:
			print(err)
			return ApiResponse().error("Please send valid id", 500)
		