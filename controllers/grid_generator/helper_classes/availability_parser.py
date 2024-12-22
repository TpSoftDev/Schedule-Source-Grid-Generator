import sys
import os

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.append(project_root)

from controllers.api_calls.test_site.schedule_source_api import ScheduleSourceAPI
from controllers.utils.Credentials import load_creds
from controllers.grid_generator.helper_classes.time_converter import time_range_to_dict, convert_to_time
from datetime import datetime, time

from controllers.utils.URLs import URLs



#TODO: Document
def parse_availability(studentId):
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
            #Will Hold the entire dictionary for all the days and their available ranges
            dict = []

            #Get the Global Availability from Schedule Source API
            availJson = api.get_global_availability(studentId)

            #Parsing one day at a time
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


#TODO: Document
def parse_availability_for_one_day(availStr):
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


