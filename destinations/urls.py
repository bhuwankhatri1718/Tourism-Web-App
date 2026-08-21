from django.urls import path
from . import views

urlpatterns = [
    path('', views.destination_list_view, name='destination_list'),
    path('<int:pk>/', views.destination_detail_view, name='destination_detail'),
]