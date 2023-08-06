import os
import datetime
from datetime import datetime
from typing import Optional

from dotenv import load_dotenv
from timezonefinder import TimezoneFinder
import pytz
import requests

from timezoneutils.tools import check_date_instance, check_date_instance_aware

class TimeZoneConvertor(TimezoneFinder):
    def __init__(self, bin_file_location: Optional[str] = None, in_memory: bool = False):
        super().__init__(bin_file_location, in_memory)

    def convert_datetime_to_another_use_coordinates(self, lat: float, lng: float, dt: datetime = None):
        # return the converted timezone for an area using coordinates. 
        # Date is optional, if not provided, will use local system datetime
        # If date is naive, it will be treated as local system timezone
        # e.g., datetime(2023, 7, 14, 12, 0, 0) will be treated as 2023-07-14T12:00:00+09:00 if local tz is Asia/Tokyo
        timezone_identifier = self.timezone_at(lat=lat,lng=lng)
        current_time = dt if check_date_instance(dt) and dt else datetime.now()
        new_time = current_time.astimezone(pytz.timezone(timezone_identifier))
        return new_time.isoformat()
    
    def convert_datetime_to_another_use_address(self, address: str, dt: datetime = None):
        # get the lat and lng using the address to get the local timezone for the address provided. Use geoapify for this function
        # you can override tis function to use your prefered geo service
        # If you aren't using this function, you don't have to provide api key 

        load_dotenv()
        # Replace YOUR_API_KEY with your actual API key in  your envitonment variable file. Sign up and get an API key on https://www.geoapify.com/
        API_KEY = os.getenv("API_KEY")

        # Build the API URL
        url = f"https://api.geoapify.com/v1/geocode/search?text={address}&limit=1&apiKey={API_KEY}"

        # Send the API request and get the response
        response = requests.get(url)

        # Check the response status code
        if response.status_code == 200:
            # Parse the JSON data from the response
            data = response.json()

            # Extract the first result from the data
            result = data["features"][0]

            # Extract the latitude and longitude of the result
            latitude = result["geometry"]["coordinates"][1]
            longitude = result["geometry"]["coordinates"][0]

            print(f"Latitude: {latitude}, Longitude: {longitude}")
            return self.convert_datetime_to_another_use_coordinates(lat=latitude, lng=longitude, dt=dt)
        else:
            print(f"Request failed with status code {response.status_code}")
            return None

    def convert_aware_datetime_to_another_use_timezone_str(self, timezone_str: str, dt: datetime = None):
        # will use local system timezone if not aware date time
        # if you want to convert from a timezone but you have a naive datetime
        # you can <Object dateime.datetime>.replace.replace(tzinfo=tz.gettz('America/New_York'))
        # to turn it to aware datetime, The example shown use 'America/New_York' timezone
        current_time = dt if check_date_instance_aware(dt) and dt else datetime.now()
        new_time = current_time.astimezone(pytz.timezone(timezone_str))
        return new_time.isoformat()
    

