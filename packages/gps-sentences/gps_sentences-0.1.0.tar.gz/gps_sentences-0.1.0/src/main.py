""" Create a package that will read and decode GPS sentences from the serial terminal. """
from .helpers.serial_run import serial_reader
from .helpers.serial_run import time_information
from .helpers.json_dumps.json_dump_lat_long import json_lat_long
from .helpers.json_dumps.json_dump_alt import json_alt
from .helpers.json_dumps.json_dump_utctime import json_utc_time
from .helpers.json_dumps.json_dump_date import json_date_time
from fastapi import FastAPI
import uvicorn


def main():
    """ Main function """
    serial_reader(time_information())
    app = FastAPI()

    @app.get("/")
    async def index():
        """ Root endpoint """
        return {"message": "This is the root endpoint."}

    @app.get("/all_serial_data")
    async def all_serial_data():
        """ Returns all serial data """
        return {serial_reader(time_information())}

    @app.get("/all_serial_data/lat_long")
    async def all_serial_data_lat_long():
        """ Returns the latitude and longitude of the current location in JSON format"""
        return {json_lat_long()}

    @app.get("/all_serial_data/altitude")
    async def all_serial_data_altitude():
        """ Returns the altitude of the current location in JSON format"""
        return {json_alt()}

    @app.get("/all_serial_data/utc_time")
    async def all_serial_data_utc_time():
        """ Returns the UTC time of the current location in JSON format"""
        return {json_utc_time()}

    @app.get("/all_serial_data/date_time")
    async def all_serial_data_date_time():
        """ Returns the date and time of the current location in JSON format"""
        return {json_date_time()}

    uvicorn.run(app, host="127.0.0.1", port=8084)


if __name__ == '__main__':
    """ Main function """
    main()
