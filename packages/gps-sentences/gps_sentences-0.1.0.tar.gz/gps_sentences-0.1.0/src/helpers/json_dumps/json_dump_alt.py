from src.helpers.helpers import NMEASerialReader, NMEASerialDecode
import json

def json_alt():
    """ Returns a json object with the altitude from the NMEA serial reader. """
    read = NMEASerialReader()
    decode = NMEASerialDecode()
    gpgga_nmea = read.read_all()
    alt = decode.decode_alt(gpgga_nmea) + "M"
    alt_value_pair = (f"{alt}")
    value = {
        "altitude": alt_value_pair
    }
    return json.dumps(value)
    