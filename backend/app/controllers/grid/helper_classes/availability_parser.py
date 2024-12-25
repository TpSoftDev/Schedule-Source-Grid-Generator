"""
availability_parser.py

OVERVIEW:
    This module provides utility functions for parsing and processing availability data
    for a student's schedule. The main goal is to convert raw availability strings into
    structured data formats (lists of dictionaries) that are easier to work with programmatically.

    The parsed availability is used to determine and represent
    a student's available time slots in a structured format and output their time slots onto an Excel grid

FUNCTIONS:
    -parse_availability(studentId)
        Parses the full global availability data from Schedule Source and converts the date into
        an iterable dictionary list used to generate the grid

    - parse_availability_for_one_day(availStr):
        Parses a single day's availability string into a list of time range dictionaries.

DEPENDENCIES:
    - datetime: Used for parsing and handling time-related data.
    - convert_to_time: Helper function for converting string representations of time into `datetime.time` objects.
    - time_range_to_dict: Utility function for converting time range strings into structured dictionaries.

"""


import sys
from pathlib import Path
import datetime

#------------------------------------------------------------------------ Path Setup ------------------------------------------------------------------------#
# Get the absolute path of the current file and resolve any symlinks
# Then navigate up 4 levels to reach app directory:
# availability_parser.py -> helper_classes -> grid -> controllers -> app
root_dir = Path(__file__).resolve().parents[3]
sys.path.append(str(root_dir))

# Now we can import our local modules
from controllers.api.schedule_source_api import ScheduleSourceAPI
from utils.Credentials import load_creds
from utils.URLs import URLs
from controllers.grid.helper_classes.time_converter import time_range_to_dict, convert_to_time


def parse_availability(studentId):
    """
       Parses a student's availability by retrieving data from the Schedule Source API.

       This function retrieves global availability data for a student using their unique ID
       from the Schedule Source API  and converts the raw json response into a structured dictionary containing
       time ranges for each day.

       Parameters:
           studentId : str
               The unique identifier of the student whose availability is being queried.

       Returns:
           list : dict:
               A list of dictionaries where each dictionary represents a single day's availability:
                   - `'DayId'`: (int) The ID representing the day of the week (e.g., 1 for Sunday, 2 for Monday).
                   - `'DayRanges'`: (list of dict) A list of time ranges for the day, where each range contains:
                       - `'start_time'`: A `datetime.time` object marking the start of the range.
                       - `'end_time'`: A `datetime.time` object marking the end of the range.

    """

    creds = load_creds()
    credentials = {
        "code": creds.code,
        "user": creds.user,
        "password": creds.password
    }

    api = ScheduleSourceAPI(URLs.TEST_SITE_AUTH.value, credentials)
    if api.authenticate():
        print("Authentication Successful")
        try:
            # Will Hold the entire dictionary for all the days and their available ranges
            dict = []

            # Get the Global Availability from Schedule Source API
            availJson = api.get_global_availability(studentId)

            # Parsing one day at a time
            for day in availJson:
                #Extract the ranges for 1 day from entire availability
                dayRangeStr = day["AvailableRanges"]
                dayId = day["DayId"]

                #Use helper function to get a dictionary of start/end times for 1 day
                dayRangeDict = parse_availability_for_one_day(dayRangeStr)
                dict.append({
                    "DayId": dayId,
                    "DayRanges": dayRangeDict
                })

            return dict

        except Exception as e:
            print("ERROR OCCURRED ", e)
            return None


def parse_availability_for_one_day(availStr):
    """
    Parses a single day's availability string into a structured list of time ranges.
    by processing a string representation of availability for a single day,
    splits it into individual time ranges, and converts each range into a dictionary
    containing `start_time` and `end_time`.

    Parameters:
        availStr (str):
            A string representing the availability for a single day.
            Each time range is separated by a semicolon (`;`) and is in the format
            "startTime-endTime" (e.g., "9am-11am;1pm-3pm").

    Returns:
        list of dict:
            A list of dictionaries where each dictionary represents a time range for the day:
                - `'start_time'`: A `datetime.time` object marking the start of the range.
                - `'end_time'`: A `datetime.time` object marking the end of the range.
    """

    if not availStr:
        return [{
            "start_time": convert_to_time("", -1),
            "end_time": convert_to_time("", 1)
        }]

    rangesDict = []

    # String array with each time range
    rangesStr = availStr.split(';')
    rangesStr = [s for s in rangesStr if s]

    for rangeStr in rangesStr:
        rangeDict = time_range_to_dict(rangeStr)
        rangesDict.append(rangeDict)

    return rangesDict


