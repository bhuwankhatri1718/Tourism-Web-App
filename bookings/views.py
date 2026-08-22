from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone

from destinations.models import Destination
from .models import Booking
from .forms import BookingForm
from .esewa import generate_signature, decode_response, ESEWA_MERCHANT_CODE, ESEWA_FORM_URL


@login_required
def book_destination_view(request, pk):
    destination = get_object_or_404(Destination, pk=pk, is_active=True)

    if request.method == 'POST':
        form = BookingForm(request.POST, destination=destination)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.tourist = request.user
            booking.destination = destination

            if booking.hotel:
                # Advance payment = 10% of one night's rate
                booking.advance_amount = round(booking.hotel.price_per_night * Decimal('0.10'), 2)

            booking.save()

            if booking.advance_amount > 0:
                return redirect('payment_initiate', pk=booking.id)
            return redirect('booking_success', pk=booking.id)
    else:
        form = BookingForm(destination=destination)

    return render(request, 'bookings/book.html', {'form': form, 'destination': destination})


@login_required
def booking_success_view(request, pk):
    booking = get_object_or_404(Booking, pk=pk, tourist=request.user)
    return render(request, 'bookings/success.html', {'booking': booking})


@login_required
def my_bookings_view(request):
    bookings = Booking.objects.filter(tourist=request.user).order_by('-created_at')
    Booking.objects.filter(tourist=request.user, is_seen_by_tourist=False).update(is_seen_by_tourist=True)
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})


@login_required
def cancel_booking_view(request, pk):
    booking = get_object_or_404(Booking, pk=pk, tourist=request.user)
    if booking.status == 'PENDING' and request.method == 'POST':
        booking.status = 'REJECTED'
        booking.save()
    return redirect('my_bookings')


@login_required
def payment_initiate_view(request, pk):
    booking = get_object_or_404(Booking, pk=pk, tourist=request.user)

    if booking.payment_status == 'PAID' or booking.advance_amount <= 0:
        return redirect('booking_success', pk=booking.id)

    transaction_uuid = f"booking{booking.id}-{int(timezone.now().timestamp())}"
    amount = booking.advance_amount

    signature = generate_signature(amount, transaction_uuid)

    context = {
        'booking': booking,
        'amount': amount,
        'total_amount': amount,
        'transaction_uuid': transaction_uuid,
        'product_code': ESEWA_MERCHANT_CODE,
        'signature': signature,
        'success_url': request.build_absolute_uri(reverse('payment_success')),
        'failure_url': request.build_absolute_uri(reverse('payment_failure')),
        'esewa_form_url': ESEWA_FORM_URL,
    }
    return render(request, 'bookings/payment_initiate.html', context)


@login_required
def payment_success_view(request):
    data_param = request.GET.get('data')
    if not data_param:
        return redirect('my_bookings')

    try:
        decoded = decode_response(data_param)
        transaction_uuid = decoded.get('transaction_uuid', '')
        status = decoded.get('status')
        booking_id = int(transaction_uuid.replace('booking', '').split('-')[0])
        booking = Booking.objects.get(pk=booking_id, tourist=request.user)
    except (IndexError, ValueError, Booking.DoesNotExist):
        return redirect('my_bookings')

    if status == 'COMPLETE':
        booking.payment_status = 'PAID'
        booking.payment_transaction_id = decoded.get('transaction_code', '')
        booking.save()
        return redirect('booking_success', pk=booking.id)

    return redirect('payment_failure')


@login_required
def payment_failure_view(request):
    return render(request, 'bookings/payment_failed.html')