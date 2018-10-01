from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status


def api_500(request):

	""" 
		:param request: :
		return: Automatically call while system generate 500 Error 
	"""
	response = HttpResponse('{"data":{ "message":"error","responseCode": "500", "error":"Internal server error"} }', content_type="application/json", status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
	return response

class ApiResponse:

	def success(self,response='',code='',token=None):
		
		res = {
			"data":{
				"message":  "Successfully",
				"responseCode": code,
				"result":response,

			}
		}
		if not token is None:
			res['data']['token'] = token
		return Response(res)

	def paginationSuccess(self,response,code,count, unview=None):
		
		res = {
			"recordsTotal":count,
			
			"recordsFiltered": count,
			"data":{
				"message":  "Successfully",
				"responseCode": code,
				"result":response,
				
			}
		}
		if not unview is None:
			res['data']['unviewTotal'] = unview
		return Response(res)

	#@classmethod
	def error(self,response,code):
		return Response({
			"data":{
				"message":  "error",
				"responseCode": code,
				"error":response
			}
		})	