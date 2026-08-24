from django.shortcuts import render
from destinations.models import Destination
from .models import Guideline, Notice
from .forms import ComplaintForm

from django.contrib.auth.models import User
from destinations.models import Destination
from bookings.models import Booking


def home_view(request):
    destinations = Destination.objects.filter(is_active=True)[:6]
    guidelines = Guideline.objects.filter(is_active=True)[:3]
    notices = Notice.objects.filter(is_active=True).order_by('-published_date')[:3]

    context = {
        'destinations': destinations,
        'guidelines': guidelines,
        'notices': notices,
    }
    return render(request, 'core/home.html', context)


def guidelines_view(request):
    guidelines = Guideline.objects.filter(is_active=True)
    return render(request, 'core/guidelines.html', {'guidelines': guidelines})


def notices_view(request):
    notices = Notice.objects.filter(is_active=True).order_by('-published_date')
    return render(request, 'core/notices.html', {'notices': notices})


def complaint_view(request):
    submitted = False

    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            form.save()
            submitted = True
            form = ComplaintForm()
    else:
        form = ComplaintForm()

    return render(request, 'core/complaint.html', {'form': form, 'submitted': submitted})



def stats_view(request):
    total_destinations = Destination.objects.filter(is_active=True).count()
    total_tourists = User.objects.filter(is_staff=False).count()
    total_bookings = Booking.objects.count()
    confirmed_bookings = Booking.objects.filter(status='CONFIRMED').count()
    pending_bookings = Booking.objects.filter(status='PENDING').count()

    context = {
        'total_destinations': total_destinations,
        'total_tourists': total_tourists,
        'total_bookings': total_bookings,
        'confirmed_bookings': confirmed_bookings,
        'pending_bookings': pending_bookings,
    }
    return render(request, 'core/stats.html', context)