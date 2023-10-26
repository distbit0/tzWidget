import os
import json
import datetime


def get_local_utc_offset():
    """Calculate local UTC offset in hours."""
    local_time = datetime.datetime.now()
    utc_time = datetime.datetime.utcnow()
    delta = local_time - utc_time
    return round(delta.total_seconds() / 3600)


def format_time_difference(time_difference):
    """
    Format time difference to consider days if abs(time_difference) > 12.

    Args:
        time_difference (int): The time difference in hours.

    Returns:
        str: Formatted time difference.
    """
    # Determine the sign based on the value of time_difference
    sign = "+" if time_difference >= 0 else "-"

    # Use abs_time_difference for calculating days and remaining_hours
    abs_time_difference = abs(time_difference)

    if abs_time_difference > 12:
        # Calculate days and remaining_hours based on the absolute value
        days = abs_time_difference // 24
        remaining_hours = abs_time_difference % 24

        # Correct remaining_hours for negative time differences
        if time_difference < 0:
            remaining_hours = 24 - remaining_hours if remaining_hours != 0 else 0
            days = days + 1 if remaining_hours != 0 else days

        return f"{sign}{days}d+{remaining_hours}"
    else:
        return f"{sign}{abs_time_difference}"


# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the path to the config.json file
config_path = os.path.join(script_dir, "config.json")

# Read the config.json file and get the name to timezone mapping
with open(config_path, "r") as f:
    name_to_timezone = json.load(f)

# Automatically determine your timezone offset
your_timezone_offset = get_local_utc_offset()

# Initialize an empty string to store the output
output_str = "     "

# Loop through the name to timezone mapping
for name, timezone in name_to_timezone.items():
    # Calculate the time difference between your timezone and the person's timezone
    time_difference = format_time_difference(int(timezone) - your_timezone_offset)

    # Get the current UTC time
    utc_time = datetime.datetime.utcnow()

    # Convert UTC time to local time based on the timezone offset
    local_time = utc_time + datetime.timedelta(hours=int(timezone))

    # Format the local time as decimal hours
    hour = local_time.hour % 12
    minute = local_time.minute
    minute_decimal = minute / 60
    time_decimal = hour + int(minute_decimal * 10) / 10
    am_pm = "am" if local_time.hour < 12 else "pm"

    # Append to the output string
    output_str += f"{name}{time_difference}: {time_decimal}{am_pm}   "

output_str = output_str.strip()

# Define the path to the output file
output_file_path = os.path.join(script_dir, "output.txt")

# Write the output string to the output file
with open(output_file_path, "w") as f:
    f.write(output_str)
