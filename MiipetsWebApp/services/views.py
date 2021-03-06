from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from core.decorators import miiowner_required, agreed_terms_required
from core.models import User, Pets, SitterServices, ServicePhotos, MiiSitter
from core.models import ServiceBooking, ServiceLocation, ServiceReviews
from django.views.generic import ListView
from django.db.models import Q, Sum
from core.methods import sort_out_dates, filter_on_location, return_day_of_week_from_date, generate_review_html_start
from core.methods import  get_options_of_timeslots_walk_sit, get_options_of_timeslots_board_daycare
from .forms import BookService
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core import mail
from django.conf import settings
from datetime import datetime, timedelta, timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def view_all_services(request):
    """
    This view allows everyone to view all current services
    """
    try:
        if request.user.is_sitter:
            context = {
                "title": "All Services",
                "sitter_user":True
                }
        else:
            context = {
                "title": "All Services",
                "sitter_user":False
                }
    except:
        context = {
            "title": "All Services",
            "sitter_user":False
            }

    return render(request, 'services/all-services.html', context)


def view_services(request, type):
    """
    This view allows everyone to view all current Services
    """

    # get all services with type requested
    type_dictionary = {"Walker":"WALK",
                       'Boarding' :'BOARD',
                       'Sitter' :'SIT',
                       'Daycare' :'DAYCARE'}

    if request.method=="GET":
        #check if type correct for filtering
        try:
            if request.GET['service_type_input'] in type_dictionary.keys():
                type = [type_dictionary[request.GET['service_type_input']]]
            else:
                type = list(type_dictionary.values())
        except:
            try:
                type = [type_dictionary[type]]
            except:
                type = [type]

        #check if dates are correct
        try:
            start_date, end_date = sort_out_dates(request.GET['date_begin_input'],
                                                  request.GET['date_end_input'])
        except:
            start_date, end_date = sort_out_dates('', '')


        try:
            price_start = request.GET['price_start']
            if price_start == "":
                price_start = 0
        except:
            price_start = 0

        try:
            price_end = request.GET['price_end']
            if price_end == "":
                price_end = 500
        except:
            price_end = 500

        price_start = int(price_start)
        price_end = int(price_end)

        if  price_start> price_end:
            price_start, price_end = price_end, price_start


        # checking for pet type
        try:
            pet_type = request.GET['pet_type']
        except:
            pet_type = "All Pets"

        try:
            review_score = request.GET['review_score']
            if review_score == "Review score":
                review_score = -1
            else:
                review_score = int(review_score[0])

        except:
            review_score = -1

        #get relevant services not based on location
        if pet_type == "All Pets":
            services = SitterServices.objects.filter(Q(type__in=type)&
                                                     Q(allowed_to_show=True)&
                                                     Q(date_start__lte=start_date)&
                                                     Q(date_end__gte=end_date)&
                                                     Q(price__range=[price_start, price_end])&
                                                     Q(review_score__gte=review_score))

        elif pet_type == "Dog":
            services = SitterServices.objects.filter(Q(type__in=type)&
                                                     Q(allowed_to_show=True)&
                                                     Q(date_start__lte=start_date)&
                                                     Q(date_end__gte=end_date)&
                                                     Q(price__range=[price_start, price_end])&
                                                     Q(dogs_allowed=True)&
                                                     Q(review_score__gte=review_score))
        elif pet_type == "Cat":
            services = SitterServices.objects.filter(Q(type__in=type)&
                                                     Q(allowed_to_show=True)&
                                                     Q(date_start__lte=start_date)&
                                                     Q(date_end__gte=end_date)&
                                                     Q(price__range=[price_start, price_end])&
                                                     Q(cats_allowed=True)&
                                                     Q(review_score__gte=review_score))
        elif pet_type == "Bird":
            services = SitterServices.objects.filter(Q(type__in=type)&
                                                     Q(allowed_to_show=True)&
                                                     Q(date_start__lte=start_date)&
                                                     Q(date_end__gte=end_date)&
                                                     Q(price__range=[price_start, price_end])&
                                                     Q(birds_allowed=True)&
                                                     Q(review_score__gte=review_score))
        elif pet_type == "Reptile":
            services = SitterServices.objects.filter(Q(type__in=type)&
                                                     Q(allowed_to_show=True)&
                                                     Q(date_start__lte=start_date)&
                                                     Q(date_end__gte=end_date)&
                                                     Q(price__range=[price_start, price_end])&
                                                     Q(reptiles_allowed=True)&
                                                     Q(review_score__gte=review_score))
        elif pet_type == "Other":
            services = SitterServices.objects.filter(Q(type__in=type)&
                                                     Q(allowed_to_show=True)&
                                                     Q(date_start__lte=start_date)&
                                                     Q(date_end__gte=end_date)&
                                                     Q(price__range=[price_start, price_end])&
                                                     Q(other_pets_allowed=True)&
                                                     Q(review_score__gte=review_score))


        if len(services) < 1:
            services = SitterServices.objects.filter(Q(allowed_to_show=True))

        #filter on location
        try:
            location_input = request.GET['location_input']
            services,locations = filter_on_location(services, location_input)
            reviews = [generate_review_html_start(service.review_score) for service in services]
            number_of_reviews = [service.number_of_reviews for service in services]
        except:
            location_input = "Location"
            ids = [service.id for service in services]
            locations = ServiceLocation.objects.filter(id__in=ids)
            reviews = [generate_review_html_start(service.review_score) for service in services]
            number_of_reviews = [service.number_of_reviews for service in services]

        # if not location_input:
        #     location_input = "Location"

        services = zip(services, locations, reviews, number_of_reviews)
        try:
            if request.user.is_sitter:
                context = {
                    "title": "View pet services",
                    "type":"Services",
                    "sitter_user":True,
                    "services":services,
                    "location_input":location_input,
                    "google_api":str(settings.GOOGLE_API_KEY),

                    }
            else:
                context = {
                    "title": "View pet services",
                    "type":"Services",
                    "sitter_user":False,
                    "services":services,
                    "location_input":location_input,
                    "google_api":str(settings.GOOGLE_API_KEY),
                    }
        except:
            context = {
                "title": "View pet services",
                "type":"Services",
                "sitter_user":False,
                "services":services,
                "location_input":location_input,
                "google_api":str(settings.GOOGLE_API_KEY),
                }


    return render(request, 'services/single-type-services.html', context)


