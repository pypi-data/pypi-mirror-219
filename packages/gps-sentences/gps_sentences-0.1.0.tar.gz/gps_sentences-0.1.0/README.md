# gps_sentences

# Decoding GPS Sentences

## Purpose

- Create a package that will read GPS sentences from the serial terminal. 
- The package will be able to decode the information read from the serial terminal.

## Obtained Information

- Latitude
- Longitude
- Time
- Altitude

## Hardware Requirments

- GPS reciever module (The Geekstory GT-U7 GPS Module GPS Receiver Navigation Satellite Positioning NEO-6M with 6M 51 Microcontroller STM32 R3 + IPEX Active GPS Antenna High Sensitivity for Arduino Drone Raspberry Pi Flight, was used for development purposes, and has the most compatibility with this API).
- The API will expect the GPS reciever to output information in an NMEA sentence format. The desired NMEA sentence format in particular is $GPGGA.


## Installation

### Permissions

- Depending on your OS of choice, you may need to change the permissions of the serial port. The following commands may be required to change the permissions of the serial port.
* `sudo chmod 777 /dev/ttyACM*` - temporary and **UNSAFE** fix
* `sudo usermod -a -G dialout $USER` - permanent fix; **reboot required**
* `sudo usermod -a -G uucp $USER` - permanent fix; **reboot required**

### Requirements

* Python 3.10+
* git

### Install from GitHub

- Navigate to a directory where you would wish to install this package and run these commands in the terminal.
`python -m venv venv` - Optional, but very **recommended**.
`source venv/bin/activate` - Required, if last line is executed.
`pip install gps_sentences`
`gps` is the command to run the program. 
 
## Synopsis

- Create a python package that will take in any format of GPS information.

## Description

- The package will NOT be dependent on any particular type of GPS device. The package will feature an option to read in the information from the particular model we have on hand (USB Serial Device).
- The accuracy of the GPS signal, and distance to the next point will be optional features of the project.





# GPS Sentences API Interface

## API for reading GPS Sentence information from the terminal

## Introduction

- This is an api where you will be able to recieve GPS information from the serial terminal where a moduel gps reciever is connected. 

## Features

- The GPS sentence format is $GPGGA NMEA.
- Successive get requests contain updated information recieved from the terminal.
- No post functionallity has been implemented as of this moment. 
- Information is limited to the information that can be found in the $GPGGA NMEA format.


## API Design

- Host is defined as 127.0.0.1, and the established port is 8084.
- /all_serial_data
    - GET: Returns all of the serial data extracted from the terminal. Returns the latitude and longitude, altitude, date and time in your current time zone, and the universal coordinated time.
- /all_serial_data/lat_long
    - GET: Returns the latitude and longitude of the current location in JSON.
- /all_serial_data/altitude
    - GET: Returns the altitude of the current location in JSON.
- /all_serial_data/utc_time
    - GET: Returns the UTC time of the current location in JSON.
- /all_serial_data/date_time
    - GET: Returns the date and time of the current location and time zone in JSON.

## Examples / Use Cases

- To find out your latitutude and longitude, you may run the program to initialize the API server.
- After the server is initailized, you may enter this url http://127.0.0.1:8000/all_serial_data/lat_long  into your browser or an interactive api client where you can input urls.
- The expected information should be the latitude and longitude information in this json format. {"latitude": "26.286172 N", "longitude": "80.291557 W"}

## Obtained Information

- Latitude
- Longitude
- Time
- Altitude

