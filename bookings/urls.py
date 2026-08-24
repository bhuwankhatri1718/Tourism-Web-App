from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:pk>/', views.book_destination_view, name='book_destination'),
    path('success/<int:pk>/', views.booking_success_view, name='booking_success'),
    path('my-bookings/', views.my_bookings_view, name='my_bookings'),
    path('cancel/<int:pk>/', views.cancel_booking_view, name='cancel_booking'),
    path('payment/initiate/<int:pk>/', views.payment_initiate_view, name='payment_initiate'),
    path('payment/success/', views.payment_success_view, name='payment_success'),
    path('payment/failure/', views.payment_failure_view, name='payment_failure'),
    path('pdf/<int:pk>/', views.booking_pdf_view, name='booking_pdf'),
]