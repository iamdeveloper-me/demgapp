from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.views.generic.edit import UpdateView
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.validators import URLValidator


class Validation:
	def null(self, field):
		try:
			if field != '':
				return True
			return False
		except Exception as err:
			print(err)
			return False

	def requestNull(self, request):
		try:
			if request.data is None:
				return False
			return True
		except Exception as err:
			print(err)
			return True

	def email(self, email):
		try:
		    validate_email(email)
		except ValidationError as e:
		    return False
		else:
		    return True

	def url(self, url):
		urlV = URLValidator()
		try:
			urlV(url)
			return True
		except:
			return False

