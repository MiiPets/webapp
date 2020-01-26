import googlemaps
from datetime import datetime
from geopy.distance import geodesic
from django.conf import settings

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
    lat = geocode_result[0]["geometry"]["location"]["lat"]
    lng = geocode_result[0]["geometry"]["location"]["lng"]

    return lat, lng
