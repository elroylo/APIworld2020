import PySimpleGUI as sg

from os import system, name 
import requests
import json
from geopy.geocoders import Nominatim
import time
from datetime import datetime
from pprint import pprint
HEREDEV_API_KEY = 'cTCKSZTG3IDNqmvCbfRp-lEyJY48J24Ai6cbTDnVdJc'



############ Function: get_cord_from_addr ##########
# Input: Prompts user to enter address string
# returns lat, lon
####################################################
def get_cord_from_addr(addr):
    
    # Prompt user to enter address
    #addr = input("Enter address: ")
    
    # instantiate a new Nominatim client
    app = Nominatim(user_agent="tutorial")

    # get location raw data
    location = app.geocode(addr).raw

    #pprint(location) # print raw data
    
    return(location['lat'], location['lon'])
####################################################


########### Function: hd_discover_api ##############
# Input: lattitude and longitude
# Returns: list of business reported by Here Dev REST API 
####################################################
def hd_discover_api(lat, lon, bus_type, limit):
    api_key = "&apiKey=" + HEREDEV_API_KEY
    base_url = 'https://discover.search.hereapi.com/v1/discover'
    business_type = '&q=' + bus_type
    language = '&lang=en-US'
    limit = '&limit=' + limit
    lat_lon = '?at=' + lat + ',' + lon
    
    url = base_url + lat_lon + business_type + language + limit + api_key
        
    response = requests.get(url) # make REST API call
    
    # Get curated list of categories for use in GUI
    cl_raw = response.json()['items']
    
    i=0
    business_list = []
    for key in cl_raw:

        if (i== len(cl_raw)):
            break

        business_list.append(key["address"]["label"])
        i += 1 

        #print("categories: ", key["categories"])
        #print("categories.list: ", key["categories"][0])
        #print("phonemes.placenName = ", key["address"])
        #print("phonemes.placenName = ", key["address"]["label"])
        
        #name = key["address"]
        #print("name: ", name["label"])

        #print("phonemes.placenName, categories.list.name, categories.list.id= ", key["address"]["label"], key["categories"][0]["name"], key["categories"][0]["id"])
        
        #print("categories.list.id: ", key["categories"][0]["id"])

       
    
    #print("Number of business found: ", i)
    #print("Business list:")
    
    #for a in business_list:
    #    print(a)
    return(business_list)
    
########### END: hd_discover_api #################

#
# Main starts here
#

#GUI
sg.theme('Dark Blue 3')  # please make your windows colorful


layout = [
            [sg.Text('Enter address and business type e.g. hotel, train, etc')],
            [sg.Text('Address', size=(15, 1)), sg.InputText('San Francisco', key='-ADDRESS-')],
            [sg.Text('Business type', size=(15, 1)), sg.InputText('airport', key='-BUSINESS-')],
            [sg.HorizontalSeparator(color=None)],
            [sg.Text('How many business to show?')],
            [sg.Slider(range=(1,50), default_value=5, size=(20,15), orientation='horizontal', font=('Helvetica', 12), key='-LIMIT-')],
            [sg.Submit(), sg.Cancel()]
            ]

# layout = [
#             [sg.Text('Enter address and business type e.g. hotel, train, etc')],
#             [sg.Text('Address', size=(15, 1)), sg.InputText('San Francisco', key='-ADDRESS-')],
#             [sg.Text('Business type', size=(15, 1)), sg.InputText('airport', key='-BUSINESS-')],
#             [sg.HorizontalSeparator(color=None)],
#             [sg.Text('How many business to show?')],
#             [sg.Slider(range=(1,50), default_value=5, size=(20,15), orientation='horizontal', font=('Helvetica', 12), key='-LIMIT-')],
#             [sg.HorizontalSeparator(color=None)],
#             [sg.Text('Address', size=(15, 1)), sg.InputText('What do you want to search?', key='-SEARCH-')],
#             [sg.Submit(), sg.Cancel()]
#             ]
window = sg.Window('API World hackathon: Use of Here Dev REST API - Elroy Lobo', layout)

event, values = window.read()

# non-html code (same for HTML). All you need for input is:
# address, business-type and # of business to show
lat, lon = get_cord_from_addr(values['-ADDRESS-'])
bl = hd_discover_api(lat, lon, values['-BUSINESS-'], str(int(values['-LIMIT-']))) # Note: Slider returns float w/ a zero, so need conv

# Convert bl list to string format for easy to read display 
bl_str = ""
for ele in bl:
    bl_str += ele
    bl_str += '\n\n'

sg.Popup('Business found:\n', bl_str)


#window.close()