from .helpers import time_zone, local_time, date
from .helpers import NMEASerialReader, NMEASerialDecode
import json
import logging


logger = logging.getLogger(__name__)


def time_information():
    """ Function that provides the time and date information """
    tz = time_zone()
    lt = local_time()
    day = date()
    date_value_pair = (f"{day} {lt} {tz}")
    return date_value_pair


def serial_reader(date_time: str) -> str:
    """ This function reads the data from the NMEA serial port and logs it to the log file. """

    read = NMEASerialReader()
    decode = NMEASerialDecode()

    gpgga_nmea = read.read_all()
    logger.info(gpgga_nmea)

    direction_lat = gpgga_nmea[3]
    direction_long = gpgga_nmea[5]

    utc_time = decode.decode_time(gpgga_nmea)
    alt = decode.decode_alt(gpgga_nmea) + "M"
    lat = decode.decode_lat(gpgga_nmea)
    long = decode.decode_long(gpgga_nmea)

    time_value_pair = (f"{utc_time} UTC")
    alt_value_pair = (f"{alt}")
    lat_value_pair = (f"{lat} degrees {direction_lat}")
    long_value_pair = (f"{long} degrees {direction_long}")

    values = {
        "date_and_time": date_time,
        "utc_time": time_value_pair,
        "altitude": alt_value_pair,
        "latitude": lat_value_pair,
        "longitude": long_value_pair
    }

    logger.info(time_value_pair)
    logger.info(alt_value_pair)
    logger.info(lat_value_pair)
    logger.info(long_value_pair)
    return json.dumps(values)