def view_single_service(request, service_id):

        # get all services with type requested
    type_dictionary = {"WALK":"Walking Service",
                       'BOARD':"Boarding Service",
                       'SIT' :'Sitting Service',
                       'DAYCARE' :'Daycare Service'}

    service = SitterServices.objects.get(id=service_id)
    reviews = ServiceReviews.objects.filter(service=service)
    reviews_paginator = Paginator(reviews, 5)

    # check if service should be updated (only every 5 hours)
    now = datetime.now(timezone.utc)
    difference = now - service.updated_at
    total_hours = difference.days*24
    try:
        if total_hours>5:
             number_of_reviews = ServiceReviews.objects.filter(service=service).count()
             service.number_of_reviews = number_of_reviews
             service.review_score = ServiceReviews.objects.filter(service=service).aggregate(Sum('review_score'))['review_score__sum']/number_of_reviews
             service.save(update_fields=["number_of_reviews", "review_score"])
    except:
        print("couldnt update")


    # check if sitter should be updated (only every 5 hours)
    now = datetime.now(timezone.utc)
    difference = now - service.sitter.updated_at
    total_hours = difference.days*24
    try:
        if total_hours>5:
             sitter = MiiSitter.objects.get(user=service.sitter)
             number_of_services = SitterServices.objects.filter(sitter=service.sitter).count()
             sitter_review_score = SitterServices.objects.filter(sitter=service.sitter).aggregate(Sum('review_score'))['review_score__sum']/number_of_services
             number_of_bookings = ServiceBooking.objects.filter(service=service).count()

             sitter.review_score = sitter_review_score
             sitter.number_of_bookings = number_of_bookings
             sitter.save(update_fields=["review_score", "number_of_bookings"])
    except:
        print("couldnt update sitter")

    similar_services = SitterServices.objects.filter(
                          Q(type=service.type) &
                          Q(allowed_to_show=True)&
                          (Q(price__lte=service.price*1.2) &  Q(price__gte=service.price*0.8)) &
                          ~Q(id = service.id))

    photos = ServicePhotos.objects.filter(service=service)
    location = ServiceLocation.objects.get(service=service)
    sitter = User.objects.get(id=service.sitter.id)
    miisitter = MiiSitter.objects.get(user=sitter)


    time_converter = {'9999':"Not availibe",
                      '1':"01:00",
                      '2':"02:00",
                      "3":"03:00",
                      "4":"04:00",
                      "5":"05:00",
                      "7":"06:00",
                      "6":"07:00",
                      "8":"08:00",
                      "9":"09:00",
                      "10":"10:00",
                      "11":"11:00",
                      "12":"12:00",
                      "13":"13:00",
                      "14":"14:00",
                      "15":"15:00",
                      "16":"16:00",
                      "17":"17:00",
                      "18":"18:00",
                      "19":"19:00",
                      "20":"20:00",
                      "21":"21:00",
                      "22":"22:00",
                      "23":"23:00",
                      "0":"00:00"}

    if request.method == 'POST':
        form = BookService(request.POST, user = request.user, service = service)
        if form.is_valid():
            booking = form.save()
            return redirect('services-booking-confirmation', service_id = service.id, booking_id = booking.id)
    else:
        form = BookService(user = request.user, service = service)


    page = request.GET.get('page', 1)
    try:
        reviews = reviews_paginator.page(page)
    except PageNotAnInteger:
        reviews = reviews_paginator.page(1)
    except EmptyPage:
        reviews = reviews_paginator.page(paginator.num_pages)

    try:
        if request.user.is_sitter:
            context = {
                "title": "Single pet service",
                "sitter":sitter,
                "miisitter":miisitter,
                "reviews":reviews,
                "similar_services":similar_services,
                "sitter_user":True,
                "review_html":generate_review_html_start(service.review_score),
                'type':type_dictionary[service.type],
                "service_name":service.service_name,
                "service_description":service.description,
                'price':service.price,
                'photos':photos,
                'service':service,
                'location':location.city+", "+location.province,
                'monday_start_time':time_converter[str(service.time_start_monday)],
                'tuesday_start_time':time_converter[str(service.time_start_tuesday)],
                'wednesday_start_time':time_converter[str(service.time_start_wednesday)],
                'thursday_start_time':time_converter[str(service.time_start_thursday)],
                'friday_start_time':time_converter[str(service.time_start_friday)],
                'saturday_start_time':time_converter[str(service.time_start_saturday)],
                'sunday_start_time':time_converter[str(service.time_start_sunday)],
                'monday_end_time':time_converter[str(service.time_end_monday)],
                'tuesday_end_time':time_converter[str(service.time_end_tuesday)],
                'wednesday_end_time':time_converter[str(service.time_end_wednesday)],
                'thursday_end_time':time_converter[str(service.time_end_thursday)],
                'friday_end_time':time_converter[str(service.time_end_friday)],
                'saturday_end_time':time_converter[str(service.time_end_saturday)],
                'sunday_end_time':time_converter[str(service.time_end_sunday)],
                'form':form
                }
        else:
            context = {
                "title": "Single pet service",
                "sitter":sitter,
                "similar_services":similar_services,
                "miisitter":miisitter,
                "reviews":reviews,
                "sitter_user":False,
                'type':type_dictionary[service.type],
                "review_html":generate_review_html_start(service.review_score),
                "service_name":service.service_name,
                "service_description":service.description,
                'price':service.price,
                'photos':photos,
                'service':service,
                'location':location.city+", "+location.province,
                'monday_start_time':time_converter[str(service.time_start_monday)],
                'tuesday_start_time':time_converter[str(service.time_start_tuesday)],
                'wednesday_start_time':time_converter[str(service.time_start_wednesday)],
                'thursday_start_time':time_converter[str(service.time_start_thursday)],
                'friday_start_time':time_converter[str(service.time_start_friday)],
                'saturday_start_time':time_converter[str(service.time_start_saturday)],
                'sunday_start_time':time_converter[str(service.time_start_sunday)],
                'monday_end_time':time_converter[str(service.time_end_monday)],
                'tuesday_end_time':time_converter[str(service.time_end_tuesday)],
                'wednesday_end_time':time_converter[str(service.time_end_wednesday)],
                'thursday_end_time':time_converter[str(service.time_end_thursday)],
                'friday_end_time':time_converter[str(service.time_end_friday)],
                'saturday_end_time':time_converter[str(service.time_end_saturday)],
                'sunday_end_time':time_converter[str(service.time_end_sunday)],
                'form':form
                }
    except:
        context = {
                "title": "Single pet service",
                "sitter":sitter,
                "similar_services":similar_services,
                "miisitter":miisitter,
                "reviews":reviews,
                "sitter_user":False,
                'type':type_dictionary[service.type],
                "review_html":generate_review_html_start(service.review_score),
                "service_name":service.service_name,
                "service_description":service.description,
                'price':service.price,
                'photos':photos,
                'service':service,
                'location':location.city+", "+location.province,
                'monday_start_time':time_converter[str(service.time_start_monday)],
                'tuesday_start_time':time_converter[str(service.time_start_tuesday)],
                'wednesday_start_time':time_converter[str(service.time_start_wednesday)],
                'thursday_start_time':time_converter[str(service.time_start_thursday)],
                'friday_start_time':time_converter[str(service.time_start_friday)],
                'saturday_start_time':time_converter[str(service.time_start_saturday)],
                'sunday_start_time':time_converter[str(service.time_start_sunday)],
                'monday_end_time':time_converter[str(service.time_end_monday)],
                'tuesday_end_time':time_converter[str(service.time_end_tuesday)],
                'wednesday_end_time':time_converter[str(service.time_end_wednesday)],
                'thursday_end_time':time_converter[str(service.time_end_thursday)],
                'friday_end_time':time_converter[str(service.time_end_friday)],
                'saturday_end_time':time_converter[str(service.time_end_saturday)],
                'sunday_end_time':time_converter[str(service.time_end_sunday)],
                'form':form
            }

    return render(request, 'services/single-service.html', context)


