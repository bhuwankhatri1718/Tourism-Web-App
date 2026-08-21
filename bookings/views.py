from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from destinations.models import Destination
from .models import Booking
from .forms import BookingForm


@login_required
def book_destination_view(request, pk):
    destination = get_object_or_404(Destination, pk=pk, is_active=True)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.tourist = request.user
            booking.destination = destination
            booking.save()
            return redirect('booking_success', pk=booking.id)
    else:
        form = BookingForm()

    return render(request, 'bookings/book.html', {'form': form, 'destination': destination})


@login_required
def booking_success_view(request, pk):
    booking = get_object_or_404(Booking, pk=pk, tourist=request.user)
    return render(request, 'bookings/success.html', {'booking': booking})


@login_required
def my_bookings_view(request):
    bookings = Booking.objects.filter(tourist=request.user).order_by('-created_at')
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})