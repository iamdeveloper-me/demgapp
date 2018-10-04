from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from app.job.serializers import JobSerializer
from app.job.models import Job
from app.lib.response import ApiResponse
from app.lib.validation import Validation
from scripts.AgileCRM import agileCRM 
from app.company.models import Company
from app.company.serializers import CompanySerializer
import json
import requests

class JobApi(APIView):
	
	def post(self,request):
		try:
			company_name = request.data.get('owner_name')
			is_exists = Company.objects.filter(company_name=company_name).exists()
			if is_exists:
				jobdata = self.validate(request)
				if jobdata is not True:
					return jobdata
				job_data = JobSerializer(data=request.data)
				if not(job_data.is_valid()):
					return ApiResponse().error(job_data.errors,400)
				job_data.save()
				return ApiResponse().success(job_data.data,200)
			else:
				return ApiResponse().error('Owner name does not exists',400)
		except Exception as err:
			print(err)
			return ApiResponse().error('Error while assign the job',500)

	def get(self,request,job_id=None):
		# company_list = agileCRM("contacts/companies?page_size=500&global_sort_key=-created_time","GET",None,"application/json")
		# company_data = json.loads(company_list)
		# for data in company_data:
		# 	comp_id = data['id']
		# 	if Company.objects.filter(company_id=comp_id).exists():
		# 		print("Company is already present for id: ", comp_id)
		# 	else:
		# 		if data['tags'] == []:
		# 			Company.objects.create(company_id=comp_id, company_name=data['properties'][0]['value'])
		# 		else:
		# 			Company.objects.create(company_id=comp_id, tags=data['tags'][0], company_name=data['properties'][0]['value'])

		try:
			if(job_id):
				print(job_id)
				try:
					data=Job.objects.get(is_deleted=False,id=job_id)
					get_data = JobSerializer(data)
				except Exception as err:
					print(err)	
					return ApiResponse().error('please provide valid job id', 400)
			else:
				job_data = Job.objects.filter(is_deleted=False)
				get_data = JobSerializer(job_data, many=True)
			# aa=get_data.data
			return ApiResponse().success(get_data.data, 200)
		except Exception as err: 
			print(err) 
			return ApiResponse().error('Job does not exists', 500)

	def put(self,request,job_id):
		try:
			# job_id = request.data.get('id')
			company_name = request.data.get('owner_name')
			is_exists = Company.objects.filter(company_name=company_name).exists()
			if is_exists:
				get_data = Job.objects.get(pk=job_id)
				update_data = JobSerializer(get_data,data=request.data)
				# print(update_data)
				if update_data.is_valid():
					update_data.save()
					return ApiResponse().success(update_data.data, 200)
				else:
					return ApiResponse().error(update_data.errors,400)
			else:
				return ApiResponse().error('Owner name does not exists',400)	
		except:
			return ApiResponse().error('Error', 500)

	def delete(self,request,job_id):
		try:
			Job.objects.filter(pk=job_id).update(is_deleted=True)
			return ApiResponse().success('Successfully Deleted', 200)
		except Exception as err:
			print(err)
			return ApiResponse().error('Please send valid id', 500)


	def validate(self, request):
		architect = Validation().null(request.data.get('architect'))
		engineer = Validation().null(request.data.get('engineer_name'))
		contractor = Validation().null(request.data.get('contractor_customer'))
		
		if(contractor is False) and (architect is False) and (engineer is False):
			data = {"contractor":"Contractor field is required",
					"architect":"Architect field is required",
					"engineer":"Engineer field is required"}
			return ApiResponse().error(data, 400)
		if(contractor is False) and (engineer is False):
			data = {"contractor":"Contractor field is required",
					"engineer":"Engineer field is required"}
			return ApiResponse().error(data, 400)
		if(contractor is False) and (architect is False):
			data = {"contractor":"Contractor field is required",
					"architect":"Architect field is required"}
			return ApiResponse().error(data, 400)
		if(engineer is False) and (architect is False):
			data = {"engineer":"Engineer field is required",
					"architect":"Architect field is required"}
			return ApiResponse().error(data, 400)
		if engineer is False: 
			return ApiResponse().error("Engineer field is required", 400)
		if contractor is False:
			return ApiResponse().error("Contractor field is required", 400)
		if architect is False:
			return ApiResponse().error("Architect field is required", 400)
		return True	


class CrmJobApi(APIView):

	def post(self,request):

		deal_data = request.data.get('deal_data')
		data = agileCRM('opportunity','POST',deal_data,'application/json')
		return ApiResponse().success(data,200)
	
	def get(self,request,deal_id=None):
	
		if(deal_id):
			deal_data = agileCRM('opportunity/'+deal_id,'GET',None,'application/json')
		else:
			deal_data = agileCRM('opportunity?page_size=1','GET',None,'application/json')
			deal_data = json.loads(deal_data)
			for data in deal_data:
				for (key, val) in data.items():
					# print(key,val)
					if key == 'owner':
						owner = val
						print(owner)
						# Owner
						# for k,v in owner.items():
						# 	print("*****")
							
					# if key == 'tagsWithTime':
					# 	tag = val
					# 	for tag_dic in tag:
					# 		for tkey,tval in tag_dic.items():
					# 			print("**")
					# if key == 'contacts':
					# 	contact = val
					# 	for con_dic in contact:
					# 		for ckey,cval in con_dic.items():
					# 			# print(ckey,cval)
					# 			print("***")
					# 			if ckey == 'properties':
					# 				properties = cval

					# 				for prop_dic in properties:
					# 					for pkey,pval in prop_dic.items():
					# 						# print(pkey,pval)
					# 						print("#####")
					# if key == 'custom_data':
					# 	custom = val
					# 	for cus_dict in custom:
					# 		for ckey,cval in cus_dict.items():
					# 			print(ckey,cval)
					# if key == 'contact_ids':
					# 	contact = val
						# print(contact)
						# for cdata in contact:
							# print(cdata)
							# print("^^^^^^^")
					# if key == 'notes':
					# 	note = val
					# 	for ndata in note:
					# 		print(ndata)
					# if key == 'products':
					# 	product = val
					# 	for pdata in product:
					# 		print(pdata)
					# if key == 'note_ids':
					# 	note_id = val
					# 	for not_data in note_id:
					# 		print(not_data)
					# if key == 'tags':
					# 	tags = val
					# 	for tdata in tags:
					# 		print(tdata)

							# print(k)
							# print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
					# for li in key:
					# 	print(li)

		return ApiResponse().success(deal_data,200) 
			
	def put(self,request):
		update_data = request.data.get('update_data')
		contact_data = agileCRM('opportunity/partial-update','PUT',update_data,'application/json')
		return ApiResponse().success(contact_data, 200)
