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
		
		company_data = request.data.get('company_data')
		data = agileCRM("contacts","POST",company_data,"application/json")
		return ApiResponse().success(data ,200)
		

	def get(self,request):
		
			# if(company_id):
			# 	try:
			# 		company_data = agileCRM("contacts/"+company_id,"GET",None,"application/json")
			# 	except Exception as err:
			# 		print(err)	
			# 		return ApiResponse().error("please provide valid company id", 400)
			# else:
		company_data = agileCRM("contacts/companies?page_size=20&global_sort_key=-created_time","GET",None,"application/json")
		return ApiResponse().success(company_data, 200)
		

	def put(self,request):
		update_company_data = request.data.get('update_company_data')
		contact_data = agileCRM("contacts/edit-properties","PUT",update_company_data,"application/json")
		return ApiResponse().success(contact_data, 200)
			

	# def delete(self,request,company_id):
	# 	try:
	# 		Company.objects.filter(pk=company_id).update(is_deleted=True)
	# 		return ApiResponse().success("Successfully Deleted", 200)
	# 	except Exception as err:
	# 		print(err)
	# 		return ApiResponse().error("Please send valid id", 500)
	# 	