from datetime import datetime
#Converts a string representing a time value and converts it to a programmable datetime.time() object
#Param: time_str - the time value in string format (e.g "12:00:00 AM" or "1900-05-10T13:00:00")
#Returns the same time, but as an instance datetime.time()
def convert_to_time(time_str):
    try:
        if "T" in time_str:  # Check if input is in "YYYY-MM-DDTHH:MM:SS" format
            datetime_obj = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S")
        else:  # Assuming the default format is "%I:%M:%S %p"
            datetime_obj = datetime.strptime(time_str, "%I:%M:%S %p")
        return datetime_obj.time()
    except ValueError:
        return None


print(convert_to_time("4:00:00 PM"))