def load_timeslots(request, service_id):
    date = request.GET.get('date')
    service = SitterServices.objects.get(id=service_id)
    day_of_week = return_day_of_week_from_date(date)

    if day_of_week == "Monday":
        time_start = service.time_start_monday
        time_end = service.time_end_monday
    elif day_of_week == "Tuesday":
        time_start = service.time_start_tuesday
        time_end = service.time_end_tuesday
    elif day_of_week == "Wednesday":
        time_start = service.time_start_wednesday
        time_end = service.time_end_wednesday
    elif day_of_week == "Thursday":
        time_start = service.time_start_thursday
        time_end = service.time_end_thursday
    elif day_of_week == "Friday":
        time_start = service.time_start_friday
        time_end = service.time_end_friday
    elif day_of_week == "Saturday":
        time_start = service.time_start_saturday
        time_end = service.time_end_saturday
    elif day_of_week == "Sunday":
        time_start = service.time_start_sunday
        time_end = service.time_end_sunday

    if time_start == 9999:
        return render(request,
                      'services/time_slots_options.html',
                       {'timeslots': [[9999, "Not availibe on {}".format(day_of_week)]]})


    bookings = ServiceBooking.objects.filter(Q(service=service) &
                                             Q(start_date = date)).values_list('time_slot',
                                                                               'number_of_pets')
    bookings = list(set(bookings))

    #get time_slots
    taken_slots = [x[0] for x in bookings]
    number_of_pets = [x[1] for x in bookings]

    list_of_options = get_options_of_timeslots_walk_sit(taken_slots,
                                                        time_start,
                                                        time_end)

    return render(request, 'services/time_slots_options.html', {'timeslots': list_of_options})


