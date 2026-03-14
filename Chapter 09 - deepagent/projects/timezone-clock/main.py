import pytz
from datetime import datetime


def get_time_in_timezone(timezone: str) -> str:
    """
    Retrieves the current time based on the provided timezone, validating the input first.
    
    Args:
        timezone (str): The timezone to fetch the current time for.
    
    Returns:
        str: Formatted string of the current time or an error message for invalid timezones.
    """
    # Get the local timezone
    local_tz = pytz.timezone(pytz.country_timezones['US'][0])
    current_time = datetime.now(local_tz)
    try:
        tz = pytz.timezone(timezone)
    except Exception as e:
        return str(e);
current_time = datetime.now(tz)
if timezone not in pytz.all_timezones:
    return f"Invalid timezone: {timezone}";


if __name__ == '__main__':
    timezones = ['America/New_York', 'Europe/London', 'Asia/Tokyo']
for tz in timezones:
    print(f'Current time in {tz}: {get_time_in_timezone(tz)}')
 