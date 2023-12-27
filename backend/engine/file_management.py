import os
from django.conf import settings
import json
import shutil

def remove_directory(directory_path):
    try:
        shutil.rmtree(directory_path)
        print(f"Directory {directory_path} and its contents have been successfully removed.")
    except Exception as e:
        print(f"Error while removing directory {directory_path}: {str(e)}")


def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_static_file_path(filename):
    return os.path.join(settings.STATICFILES_DIRS[0], filename)

def save_json_file(file_path, json_data):
    with open(file_path, 'w') as json_file:
    # Use json.dump() to write the data to the file
        json.dump(json_data, json_file, indent=2)

def save_txt_file(file_path, txt_data):
    with open(file_path, 'w') as file:
        file.write(txt_data)