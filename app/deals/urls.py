from django.conf.urls import url
from app.deals import views
app_name='deals'


urlpatterns = [
	# url(r'^deal/(?P<deal_id>[0-9]+)$',views.DealApi.as_view()),
	url(r'^deal$',views.DealApi.as_view()),

]