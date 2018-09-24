from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from app.job.serializers import JobSerializer
from app.job.models import Job
from app.lib.response import ApiResponse


class JobApi(APIView):
	
	def post(self,request):
		try:
			job_data = JobSerializer(data=request.data)
			if not(job_data.is_valid()):
				return ApiResponse().error(job_data.errors,400)
			job_data.save()
			return ApiResponse().success(job_data.data,200)
		except Exception as err:
			print(err)
			return ApiResponse().error('Error while assign the job',500)

	def get(self,request,job_id=None):
		try:
			
			if(job_id):
				try:
					get_data = JobSerializer(Job.objects.get(is_deleted=False,id=job_id))
				except Exception as err:
					print(err)	
					return ApiResponse().error('please provide valid job id', 400)
			else:
				job_data = Job.objects.filter(is_deleted=False)
				get_data = JobSerializer(job_data, many=True)
			return ApiResponse().success(get_data.data, 200)
		except Exception as err: 
			print(err) 
			return ApiResponse().error('Job does not exists', 500)

	def put(self,request):
		try:
			job_id = request.data.get('id')
			get_data = Job.objects.get(pk=job_id)
			update_data = JobSerializer(get_data,data=request.data)
			print(update_data)
			if update_data.is_valid():
				update_data.save()
				return ApiResponse().success('Job details updated Successfully', 200)
			else:
				return ApiResponse().error('Error while updating the job details', 400)	
		except:
			return ApiResponse().error('Error', 500)

	def delete(self,request,job_id):
		try:
			Job.objects.filter(pk=job_id).update(is_deleted=True)
			return ApiResponse().success('Successfully Deleted', 200)
		except Exception as err:
			print(err)
			return ApiResponse().error('Please send valid id', 500)
		