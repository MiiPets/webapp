import googlemaps
from datetime import datetime
from geopy.distance import geodesic
from django.conf import settings
from datetime import datetime, timedelta
from core.models import ServiceLocation, ServiceReviews
import geopy.distance
import numpy as np


def sort_out_dates(start_date, end_date):
    """
    This function will return the correct start and end date of a
    a users input. The locig is as follow:

    If both dates are missing, then return todays date and next week date
    If just end date is missing, return a week laters date
    If no start date but end date, take today and end date
    If start date after end date, rotate
    If start date or end date before today, then apply first logic

    Input: MM-DD-YYYY, MM-DD-YYYY
    Ouput: MM-DD-YYYY, MM-DD-YYYY
    """

    today = datetime.date(datetime.today())

    if not start_date:
        start_date = today
    else:
        month_s,day_s,year_s = start_date.split('/')
        start_date = datetime(int(year_s), int(month_s), int(day_s))

    if not end_date:
        end_date = start_date + timedelta(7)
    else:
        month_e,day_e,year_e = end_date.split('/')
        end_date = datetime(int(year_e), int(month_e), int(day_e))

    if start_date > end_date:
        start_date, end_date = end_date, start_date

    try:
        start_date = datetime.strptime(str(start_date), "%Y-%m-%d %H:%M:%S")
        end_date = datetime.strptime(str(end_date), "%Y-%m-%d %H:%M:%S")
    except:
        pass

    return start_date, end_date

def address_to_lat_long(full_addres='', city="", province="", street_name="", street_number='', area_code=''):
    """
    This function takes in the address details and returns the lattitude and longitude
    of the adress using the google maps API from Goodle cloud.

    Input example: 'Secunda', 'Mpumalanga', 'Grobler Street', '13', '2302'
    Output example: 17022.23, 1233.34
    """
    gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)

    # fetch long lat
    if full_addres:
        geocode_result = gmaps.geocode(full_addres)
    else:
        geocode_result = gmaps.geocode(f'{city} {province} {street_name} {street_number} {area_code}')

    # fetch from json
    try:
        lat = geocode_result[0]["geometry"]["location"]["lat"]
        lng = geocode_result[0]["geometry"]["location"]["lng"]
    except:
        lat=0
        lng=0

    return lat, lng


def filter_on_location(services, searched_location):
    """
    This function will filter the current services and only return the services
    that are within a certian radius of the given location.
    """

    lat_search, lng_search = address_to_lat_long(searched_location)

    # get location data of services
    ids = [service.id for service in services]
    locations = ServiceLocation.objects.filter(id__in=ids)

    # create coordinate sets
    lat_long_sets = [(location.lattitude, location.longitude) for location in locations]
    # get distances
    distances = [geopy.distance.vincenty((lat_search, lng_search), location).km for location in lat_long_sets]

    # order services by distance rather than not giving anything
    sorted_indexes = sorted(range(len(distances)),key=distances.__getitem__)

    # # get passed values
    services = [services[index] for index in sorted_indexes ]
    # id_passed = [ids_loc[index] for index in passed_indexes ]
    locations =  [locations[index] for index in sorted_indexes ]

    return services, locations
