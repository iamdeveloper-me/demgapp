from django.conf.urls import url
from app.company import views
app_name='company'


urlpatterns = [
	url(r'^company/list/$',views.AllCompanyApi.as_view()),
	url(r'^company/$',views.CompanyApi.as_view()),

]