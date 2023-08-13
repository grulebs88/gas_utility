from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('service_request/', views.service_request, name='service_request'),
    path('request_tracking/', views.request_tracking, name='request_tracking'),
    path('manage_requests/', views.manage_requests, name='manage_requests'),
]