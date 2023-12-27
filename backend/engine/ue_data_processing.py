import random
import json

def ue_data(durations):
    # Camera types
    camera_types = ['ecu', 'cu', 'm', 'w', 't', 'f', 'ots', 'rm', 'lm']

    # Generate JSON data with random camera types
    json_data = []
    for duration in durations:
        random_camera_type = random.choice(camera_types)
        data = {"total_duration": duration, "camera_type": random_camera_type}
        json_data.append(data)

    # Convert the JSON data to a string with "@" as the delimiter
    json_string = "@".join(json.dumps(item) for item in json_data)

    return json_string
