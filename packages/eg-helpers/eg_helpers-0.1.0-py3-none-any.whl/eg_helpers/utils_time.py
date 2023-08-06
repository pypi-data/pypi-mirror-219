#File: utils_time.py
import datetime
from utils_debug import debugging_prints
import pytz
import regex as re

debug_level = 2

def dprint(msg, level=2, log_timestamps=True, *args):
    debugging_prints(msg, level, debug_level, log_timestamps, *args)
    

def get_current_cet_datetime(mode="object"):
    '''
    Returns the current date and time in the CET timezone.
    
    Parameters:
    mode (str): "object" or "string"
    
    Returns:
    datetime.datetime/str: Current CET date and time as a datetime object (if mode=="object") or as a string (if mode=="string").
    '''
    if mode=="object":
        return datetime.datetime.now(pytz.timezone('CET'))
    elif mode=="string":
        return datetime.datetime.now(pytz.timezone('CET')).strftime("%Y-%m-%d %H:%M")
    

def create_cet_datetime(val):
    '''
    Converts a string datetime into a datetime object and localizes it to the CET timezone.
    
    Parameters:
    val (str): The datetime string in the format "%Y-%m-%d %H:%M".
    
    Returns:
    datetime.datetime: The localized CET datetime object.
    '''
    temp_datetime = datetime.datetime.strptime(val, "%Y-%m-%d %H:%M")
    return pytz.timezone('CET').localize(temp_datetime)


def check_time_difference_to_now(timestamp, mode="days"):
    '''
    Checks the difference between the current time and a provided timestamp.
    
    Parameters:
    timestamp (str): A timestamp as a string in the format "%Y-%m-%d %H:%M".
    mode (str): The unit of time to return the difference in. Options: "days", "hours", "minutes", "seconds".
    
    Returns:
    int: The difference between the current time and the timestamp in the specified mode.
    '''

    # Convert the timestamp to a datetime object using the helper function
    datetime_obj = create_cet_datetime(timestamp)

    # Get the current datetime using the helper function
    current_datetime = get_current_cet_datetime(mode="object")

    # Calculate the time difference
    time_difference = current_datetime - datetime_obj

    # Return the time difference based on the specified mode
    if mode == "days":
        return time_difference.days
    elif mode == "hours":
        return int(time_difference.total_seconds() / 3600)
    elif mode == "minutes":
        return int(time_difference.total_seconds() / 60)
    elif mode == "seconds":
        return int(time_difference.total_seconds())
    else:
        raise ValueError("Invalid mode. Please choose one of the following: 'days', 'hours', 'minutes', 'seconds'.")




def create_timedelta(num, unit):
    '''
    Creates a timedelta object for the given number of time units.
    
    Parameters:
    num (int): The number of time units.
    unit (str): The type of time unit. Could be "min", "h", "sec", "day", "week", "month", or "year".
    
    Returns:
    datetime.timedelta: The timedelta object representing the number of time units.
    '''
    if unit.startswith("min"):
        return datetime.timedelta(minutes=num)
    elif unit.startswith("h") or unit == "hour" or unit == "hours":
        return datetime.timedelta(hours=num)
    elif unit.startswith("sec"):
        return datetime.timedelta(seconds=num)
    elif unit.startswith("day"):
        return datetime.timedelta(days=num)
    elif unit.startswith("week"):
        return datetime.timedelta(weeks=num)
    elif unit.startswith("month"):
        return datetime.timedelta(days=num*30)
    elif unit.startswith("year"):
        return datetime.timedelta(days=num*365)

def apply_delta(delta):
    '''
    Subtracts a timedelta from the current CET datetime and returns the result.
    
    Parameters:
    delta (datetime.timedelta): The timedelta to subtract.
    
    Returns:
    datetime.datetime: The datetime after subtracting the delta.
    '''
    current_date = get_current_cet_datetime(mode="object")
    return current_date - delta


def reformat_date(date_str):
    '''
    Reformats date strings from various common human-readable formats into the format "%Y-%m-%d %H:%M".
    
    Parameters:
    date_str (str): The date string to reformat.
    
    Returns:
    str: The reformatted date in the format "%Y-%m-%d %H:%M" as a string.
    
    Raises:
    ValueError: If the date string does not match any expected format.
    '''
    try:
        dprint(f"Date string scraped that we're going to reformat: {date_str}",2)
        # Match patterns
        # Single time unit with the word "ago"
        # Examples: "3 hours ago", "5 days ago", "1 month ago"
        single_unit_match = re.match(r'^(\d+)\s+(minute|min\.?|second|hr\.?|hour|day|week|month|year)s? ago$', date_str)

        # Combined time units with the word "ago"
        # Examples: "2 hours 29 minutes ago", "1 day 3 hours ago", "1 month 15 days ago"
        combined_unit_match = re.match(r'^(\d+)\s+(min\.?|minute|second|hr\.?|hour|day|week|month|year)s? (\d+)\s+(min\.?|minute|second|hr\.?|hour|day|week|month|year)s? ago$', date_str)

        # Single time unit without the word "ago"
        # Examples: "3 min", "5 hr", "20 sec"
        single_unit_no_ago_match = re.match(r'^(\d+)\s+(min\.?|hr\.?|sec)s?$', date_str)

        # Date string starting with "Yesterday"
        # Example: "Yesterday at 14:30"
        yesterday_match = date_str.startswith("Yesterday")

        # Month day at time format
        # Examples: "June 25 at 12:30", "February 7 at 09:45"
        month_day_time_match = re.match(r'^\w+ \d+ at \d+:\d+$', date_str)

        # Month day, year at time format
        # Examples: "June 25, 2022 at 12:30", "February 7, 2023 at 09:45"
        month_day_year_time_match = re.match(r'^\w+ \d+, \d{4} at \d+:\d+$', date_str)


        if single_unit_match:
            match = single_unit_match
            num = int(match.group(1))
            unit = match.group(2)
            delta = create_timedelta(num, unit)
            date_obj = apply_delta(delta)

        elif combined_unit_match:
            match = combined_unit_match
            num = int(match.group(1))
            unit = match.group(2)
            num2 = int(match.group(3))
            unit2 = match.group(4)
            delta = create_timedelta(num, unit) + create_timedelta(num2, unit2)
            date_obj = apply_delta(delta)

        elif single_unit_no_ago_match:
            num = int(single_unit_no_ago_match.group(1))
            unit = single_unit_no_ago_match.group(2)
            delta = create_timedelta(num, unit)
            date_obj = apply_delta(delta)

        elif yesterday_match:
            time_str = date_str.replace("Yesterday at ", "")
            current_date = get_current_cet_datetime(mode="object")
            yesterday = current_date - datetime.timedelta(days=1)
            date_obj = datetime.datetime.strptime(time_str, "%H:%M")
            date_obj = date_obj.replace(year=yesterday.year, month=yesterday.month, day=yesterday.day)

        elif month_day_time_match:
            date_obj = datetime.datetime.strptime(date_str, "%B %d at %H:%M")
            current_year = get_current_cet_datetime(mode="object").year
            date_obj = date_obj.replace(year=current_year)

        elif month_day_year_time_match:
            date_obj = datetime.datetime.strptime(date_str, "%B %d, %Y at %H:%M")

        else:
            raise ValueError(f"Date string '{date_str}' does not match the expected formats.")

    except ValueError as e:
        dprint(f"Error in reformat_date: {e}",3)
        return None
    
    formatted_date_str = date_obj.strftime("%Y-%m-%d %H:%M")
    dprint(f"Formatted date string: {formatted_date_str}",1)
    return formatted_date_str


