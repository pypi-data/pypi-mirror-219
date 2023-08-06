from src.helpers.helpers import NMEASerialReader, NMEASerialDecode
from src.helpers.helpers import time_zone, local_time, date
import json

def json_date_time():
    """ Returns the current date as a string in json format """
    read = NMEASerialReader()
    decode = NMEASerialDecode()
    gpgga_nmea = read.read_all()
    tz = time_zone()
    lt = local_time()
    day = date()
    date_value_pair = (f"{day} {lt} {tz}")
    value = {
        "date_time" : date_value_pair
    }
    return json.dumps(value)