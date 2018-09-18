from django.conf.urls import url
from app.contact import views
app_name='contact'

urlpatterns = [
	# url(r'^contact/(?P<contact_id>[0-9]+)$',views.ContactApi.as_view()),
	url(r'^contact/$',views.ContactApi.as_view()),
	
]
