from django.shortcuts import render, get_object_or_404
from .models import Destination


def destination_list_view(request):
    destinations = Destination.objects.filter(is_active=True)
    return render(request, 'destinations/list.html', {'destinations': destinations})


def destination_detail_view(request, pk):
    destination = get_object_or_404(Destination, pk=pk, is_active=True)
    return render(request, 'destinations/detail.html', {'destination': destination})