import googlemaps
from datetime import datetime
from geopy.distance import geodesic
from django.conf import settings
from datetime import datetime, timedelta


def sort_out_dates(start_date, end_date):
    """
    This function will return the correct start and end date of a
    a users input. The locig is as follow:

    If both dates are missing, then return todays date and next week date
    If just end date is missing, return a week laters date
    If no start date but end date, take today and end date
    If start date after end date, rotate
    If start date or end date before today, then apply first logic

    Input: YYYY-MM-DD, YYYY-MM-DD
    Ouput: YYYY-MM-DD, YYYY-MM-DD
    """

    today = datetime.today().strftime('%Y-%m-%d')

    if not start_date:
        start_date = today

    if not end_date:
        end_date = datetime.strptime(start_date, '%Y-%m-%d') + timedelta(7)
        end_date = end_date.strftime('%Y-%m-%d')

    if datetime.strptime(start_date, '%Y-%m-%d') > datetime.strptime(end_date, '%Y-%m-%d'):
        start_date, end_date = end_date, start_date

    return start_date, end_date

def address_to_lat_long(city, province, street_name, street_number, area_code):
    """
    This function takes in the address details and returns the lattitude and longitude
    of the adress using the google maps API from Goodle cloud.

    Input example: 'Secunda', 'Mpumalanga', 'Grobler Street', '13', '2302'
    Output example: 17022.23, 1233.34
    """

    gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)

    # fetch long lat
    geocode_result = gmaps.geocode(f'{city} {province} {street_name} {street_number} {area_code}')

    # fetch from json
    try:
        lat = geocode_result[0]["geometry"]["location"]["lat"]
        lng = geocode_result[0]["geometry"]["location"]["lng"]
    except:
        lat=0
        lng=0

    return lat, lng
