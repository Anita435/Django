from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path

from . import views

app_name = 'user_api'

router = routers.DefaultRouter()
router.register(r'user', views.UserRetrieveUpdateAPIView)

urlpatterns = [
    url(r'api/', include(router.urls)),
    path('signup/', views.RegistrationAPIView.as_view()),
    url(r'signin/', views.LoginAPIView.as_view()),
    url(r'signout/', views.LogoutAPIView.as_view()),
    url("otp-verify/", views.OTPDetailsView.as_view({"post":'otp_view'}), name="otp_view"),
    url("otp-resend/", views.OTPDetailsView.as_view({"get":'otp_resent_view'}), name="otp_resent_view"),
]


