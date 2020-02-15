from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from core.decorators import  agreed_terms_required
from core.models import SitterServices, MiiSitter
from core.models import ServiceBooking, ServiceLocation, ServiceReviews
from core.methods import create_signature
from .forms import ReviewService

def add_review(request, booking_id):

    booking = ServiceBooking.objects.get(id=booking_id)

    if request.method == 'POST':
        form = ReviewService(request.POST, booking = booking, service=booking.service)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            return redirect('core-home')
    else:
        form = ReviewService(booking = booking, service=booking.service)

    context = {
        'form':form,
        "service":booking.service,
    }

    return render(request, 'reviews/add_review.html', context)
