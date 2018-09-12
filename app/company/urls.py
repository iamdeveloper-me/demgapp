from django.conf.urls import url
from app.company import views
app_name='company'


urlpatterns = [
	# url(r'^company/(?P<company_id>[0-9]+)$',views.CompanyApi.as_view()),
	url(r'^company$',views.CompanyApi.as_view()),

]