from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('guidelines/', views.guidelines_view, name='guidelines'),
    path('notices/', views.notices_view, name='notices'),
    path('grievance/', views.complaint_view, name='grievance'),
]