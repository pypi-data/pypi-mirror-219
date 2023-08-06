import datetime
from datetime import datetime, timedelta
from typing import Optional

from timezonefinder import TimezoneFinder
import pytz

from timezoneutils.convert import TimeZoneConvertor
from timezoneutils.tools import check_date_instance_aware

class TimeZoneUtils(TimezoneFinder):
    def __init__(self, bin_file_location: Optional[str] = None, in_memory: bool = False):
        super().__init__(bin_file_location, in_memory)

    def list_all_timezone(self):
        return pytz.all_timezones
    
    def list_all_dst_timezone(self):
        timezone = pytz.all_timezones
        dst_timezone = [item for item in filter(lambda x:self.timezone_is_DST(x), timezone)]
        return dst_timezone
    
    def timezone_offset(self, timezone_str: str):
        # return the offset hour and minutes of certain timezone comparing to utc
        # e.g., ["ahead", 8, 0] means 8 hours ahead of utc
        # e.g., ["behind", 8, 30] means 8 hours 30 minutes behind utc
        # if None is return means no offset
        current_time = datetime.now()
        timezone = current_time.astimezone(
            pytz.timezone(timezone_str)).isoformat()
        utc_offset = timezone[-6:]
        if(utc_offset[0]=="+"):
            return ["ahead", int(utc_offset[1:3]), int(utc_offset[4:])]
        elif(utc_offset[0]=="-"):
            return ["behind", int(utc_offset[1:3]), int(utc_offset[4:])]
        return None

    def timezone_is_DST(self, timezone_str: str):
        # check if a timezone is observing daylight savings time
        timezone = datetime.now().astimezone(pytz.timezone(timezone_str))
        return timezone.dst() != timedelta(0)
    
    def dst_start_end(self, timezone_str: str, year:int = datetime.today().year):
        # only return start and end date if timezone is observing daylight savings time
        date=[]
        if self.timezone_is_DST(timezone_str):
            timezone = pytz.timezone(timezone_str)
            for tz in timezone._utc_transition_times:
                if str(tz.isoformat()[:4]) == str(year):
                    date.append(tz.isoformat())
        return date
    
    def list_timezone_identifier_naive(self, dt:datetime = datetime.now()):
        timezone_list = []
        for tz in pytz.all_timezones:
            tz_utc_aware = dt.astimezone(pytz.timezone(tz))
            if "{}".format(tz_utc_aware)[:16] == "{}".format(dt)[:16]:
                timezone_list.append(tz)
        return timezone_list

    def get_timezone_identifier_aware(self, dt: datetime):
        # return the timezone identifier base on the aware timezone provided
        # return "Unknown" if naive timezone provided
        try:
            tz = dt.tzinfo
            return tz.zone
        except AttributeError:
            return "Unknown"
        
    def get_timezone_abbreviation_aware(self, dt:datetime):
        # return timezone abbreviations. 
        # e.g., "Asia/Tokyo" timezone dt returns "JST"
        check_date_instance_aware(dt)
        abbreviation = dt.strftime('%Z')
        return abbreviation
    
    def get_timezone_metadata(self, timezone_str:str):
        # return data regarding to a timezone
        timezones = pytz.country_timezones.items()
        country = []
        if timezones:
            for country_code, timezone in timezones:
                if timezone_str in timezone:
                    country.append(
                        (pytz.country_names.get(country_code), country_code)
                    )

        metadata = {
            'timezone_name': timezone_str,
            'timezone_abbraviation': datetime.now()
                                    .astimezone(pytz.timezone(timezone_str))
                                    .strftime('%Z'),
            'country':country
        }
        return metadata

    def time_zone_difference(self, timezone: list = [], coordinates: list = []):
        # calculate difference of two aware timezone
        # timezone are list of string. e.g., ["Asia/Tokyo","US/Central"]
        # coordinates are list of coordinates tuple e.g., [(lat,lng)]
        # prioritize timezone
        current_time = datetime.now()
        timezones = []
        if len(timezone) >= 1 and len(timezone) <= 2:
            for tz in timezone:
                timezones.append(
                    current_time
                    .astimezone(pytz.timezone(tz))
                    .isoformat()
                )
            if len(timezones) == 1:
                timezones.append(
                    current_time
                    .astimezone(pytz.utc)
                    .isoformat()
                )

        if len(coordinates) >= 1 and len(coordinates) <= 2 and len(timezone) == 0:
            for tz in coordinates:
                timezones.append(
                    TimeZoneConvertor().convert_time_to_another_use_coordinates(
                        lat=tz[0], lng=tz[1])
                )
            if len(timezones) == 1:
                timezones.append(
                    current_time.astimezone(pytz.utc)
                )
        if len(timezones) == 2:
            time1 = timezones[0][-6:-1]
            time2 = timezones[1][-6:-1]
            time1_hour = int(time1[0:3])
            time1_minutes = int(time1[4:])
            time2_hour = int(time2[0:3])
            time2_minutes = int(time2[4:])
            print(timezones)
            # both time are in the same positve side which means both utc is at positive
            if time1_hour >= 0 and time2_hour >= 0:
                minutes = abs(time1_minutes-time2_minutes)
                hours = abs(time1_hour-time2_hour)
                return hours, minutes

            # both time are in the same negative side which means both utc is at negative
            elif time1_hour < 0 and time2_hour < 0:
                minutes = abs(time1_minutes-time2_minutes)
                hours = abs(time1_hour-time2_hour)
                return hours, minutes

            else:
                external_hour = 0
                minutes = abs(time1_minutes+time2_minutes)
                if minutes >= 60:
                    minutes -= 60
                    external_hour += 0
                hours = abs(time1_hour-time2_hour)+external_hour
                return hours, minutes
        return None