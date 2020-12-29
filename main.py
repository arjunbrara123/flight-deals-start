# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

import requests
import os
import data_manager
import notification_manager
import flight_search

# Initialise class references
flight_finder = flight_search.FlightSearch()
flight_data = data_manager.DataManager()
twilio = notification_manager.NotificationManager()

# Load up current flight data
flight_data.get_data()

# Update all city codes
for row in flight_data.data:

    #1. Update IATA Code
    iata_code = row['iataCode']
    if len(iata_code) == 0:
        print(row['city'])
        this_code = flight_finder.get_iata_code(row['city'])
        print(row)
        row['iataCode'] = this_code
        print(row)
        flight_data.set_data(row)

    # 2. Get lowest price
    search_results = flight_finder.get_price(iata_code)
    min_price = search_results[0]['price']
    for item in search_results:
        if item['price'] < min_price:
            min_price = item['price']

    # 3. Check if min price is lower than last price
    if min_price < row['lowestPrice']:
        row['lowestPrice'] = min_price
        flight_data.set_data(row)
        msg = f"Lowest price is {min_price} from Edinburgh to {row['city']}!"
        twilio.send_msg(msg, "+447506256864")

# Refresh latest flight data
flight_data.get_data()




