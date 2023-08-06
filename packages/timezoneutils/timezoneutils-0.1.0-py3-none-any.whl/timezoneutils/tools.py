from datetime import datetime

def check_date_instance(datetimefield):
    # check is datetime.datetime object
    if datetimefield is None:
        return False
    if not isinstance(datetimefield, datetime):
        raise TypeError('datetimefield must be a datetime.datetime object')
    return True


def check_date_instance_aware(datetimefield):
    # check is an aware datetime.datetime object 
    if check_date_instance(datetimefield):
        try:
            datetimefield.tzinfo
            return True
        except AttributeError:
            raise TypeError('datetimefield must be an aware (not naive) datetime.datetime object')
    return False

