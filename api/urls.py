from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

from . import views

router = DefaultRouter()
router.register(r'users/(?P<uid>[0-9]+)/records', views.UserRecordViewSet, base_name='user_record')
router.register(r'users', views.UserViewSet, base_name='user')
router.register(r'records', views.RecordViewSet, base_name='record')

urlpatterns = [
	url(r'^login/$', obtain_jwt_token, name='login'),
  url(r'^register/$', views.RegisterView.as_view(), name='register'),
	url(r'^', include(router.urls)),
]
