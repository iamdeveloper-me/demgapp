from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from app.lib.response import ApiResponse
from scripts.AgileCRM import agileCRM
from app.contact.serializers import ContactSerializer

class ContactApi(APIView):

	def post(self,request):
		try:
			contact_data = ContactSerializer(data=request.data)
			if not(contact_data.is_valid()):
				return ApiResponse().error(contact_data.errors,400)
			contact_data.save()
			return ApiResponse().success(contact_data.data,200)
		except Exception as err:
			return ApiResponse().error("Error while create contact",500)

	def get(self,request,contact_id=None):
		try:
			if(contact_id):
				try:
					get_data = ContactSerializer(Contact.objects.get(is_deleted=False,id=contact_id))
				except Exception as err:
					print(err)	
					return ApiResponse().error("please provide valid contact id", 400)
			else:
				contact_data = Contact.objects.filter(is_deleted=False)
				get_data = ContactSerializer(contact_data, many=True)
			return ApiResponse().success(get_data.data, 200)
		except Exception as err: 
			print(err) 
			return ApiResponse().error("Contact does not exists", 500)
			
class CrmContactApi(APIView):

	def post(self,request):
		
		contact_data = request.data.get('contact_data')
		data = agileCRM("contacts","POST",contact_data,"application/json")
		return ApiResponse().success(data, 200)

	def get(self,request,contact_id=None):

		if(contact_id):
			contact_data = agileCRM("contacts/"+contact_id,"GET",None,"application/json")
		else:
			contact_data = agileCRM("contacts?page_size=700&global_sort_key=-created_time","GET",None,"application/json")
			# contact_data = agileCRM("search?q=austin_b raut&page_size=900&type='PERSON'", "GET", None,"application/json")
		return ApiResponse().success(contact_data, 200)
		

	def put(self,request):
		
		update_contact_data = request.data.get('update_contact_data')
		contact_data = agileCRM("contacts/edit-properties","PUT",update_contact_data,"application/json")
		return ApiResponse().success(contact_data, 200)