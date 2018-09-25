from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from app.company.serializers import CompanySerializer
from app.company.models import Company
from app.lib.response import ApiResponse
from scripts.AgileCRM import agileCRM
import json

class CompanyApi(APIView):

	def post(self,request):
		try:
			company_data = CompanySerializer(data=request.data)
			if not(company_data.is_valid()):
				return ApiResponse().error(company_data.errors,400)
			company_data.save()
			return ApiResponse().success("company created successfully",200)
		except Exception as err:
			print(err)
			return ApiResponse().error("Error while assign the company",500)

	
	
	def get(self,request):
		
			# if(company_id):
			# 	try:
			# 		company_data = agileCRM("contacts/"+company_id,"GET",None,"application/json")
			# 	except Exception as err:
			# 		print(err)	
			# 		return ApiResponse().error("please provide valid company id", 400)
			# else:
		# company_list = agileCRM("contacts/companies?page_size=500&global_sort_key=-created_time","GET",None,"application/json")
		# return ApiResponse().success(company_list, 200)
		# response = {}
		eng_data = Company.objects.filter(is_deleted=False, tags='Engineer')#.values_list('company_name', 'company_id')
		# response['eng_data'] = eng_data
		arc_data = Company.objects.filter(is_deleted=False, tags='Architect')#.values_list('company_name', 'company_id')
		# response['arc_data'] = arc_data
		owner_data = Company.objects.filter(is_deleted=False, tags='Owner' )#.values_list('company_name', 'company_id')
		# response['owner_data'] = owner_data
		contractor_data = Company.objects.filter(is_deleted=False, tags='Contractor' )#.values_list('company_name', 'company_id')
		# response['contractor_data'] = contractor_data

		# print(response)
		# company_data = Company.objects.filter(is_deleted=False)
		# get_data = CompanySerializer(response, many=True)
		# print(get_data.data)
		# company_data = json.loads(json.dumps(get_data.data))
		# print(company_data)
		# return ApiResponse().success(response, 200)

		response = {
			'eng_data': list(eng_data.values()),
			'arc_data': list(arc_data.values()),
			'owner_data': list(owner_data.values()),
			'contractor_data': list(contractor_data.values()),
		}
		print(response)
		return ApiResponse().success(response, 200)

		

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


class CrmCompanyApi(APIView):

	def post(self,request):

		company_data = request.data.get('company_data')
		data = agileCRM("contacts","POST",company_data,"application/json")
		return ApiResponse().success(data ,200)
		


	def get(self,request):
		company_list = agileCRM("contacts/companies?page_size=500&global_sort_key=-created_time","GET",None,"application/json")
		company_data = json.loads(company_list)
		for data in company_data:
			try:
				comp_id = data['id']
				if Company.objects.filter(company_id=comp_id).exists():
					print("Company is already present for id: ", comp_id)
				else:
					if data['tags'] == []:
						Company.objects.create(company_id=comp_id, company_name=data['properties'][0]['value'])
					else:
						Company.objects.create(company_id=comp_id, tags=data['tags'][0], company_name=data['properties'][0]['value'])
			except Exception as err:
				print(err)
				return ApiResponse().error("Something is wrong!!!",500)
		return ApiResponse().success(company_list, 200)
		