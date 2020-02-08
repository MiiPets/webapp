from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from core.decorators import miiowner_required
from core.models import User, Pets, SitterServices, ServicePhotos
from core.models import ServiceBooking, ServiceLocation, ServiceReviews
from django.views.generic import ListView
from django.db.models import Q
from core.methods import sort_out_dates, filter_on_location, return_day_of_week_from_date
from core.methods import  get_options_of_timeslots_walk_sit, get_options_of_timeslots_board_daycare
from .forms import BookService

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
                type = type_dictionary.values()
        except:
            type = [type_dictionary[type]]

        #check if dates are correct
        try:
            start_date, end_date = sort_out_dates(request.GET['date_begin_input'], request.GET['date_end_input'])
        except:
            start_date, end_date = sort_out_dates('', '')

        try:
            price_start = request.GET['price_start']
            price_end = request.GET['price_end']

            if price_start > price_end:
                price_start, price_end = price_end, price_start

            if not price_start:
                price_start = 0
                price_end = 99999999
        except:
            price_start = 0
            price_end = 99999999

        # checking for pet type
        try:
            pet_type = request.GET['pet_type']
        except:
            pet_type = "All Pets"

        want_dog = True
        want_cat = True
        want_bird = True
        want_reptile = True
        want_other = True

        if pet_type == "Dog":
            want_cat = False
            want_bird = False
            want_reptile = False
            want_other = False
        elif pet_type == "Cat":
            want_dog = False
            want_bird = False
            want_reptile = False
            want_other = False
        elif pet_type == "Bird":
            want_cat = False
            want_dog = False
            want_reptile = False
            want_other = False
        elif pet_type == "Reptile":
            want_dog = False
            want_cat = False
            want_bird = False
            want_other = False
        elif pet_type == "Other":
            want_dog = False
            want_cat = False
            want_bird = False
            want_reptile = False


        #get relevant services not based on location
        if pet_type == "All Pets":
            services = SitterServices.objects.filter(Q(type__in=type)&
                                                     Q(date_start__lte=start_date)&
                                                     Q(date_end__gte=end_date)&
                                                     Q(price__range=[price_start, price_end]))
        else:
            services = SitterServices.objects.filter(Q(type__in=type)&
                                                     Q(date_start__lte=start_date)&
                                                     Q(date_end__gte=end_date)&
                                                     Q(price__range=[price_start, price_end])&
                                                     Q(dogs_allowed=want_dog)&
                                                     Q(cats_allowed=want_cat)&
                                                     Q(birds_allowed=want_bird)&
                                                     Q(reptiles_allowed=want_reptile)&
                                                     Q(other_pets_allowed=want_other))

        #filter on location
        try:
            location_input = request.GET['location_input']
            services,locations = filter_on_location(services, location_input)
        except:
            location_input = ""
            ids = [service.id for service in services]
            locations = ServiceLocation.objects.filter(id__in=ids)

        if not location_input:
            location_input = "Location"

        services = zip(services, locations)

        try:
            if request.user.is_sitter:
                context = {
                    "title": "View pet services",
                    "type":"Services",
                    "sitter_user":True,
                    "services":services,
                    "location_input":location_input
                    }
            else:
                context = {
                    "title": "View pet services",
                    "type":"Services",
                    "sitter_user":False,
                    "services":services,
                    "location_input":location_input
                    }
        except:
            context = {
                "title": "View pet services",
                "type":"Services",
                "sitter_user":False,
                "services":services,
                "location_input":location_input
                }

    return render(request, 'services/single-type-services.html', context)


@login_required(login_url='core-login')
def view_single_service(request, service_id):

    service = SitterServices.objects.get(id=service_id)
    similar_services = SitterServices.objects.filter(
                          Q(type=service.type) &
                          (Q(price__lte=service.price*1.2) &  Q(price__gte=service.price*0.8)) &
                          ~Q(id = service.id))

    photos = ServicePhotos.objects.filter(service=service)
    location = ServiceLocation.objects.get(service=service)
    sitter = User.objects.get(id=service.sitter.id)

    type_converter = {"BOARD":"Boarding",
                      "SIT": "House Sitter/Feeder",
                      "WALK":"Walker",
                      "DAYCARE":"Daycare"}

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
            form.save()
            return redirect('services-booking-confirmation')
    else:
        form = BookService(user = request.user, service = service)

    try:
        if request.user.is_sitter:
            context = {
                "title": "Single pet service",
                "sitter":sitter,
                "similar_services":similar_services,
                "sitter_user":True,
                'type':type_converter[service.type],
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
                "sitter_user":False,
                'type':service.type,
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
                "sitter_user":False,
                'type':service.type,
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
    booked_pets = request.GET.get('booked_pets')
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

def booking_confirmation(request):
    return render(request, 'services/booking_confirmation.html')
