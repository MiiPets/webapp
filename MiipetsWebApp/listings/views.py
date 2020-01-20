from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from core.decorators import miiowner_required
from core.models import User, Pets, SitterServices
from django.views.generic import ListView

def view_all_listings(request):
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

def view_listings(request, type):
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




# def view_single_listings(request, service_id):
#
#     service = SitterServices.objects.get(id=service_id)
#
#
#     try:
#         if request.user.is_sitter:
#             context = {
#                 "title": service.listing_name,
#                 "sitter_user":True,
#                 'type':service.type,
#                 "listing_name":service.listing_name,
#                 #"list_address":service.address,
#                 "listing_description":service.description,
#                 'price':service.price,
#                 #'number_of_reviews':15,
#                 #"reviews":reviews,
#                 #"timeslots":timeslots
#                 }
#         else:
#             context = {
#                 "title": service.listing_name,
#                 "sitter_user":False,
#                 'type':service.type,
#                 "listing_name":service.listing_name,
#                 #"list_address":service.address,
#                 "listing_description":service.description,
#                 'price':service.price,
#                 #'number_of_reviews':15,
#                 #"reviews":reviews,
#                 #"timeslots":timeslots
#                 }
#     except:
#         context = {
#                 "title": service.listing_name,
#                 "sitter_user":False,
#                 'type':service.type,
#                 "listing_name":service.listing_name,
#                 #"list_address":service.address,
#                 "listing_description":service.description,
#                 'price':service.price,
#                 #'number_of_reviews':15,
#                 #"reviews":reviews,
#                 #"timeslots":timeslots
#             }
#
#     return render(request, 'listings/single-listing.html', context)
