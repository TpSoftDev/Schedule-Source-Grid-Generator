from datetime import datetime

#TODO: Document
def convert_to_time(time_str, indicator):
    if not time_str:
        if indicator == -1:
            midnight = datetime.strptime("00:00", "%H:%M")
            midnight_time = midnight.time()
            return midnight_time

        elif indicator == 1:
            latenight = datetime.strptime("23:59", "%H:%M")
            latenight_time = latenight.time()
            return latenight_time

    # Handle cases where the input time_str may have missing minutes (e.g., "8am")
    if len(time_str) == 4:  # For time strings like "8am" or "12am"
        time_str = time_str[:2] + ":00" + time_str[2:]

    # Convert the string to datetime object using strptime
    try:
        # Parse the time string in 12-hour format and convert to datetime object in 24-hour format
        time_obj = datetime.strptime(time_str, "%I:%M%p")
        time_obj_time = time_obj.time()
    except ValueError:
        # Handle the case where no minutes were provided, e.g., "8am"
        time_obj = datetime.strptime(time_str, "%I%p")
        time_obj_time = time_obj.time()


    return time_obj_time




#TODO: Document
def time_range_to_dict(time_range_str):

    try:
        # Remove any spaces
        time_range_str = time_range_str.strip()
        start_to_end_str = time_range_str.split("-")
        start = convert_to_time(start_to_end_str[0], -1)
        end = convert_to_time(start_to_end_str[1], 1)

        return {
            'start_time': start,
            'end_time': end
        }

    except Exception as e:
        print("ERROR OCCURRED WHILE CONVERTING STRING TO TIMES: ", e)
        return None


