from src.helpers.helpers import NMEASerialReader, NMEASerialDecode
import json


def json_lat_long():
    """ Returns the latitude and longitude of the current location in JSON format """
    read = NMEASerialReader()
    decode = NMEASerialDecode()
    gpgga_nmea = read.read_all()
    direction_lat = gpgga_nmea[3]
    direction_long = gpgga_nmea[5]
    lat = decode.decode_lat(gpgga_nmea)
    long = decode.decode_long(gpgga_nmea)
    lat_value_pair = (f"{lat} {direction_lat}")
    long_value_pair = (f"{long} {direction_long}")
    values = {
        "latitude": lat_value_pair,
        "longitude": long_value_pair
    }
    return json.dumps(values)