def send_sitter_confirmation_email(service, booking, user, email_address):
    """
    Send email to sitter after owner makes a booking
    """

    time_to_interval_converter = {
        9999:"Whole day",
        1:"01:00-02:00",
        2:"02:00-02:00",
        3:"03:00-04:00",
        4:"04:00-05:00",
        5:"05:00-06:00",
        6:"06:00-07:00",
        7:"07:00-08:00",
        8:"08:00-09:00",
        9:"09:00-10:00",
        10:"10:00-11:00",
        11:"11:00-12:00",
        12:"12:00-13:00",
        13:"13:00-14:00",
        14:"14:00-15:00",
        15:"15:00-16:00",
        16:"16:00-17:00",
        17:"17:00-18:00",
        18:"18:00-19:00",
        19:"19:00-20:00",
        20:"20:00-21:00",
        21:"21:00-22:00",
        22:"22:00-23:00",
        23:"23:00-00:00"
    }

    #creating context data
    timeslot = time_to_interval_converter[booking.time_slot]

    context = {
        "service":service,
        "booking":booking,
        "owner":user,
        "timeslot":timeslot
    }

    subject = 'You have a booking with MiiPets!'
    html_message = render_to_string('services/notify_sitter_booking_email.html',
                                    context)
    plain_message = strip_tags(html_message)
    from_email = 'info@miipets.com'
    to = email_address
    try:
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
    except mail.BadHeaderError:
        return HttpResponse('Invalid header found.')


