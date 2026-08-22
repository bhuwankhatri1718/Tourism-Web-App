from django.shortcuts import render, get_object_or_404
from .models import Destination
from django.db import models


def destination_list_view(request):
    query = request.GET.get('q', '').strip()
    destinations = Destination.objects.filter(is_active=True)

    if query:
        destinations = destinations.filter(
            models.Q(name__icontains=query) | models.Q(location__icontains=query)
        )

    return render(request, 'destinations/list.html', {'destinations': destinations, 'query': query})


def destination_detail_view(request, pk):
    destination = get_object_or_404(Destination, pk=pk, is_active=True)
    return render(request, 'destinations/detail.html', {'destination': destination})