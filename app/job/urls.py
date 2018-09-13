from django.conf.urls import url
from app.job import views
app_name='job'

urlpatterns = [
	url(r'^job/(?P<job_id>[0-9]+)$',views.JobApi.as_view()),
	url(r'^job/$',views.JobApi.as_view()),
	
]
