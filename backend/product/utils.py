from datetime import datetime
import pytz

def convert_utc_to_ist(utc_time):
    """Convert a UTC datetime object to IST (Indian Standard Time) and return a formatted string."""
    if not utc_time:
        return None

    ist_timezone = pytz.timezone("Asia/Kolkata")
    ist_time = utc_time.astimezone(ist_timezone)
    
    return ist_time.strftime("%d-%m-%Y %H:%M:%S IST")
