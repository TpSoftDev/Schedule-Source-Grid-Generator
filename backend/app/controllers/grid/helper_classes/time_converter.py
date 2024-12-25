"""
This file contains utility functions for parsing and converting time-related strings into usable Python `datetime.time` objects. These utilities are designed to handle various formats of time inputs and transform them into structured time ranges for further processing.

Overview:
- **`convert_to_time`:** Converts a string representation of a time (e.g., "8am", "12:30pm") into a `datetime.time` object. Handles cases with missing minutes and edge cases like "midnight" or "latenight."
- **`time_range_to_dict`:** Parses a time range string (e.g., "8am-3pm") and converts it into a dictionary with `start_time` and `end_time` keys, where the values are `datetime.time` objects.

Dependencies:
- Python's `datetime` module for parsing and working with time.

Key Functions:
1. `convert_to_time(time_str, indicator)`:
2. `time_range_to_dict(time_range_str)`:

Usage:
- These utilities are intended to preprocess time-related input strings and convert them into structured Python objects for further processing.

"""
from datetime import datetime


def convert_to_time(time_str, indicator):
    """
    converts the string value of a time into a datetime.time object.


    Parameters:
        time_str (str):
            The string representation of the time, e.g., "8am", "12:30pm", or "11:59pm".
            If the string is empty or invalid, the `indicator` determines the fallback value.
        indicator (int):
            Determines the fallback time when `time_str` is not provided:
            - `-1`: Returns midnight (`00:00`).
            - `1`: Returns the last possible minute of the day (`23:59`).

    Returns:
        datetime.time:
            A `datetime.time` object representing the parsed time from the string, or
            a fallback value (`00:00` or `23:59`) if the string is empty.

        """
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


def time_range_to_dict(time_range_str):
    """
    Converts a time range string into a dictionary with structured start and end times.

    This function takes a string representation of a time range (e.g., "8am-3pm") and
    parses it into a dictionary containing `start_time` and `end_time` as `datetime.time` objects.
    The `convert_to_time` function is used to parse each individual time within the range.

    Parameters:
        time_range_str (str):
            The string representation of the time range, e.g., "8am-3pm".
            The format should consist of two times separated by a dash ("-"), with optional spaces.

    Returns:
        dict:
            A dictionary containing:
            - `'start_time'`: A `datetime.time` object representing the start of the range.
            - `'end_time'`: A `datetime.time` object representing the end of the range.


        None: (if an exception is raised).
            If an error occurs during parsing, the function logs the error and returns `None`.

    Exceptions:
        - This function catches and logs exceptions such as:
            - `ValueError` if the input string format is incorrect or invalid.
            - `IndexError` if the input string does not contain both start and end times.
    """

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


