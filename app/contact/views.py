from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
# from app.company.serializers import CompanySerializer
# from app.company.models import Company
from app.lib.response import ApiResponse
from scripts.AgileCRM import agileCRM

class ContactApi(APIView):
	def get(self,request,contact_id=None):
		try:
			if(contact_id):
				try:
					contact_data = agileCRM("contacts/"+contact_id,"GET",None,"application/json")
				except Exception as err:
					print(err)	
					return ApiResponse().error("please provide valid company id", 400)
			else:
				# company_data = Company.objects.filter(is_deleted=False)
				# get_data = CompanySerializer(company_data, many=True)
				contact_data = agileCRM("opportunity/","GET",None,"application/json")
			return ApiResponse().success(contact_data, 200)
		except Exception as err: 
			print(err) 
			return ApiResponse().error("Company does not exists", 500)