def send_owner_confirmation_email(service, booking, sitter_answer):
    """
    Send email to owner after sitter confirms
    """

    time_to_interval_converter = {
        9999:"Whole day",
        1:"01:00-02:00",
        2:"02:00-02:00",
        3:"03:00-04:00",
        4:"04:00-05:00",
        5:"05:00-06:00",
        6:"06:00-07:00",
        7:"07:00-08:00",
        8:"08:00-09:00",
        9:"09:00-10:00",
        10:"10:00-11:00",
        11:"11:00-12:00",
        12:"12:00-13:00",
        13:"13:00-14:00",
        14:"14:00-15:00",
        15:"15:00-16:00",
        16:"16:00-17:00",
        17:"17:00-18:00",
        18:"18:00-19:00",
        19:"19:00-20:00",
        20:"20:00-21:00",
        21:"21:00-22:00",
        22:"22:00-23:00",
        23:"23:00-00:00"
    }

    #creating context data
    timeslot = time_to_interval_converter[booking.time_slot]

    context = {
        "service":service,
        "booking":booking,
        "owner":booking.requester,
        "timeslot":timeslot
    }

    if booking.sitter_answer:
        subject = 'Your MiiSitter has accepted your booking!'
    else:
        subject = 'Your MiiSitter has responded to your booking'

    html_message = render_to_string('services/notify_owner_booking_email.html',
                                    context)
    plain_message = strip_tags(html_message)
    from_email = 'info@miipets.com'
    to = booking.requester.email
    try:
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
    except mail.BadHeaderError:
        return HttpResponse('Invalid header found.')


@login_required(login_url='core-login')
def booking_confirmation(request, service_id, booking_id):


    booking = ServiceBooking.objects.get(id=booking_id)
    service = SitterServices.objects.get(id=service_id)

    # send email to sitter
    if booking.notified_sitter == False:
        try:
            send_sitter_confirmation_email(service, booking, request.user, service.sitter.email)
            print("SITTER NOTIFIED")
            booking.notified_sitter = True
            booking.save(update_fields=['notified_sitter'])
        except:
            print("Sitter notification email did not work")

    return render(request, 'services/booking_confirmation.html', {"user":request.user})


@login_required(login_url='core-login')
def sitter_confirmation(request, service_id, booking_id, sitter_answer):

    booking = ServiceBooking.objects.get(id=booking_id)
    service = SitterServices.objects.get(id=service_id)

    sitter_answer_converter = {
        0:False,
        1:True
    }

    if booking.sitter_confirmed:
        # sitter has already answered and can not change now
        pass
    else:
        booking.sitter_confirmed = True
        booking.sitter_answer = sitter_answer_converter[sitter_answer]

        #send owner email notifying of sitter answer
        try:
            send_owner_confirmation_email(service,
                                          booking,
                                          sitter_answer)
            booking.notified_owner_of_sitter_response = True
        except:
            print("Could not send email to owner")

        #update booking details
        booking.save(update_fields=['sitter_confirmed',
                                    'sitter_answer',
                                    'notified_owner_of_sitter_response'])

    return render(request, 'services/booking_confirmation_sitter.html', {"user":request.user, "sitter_answer":sitter_answer})

@login_required(login_url='core-login')
@agreed_terms_required
def view_sitter_profile(request, sitter_id):
    """
    When a someone clicks on the service sitter
    link they will be taken to this profile page
    where there is no option to edit profile
    """
    sitter = User.objects.get(id=sitter_id)
    miisitter = MiiSitter.objects.get(user=sitter)
    services = SitterServices.objects.filter(sitter=sitter)

    try:
        if request.user.is_sitter:
            context = {
                "services":services,
                "sitter":sitter,
                "sitter_user":True,
                "review_html":generate_review_html_start(miisitter.review_score),
                "review_score":miisitter.review_score,
            }
        else:
            context = {
                "services":services,
                "sitter":sitter,
                "sitter_user":False,
                "review_html":generate_review_html_start(miisitter.review_score),
                "review_score":miisitter.review_score,
            }
    except:
        context = {
            "services":services,
            "sitter":sitter,
            "sitter_user":False,
            "review_html":generate_review_html_start(miisitter.review_score),
            "review_score":miisitter.review_score,
        }

    return render(request, 'services/view_sitter_profile.html', context)

@login_required(login_url='core-login')
@agreed_terms_required
def view_owner_profile(request, owner_id):
    """
    When a someone clicks on the owner
    link they will be taken to this profile page
    where there is no option to edit profile
    """
    owner = User.objects.get(id=owner_id)
    pets = Pets.objects.filter(owner=owner)

    try:
        if request.user.is_sitter:
            context = {
                "pets":pets,
                "owner":owner,
                "sitter_user":True,
            }
        else:
            context = {
                "pets":pets,
                "owner":owner,
                "sitter_user":False,
            }
    except:
        context = {
            "pets":pets,
            "owner":owner,
            "sitter_user":False,
        }

    return render(request, 'services/view_owner_profile.html', context)


@login_required(login_url='core-login')
@agreed_terms_required
def owner_payment(request, service_id, booking_id):

    booking = ServiceBooking.objects.get(id=booking_id)
    service = SitterServices.objects.get(id=service_id)

    return render(request, 'services/payment_owner.html', {"user":request.user})
