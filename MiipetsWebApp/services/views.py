from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from core.decorators import miiowner_required
from core.models import User, Pets, SitterServices, ServicePhotos
from core.models import ServiceBooking, ServiceLocation, ServiceReviews
from django.views.generic import ListView
from django.db.models import Q
from core.methods import sort_out_dates, filter_on_location


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

        #get relevant services not based on location
        services = SitterServices.objects.filter(Q(type__in=type)&
                                                 Q(date_start__lte=start_date)&
                                                 Q(date_end__gte=end_date))


        #filter on location
        services,locations = filter_on_location(services, request.GET['location_input'])

        services = zip(services, locations)

        try:
            if request.user.is_sitter:
                context = {
                    "title": "View pet services",
                    "type":"Services",
                    "sitter_user":True,
                    "services":services
                    }
            else:
                context = {
                    "title": "View pet services",
                    "type":"Services",
                    "sitter_user":False,
                    "services":services
                    }
        except:
            context = {
                "title": "View pet services",
                "type":"Services",
                "sitter_user":False,
                "services":services
                }

    return render(request, 'services/single-type-services.html', context)



def view_single_service(request, service_id):

    service = SitterServices.objects.get(id=service_id)
    similar_services = SitterServices.objects.filter(
                      Q(type=service.type) &
                      (Q(price__lte=service.price*1.2) &  Q(price__gte=service.price*0.8)) &
                      ~Q(id = service.id)
                      )

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
            }

    print(context)
    return render(request, 'services/single-service.html', context)
