from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:pk>/', views.book_destination_view, name='book_destination'),
    path('success/<int:pk>/', views.booking_success_view, name='booking_success'),
    path('my-bookings/', views.my_bookings_view, name='my_bookings'),
]