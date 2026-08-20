from django.shortcuts import render
from destinations.models import Destination
from .models import Guideline, Notice


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