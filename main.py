import os
import json
import datetime

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the path to the config.json file
config_path = os.path.join(script_dir, "config.json")

# Read the config.json file and get the name to timezone mapping
with open(config_path, "r") as f:
    name_to_timezone = json.load(f)

# Initialize an empty string to store the output
output_str = "[ "

# Loop through the name to timezone mapping
for name, timezone in name_to_timezone.items():
    # Get the current UTC time
    utc_time = datetime.datetime.utcnow()

    # Convert UTC time to local time based on the timezone offset
    local_time = utc_time + datetime.timedelta(hours=int(timezone))

    # Format the local time
    formatted_time = local_time.strftime("%I:%M%p").lower()

    # Append to the output string
    output_str += f"{name}: {formatted_time}   "

output_str = output_str.strip()
output_str += " ]"
# Define the path to the output file
output_file_path = os.path.join(script_dir, "output.txt")

# Write the output string to the output file
with open(output_file_path, "w") as f:
    f.write(output_str)
