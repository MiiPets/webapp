import googlemaps
from datetime import datetime
from geopy.distance import geodesic
from django.conf import settings
from datetime import datetime, timedelta
from core.models import ServiceLocation, ServiceReviews
import geopy.distance
import numpy as np
import hashlib
import urllib.parse

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

def address_to_lat_long(full_addres='', city="", province="",
                         street_name="", street_number='', area_code=''):
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
    locations = ServiceLocation.objects.filter(service__in=services)
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


def return_day_of_week_from_date(date_string):
    """
    Function to return the day of the week from the given date string.

    Input format: YYYY-MM-DD
    Output: "Monday"
    """

    return datetime.strptime(date_string, '%Y-%m-%d').strftime('%A')


def calculate_number_of_days(start_date, end_date):
    """
    Function to calculate the number of days between dates given

    Input format: YYYY-MM-DD, YYYY-MM--D
    Output: 2
    """
    if start_date > end_date:
        start_date, end_date = end_date, start_date
    delta = end_date - start_date

    return delta.days


def make_sure_start_before_end_date(start_date, end_date):
    '''
    Function to ensure the start date is before the end date
    '''

    if start_date > end_date:
        start_date, end_date = end_date, start_date

    return start_date, end_date


def get_options_of_timeslots_walk_sit(taken_slots, time_start, time_end):
    """
    This function will take the booked time slots and the times
    between when the service is open for. It will then return a list of lists
    containing possible timeslots that can be fed into the drop down list on booking
    page. When booking for daycare or boarding, will check number of pets as
    well

    Input: [2,4,5], 1, 8
    returns: [[1, "01:00-02:00"], [3, "03:00-04:00"],[6, "06:00-07:00"],[7, "07:00-08:00"]]
    """

    time_to_interval_converter = {
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

    if time_end == 0:
        time_end = 24

    time_operates = list(range(time_start, time_end+1))
    availibe_intervals = [x for x in time_operates if x not in taken_slots]
    options = [[x, time_to_interval_converter[x]] for x in availibe_intervals ]

    return options


def get_options_of_timeslots_board_daycare (taken_dates, number_of_pets, requested_pets,
                                            maximum_pets, date_start, date_end):

    """
    This function will take the booked time slots and the times
    between when the service is open for as well as not to much pets.
    It will then return a list of lists containing possible timeslots
    that can be fed into the drop down list on booking page.

    Input: [2,4,5], 1, 4, 7 9
    returns: [[1, "01:00-02:00"], [3, "03:00-04:00"],[6, "06:00-07:00"],[7, "07:00-08:00"]]
    """

    time_to_interval_converter = {
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

    if time_end == 0:
        time_end = 24

    time_operates = list(range(time_start, time_end+1))
    pet_in_slot = {slot:0 for slot in time_operates}

    for taken_slot, pet in zip(taken_slots,number_of_pets):
        pet_in_slot[taken_slot].append(pet)

    for slot in pet_in_slot.keys():
        pet_in_slot[slot] = sum(pet_in_slot[slot])

    time_slots_availible = [slot for slot in pet_in_slot.keys() if pet_in_slot[slot]+requested_pets <= maximum_pets]
    options = [[x, time_to_interval_converter[x]] for x in time_slots_availible ]

    return options


def create_signature(list_of_values):

    """
    Required to create hash function for Payfast payments
    """

    signature_string = urllib.parse.urlencode(list_of_values, encoding='utf-8', errors='strict')
    signature = hashlib.md5(signature_string.rstrip().encode('ascii')).hexdigest()
    print(signature_string)
    print(signature)
    return signature


def generate_review_html_start(rating):

    """
    This function will return html that displays the rating in terms of
    stars. It will always generate x.5 or x.0 stars. The function returns the html that should
    be inserted into the template.
    """

    one_star_total = """<ul class="product-rating">
        <li><i class="ion-android-star"></i></li>
        <li><i class="ion-android-star-half"></i></li>
        </ul>
    """

    one_half_star_total = """<ul class="product-rating">
        <li><i class="ion-android-star"></i></li>
        </ul>
    """

    two_star_total = """<ul class="product-rating">
        <li><i class="ion-android-star"></i></li>
        <li><i class="ion-android-star"></i></li>
        </ul>
    """

    two_half_star_total = """<ul class="product-rating">
        <li><i class="ion-android-star"></i></li>
        <li><i class="ion-android-star"></i></li>
        <li><i class="ion-android-star-half"></i></li>
        </ul>
    """

    three_star_total = """<ul class="product-rating">
        <li><i class="ion-android-star"></i></li>
        <li><i class="ion-android-star"></i></li>
        <li><i class="ion-android-star"></i></li>
        </ul>
    """

    three_half_star_total = """<ul class="product-rating">
        <li><i class="ion-android-star"></i></li>
        <li><i class="ion-android-star"></i></li>
        <li><i class="ion-android-star"></i></li>
        <li><i class="ion-android-star-half"></i></li>
        </ul>
    """

    four_star_total = """<ul class="product-rating">
        <li><i class="ion-android-star"></i></li>
        <li><i class="ion-android-star"></i></li>
        <li><i class="ion-android-star"></i></li>
        <li><i class="ion-android-star"></i></li>
        </ul>
    """

    four_half_star_total = """<ul class="product-rating">
        <li><i class="ion-android-star"></i></li>
        <li><i class="ion-android-star"></i></li>
        <li><i class="ion-android-star"></i></li>
        <li><i class="ion-android-star"></i></li>
        <li><i class="ion-android-star-half"></i></li>
        </ul>
    """

    five_star_total = """<ul class="product-rating">
        <li><i class="ion-android-star"></i></li>
        <li><i class="ion-android-star"></i></li>
        <li><i class="ion-android-star"></i></li>
        <li><i class="ion-android-star"></i></li>
        <li><i class="ion-android-star"></i></li>
        </ul>
    """

    if 0 <= rating <= 1.49:
        return one_star_total
    elif 1.49 <= rating <= 1.99:
        return one_half_star_total
    elif 2 <= rating <= 2.49:
        return two_star_total
    elif 2.49 <= rating <= 2.99:
        return two_half_star_total
    elif 3.0 <= rating <= 3.49:
        return three_star_total
    elif 3.49 <= rating <= 3.99:
        return three_half_star_total
    elif 4 <= rating <= 4.49:
        return four_star_total
    elif 4.49 <= rating <= 4.8:
        return four_half_star_total
    elif 4.8 <= rating <= 5:
        return five_star_total
    else:
        return "No reviews yet"
