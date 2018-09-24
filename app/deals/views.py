from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from app.deals.serializers import DealSerializer
from app.deals.models import Deals
from app.lib.response import ApiResponse
from scripts.AgileCRM import agileCRM 
import json
from django.http import HttpResponse


class DealApi(APIView):
	
	def post(self,request):
		
		deal_data = request.data.get('deal_data')
		print(deal_data)
		data = agileCRM('opportunity','POST',deal_data,'application/json')
		return ApiResponse().success(data,200)
	
	def get(self,request,deal_id=None):
	
		if(deal_id):
			deal_data = agileCRM('opportunity/'+deal_id,'GET',None,'application/json')
		else:
			deal_data = agileCRM('opportunity?page_size=2','GET',None,'application/json')
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

	# def delete(self,request,deal_id):
	# 	try:
	# 		Deals.objects.filter(pk=deal_id).update(is_deleted=True)
	# 		return ApiResponse().success('Successfully Deleted', 200)
	# 	except Exception as err:
	# 		print(err)
	# 		return ApiResponse().error('Please send valid id', 500)
		

# class DealByJobId(APIView):
	
# 	def get(self,request,job_id=None):
# 		try:
# 			if(job_id):
# 				try:
# 					deal_data = Deals.objects.filter(is_deleted=False, custom_id=job_id)
# 					get_data = DealSerializer(deal_data, many=True)
# 				except Exception as err:
# 					print(err)
# 					return ApiResponse().error('Error while getting the details', 400)
# 				return ApiResponse().success(get_data.data, 200)
# 			return ApiResponse().error('Please provide job id', 400)
# 		except Exception as err: 
# 			print(err) 
# 			return ApiResponse().error('Deal matching query does not exist', 500)
