import requests
import json
from secret import google_geo_coder


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# This module is named after our first software developer intern -- Jans_Bertran --
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


def api_call(zip_code):
    """takes inputted zip code calls upon googles geocoding api to receive location details"""
    URL = f"https://maps.googleapis.com/maps/api/geocode/json?address={str(zip_code)}&key={google_geo_coder}"
    payload = {}
    headers = {}
    return requests.request("GET", URL, headers=headers, data=payload)


def type_finder(components: list, desired_level: str) -> str:
    """return what position in the address components
    list that the disreed address componenet lies in"""
    for i, v in enumerate(components):
        if v['types'][0] == desired_level:
            return i


def goog_coords_api_formater(response: str) -> dict:
    """takes in a api response from google geocoding and
    returns a dictionary of location information"""
    adress_components = response.json()['results'][0]['address_components']
    coords = response.json()['results'][0]['geometry']['location']
    data = {
        'zip': [adress_components[type_finder(adress_components, 'postal_code')]['long_name']],
        'city': [response.json()['results'][0]['address_components'][1]['long_name']],
        'county_name': [adress_components[type_finder(adress_components, 'administrative_area_level_2')]['long_name']],
        'state_name': [adress_components[type_finder(adress_components, 'administrative_area_level_1')]['long_name']],
        'lat': [coords["lat"]],
        'lng': [coords["lng"]],
    }
    return data


def jb_geo_coder(zip_code: int) -> json:
    print('Thank you raspberry')
    return goog_coords_api_formater(api_call(zip_code))


if __name__ == '__main__':
    zip = input('Enter a zip: \n')
    print(jb_geo_coder(zip))
