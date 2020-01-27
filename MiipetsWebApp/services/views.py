from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from core.decorators import miiowner_required
from core.models import User, Pets, SitterServices
from django.views.generic import ListView


def view_all_services(request):
    """
    This view allows everyone to view all current listings
    """
    try:
        if request.user.is_sitter:
            context = {
                "title": "All Listings",
                #"listings":listings,
                "sitter_user":True
                }
        else:
            context = {
                "title": "All Listings",
                #"listings":listings,
                "sitter_user":False
                }
    except:
        context = {
            "title": "All Listings",
            #"listings":listings,
            "sitter_user":False
            }

    return render(request, 'listings/all-listings.html', context)

def view_services(request, type):
    """
    This view allows everyone to view all current listings
    """
    try:
        if request.user.is_sitter:
            context = {
                "title": type,
                "type":type.upper(),
                #"listings":listings,
                "sitter_user":True
                }
        else:
            context = {
                "title": type,
                #"listings":listings,
                "type":type.upper(),
                "sitter_user":False
                }
    except:
        context = {
            "title": type,
            #"listings":listings,
            "type":type.upper(),
            "sitter_user":False
            }

    return render(request, 'listings/single-type-listings.html', context)



def view_single_service(request, service_id):
    
    # sitter
    # service_name
    # type
    # description
    # price
    # profile_picture
    # date_start
    # date_end
    # time_start_monday
    # time_start_tuesday
    # time_start_wednesday
    # time_start_thursday
    # time_start_friday
    # time_start_saturday
    # time_start_sunday
    # time_end_monday
    # time_end_tuesday
    # time_end_wednesday
    # time_end_thursday
    # time_end_friday
    # time_end_saturday
    # time_end_sunday

    service = SitterServices.objects.get(id=service_id)
    print(service)

    try:
        if request.user.is_sitter:
            context = {
                "title": service.type,
                "sitter_user":True,
                'type':service.type,
                "service_name":service.service_name,
                "service_description":service.description,
                'price':service.price,
                }
        else:
            context = {
                "title": service.type,
                "sitter_user":False,
                'type':service.type,
                "service_name":service.service_name,
                "service_description":service.description,
                'price':service.price,
                }
    except:
        context = {
                "title": service.type,
                "sitter_user":False,
                'type':service.type,
                "service_name":service.service_name,
                "service_description":service.description,
                'price':service.price,
            }

    return render(request, 'services/single-service.html', context)
