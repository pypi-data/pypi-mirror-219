from datetime import datetime

import geocoder
import pytz

class TimeZoneForIpAddressMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # the ip_address retrieved is the ip address of your network
        # your ip_address decided by your network provider
        # if vpn is used, the ip_address will be decide by vpn used
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
        private_ip_address = request.META.get('REMOTE_ADDR')
        print("public ip address: {}".format(ip_address))
        print("private ip address: {}".format(private_ip_address))
        g = None
        if ip_address is not None:
            g = geocoder.ip(ip_address)

        if g and g[0].raw:
            timezone_name = g[0].raw["timezone"]
            timezone_obj = pytz.timezone(timezone_name)
            request.ip_info = g[0].raw
        else:
            # Default timezone if geolocation or timezone not found
            timezone_obj = pytz.timezone('UTC')
        # ip_info will be a dictionary of info regarding the ip_address provided
        # e.g., {'ip': <ip address>, 'city': <city>, 'region': <region>, 'country': <country code>, 'loc': <location coordinates e.g., (lat,lng)>,
        #  'org': <network provider>, 'postal': <post code>, 'timezone': <timezone>, 'readme': 'https://ipinfo.io/missingauth'}
        request.timezone = timezone_obj
        request.time = datetime.now().astimezone(request.timezone)
        response = self.get_response(request)
        

        print("{} client timezone: {}".format(ip_address,request.time))
        return response

