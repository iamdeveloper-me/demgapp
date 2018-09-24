from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from app.lib.response import ApiResponse
from scripts.AgileCRM import agileCRM

class ContactApi(APIView):

	def post(self,request):
		
		contact_data = request.data.get('contact_data')
		data = agileCRM("contacts","POST",contact_data,"application/json")
		return ApiResponse().success(data, 200)

	def get(self,request,contact_id=None):

		if(contact_id):
			contact_data = agileCRM("contacts/"+contact_id,"GET",None,"application/json")
		else:
			# contact_data = agileCRM("contacts?page_size=700&global_sort_key=-created_time","GET",None,"application/json")
			contact_data = agileCRM("search?q=austin_b raut&page_size=900&type='PERSON'", "GET", None,"application/json")
		return ApiResponse().success(contact_data, 200)
		

	def put(self,request):
		
		update_contact_data = request.data.get('update_contact_data')
		contact_data = agileCRM("contacts/edit-properties","PUT",update_contact_data,"application/json")
		return ApiResponse().success(contact_data, 200)
			
		