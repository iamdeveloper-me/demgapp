from django.conf.urls import url
from app.properties import views

app_name='properties'

urlpatterns = [
	url(r'^property/$',views.PropertyView.as_view()),
	url(r'^property/(?P<property_id>[0-9]+)$',views.PropertyView.as_view()),
]