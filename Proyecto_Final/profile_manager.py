import json
import os

PROFILE_FILE = "current_profile.json"

def save_current_profile(profile_name):
    with open(PROFILE_FILE, 'w') as file:
        json.dump({"current_profile": profile_name}, file)

def get_current_profile():
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, 'r') as file:
            data = json.load(file)
            return data.get("current_profile")
    return None


current_profile = get_current_profile()