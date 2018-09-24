from django.conf.urls import url
from app.owner import views

app_name='owner'

urlpatterns = [
	url(r'^owner/$',views.OwnerView.as_view()),
	url(r'^owner/(?P<property_id>[0-9]+)$',views.OwnerView.as_view()),
]