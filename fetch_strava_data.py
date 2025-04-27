import requests
import webbrowser
import json
import datetime
import os
import time

TOKEN_FILE = "strava_tokens.json"

def load_tokens():
    with open(TOKEN_FILE, "r") as f:
        return json.load(f)

def save_tokens(tokens):
    with open(TOKEN_FILE, "w") as f:
        json.dump(tokens, f, indent=4)

def refresh_access_token(tokens):
    print("Access Token expired, refreshing...")
    response = requests.post("https://www.strava.com/oauth/token", data={
        "client_id": tokens["client_id"],
        "client_secret": tokens["client_secret"],
        "grant_type": "refresh_token",
        "refresh_token": tokens["refresh_token"]
    })

    if response.status_code != 200:
        raise Exception(f"Token Refresh Failed: {response.text}")

    new_data = response.json()
    tokens["access_token"] = new_data["access_token"]
    tokens["refresh_token"] = new_data["refresh_token"]
    tokens["expires_at"] = new_data["expires_at"]

    save_tokens(tokens)
    return tokens

def get_valid_token():
    tokens = load_tokens()
    now = int(time.time())

    if now >= tokens["expires_at"]:
        tokens = refresh_access_token(tokens)
    else:
        print("Access Token still valid.")

    return tokens["access_token"]

def getAllActivities(headers):
    params = {
    'per_page': 200,
    'page': 1
    }
    getAllActivities_url = 'https://www.strava.com/api/v3/athlete/activities'
    
    activity_response = requests.get(getAllActivities_url, headers=headers, params=params)
    if activity_response.status_code == 200:
        activities = activity_response.json()
        print(f"Fetched {len(activities)} activities.")

        # Save to file
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        os.makedirs("StravaDashboard/output", exist_ok=True)
        filename = f"StravaDashboard/output/{timestamp}_allActivities.json"
        with open(filename, "w") as f:
            json.dump(activities, f, indent=2)
        print(f"📁 Activities saved to {filename}")
    else:
        print("Error fetching activities:", activity_response.text)
        
def getSingleActivity(headers, activityId):
    getSingleActivity_url = f'https://www.strava.com/api/v3/activities/{activityId}/streams?keys=time,distance,latlng,altitude,velocity_smooth,heartrate,cadence,watts,temp,moving,grade_smooth&key_by_type=true'
    print(getSingleActivity_url)
    
    activity_response = requests.get(getSingleActivity_url, headers=headers)
    if activity_response.status_code == 200:
        activities = activity_response.json()
        print(f"Fetched {activities} activities.")

        # Save to file
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        os.makedirs("StravaDashboard/output", exist_ok=True)
        filename = f"StravaDashboard/output/{timestamp}_activity_{activityId}.json"
        with open(filename, "w") as f:
            json.dump(activities, f, indent=2)
        print(f"📁 Activities saved to {filename}")
    else:
        print("Error fetching activities:", activity_response.text)



# Beispielnutzung:
if __name__ == "__main__":
    token = get_valid_token()
    print("Aktueller Access Token:", token)

    # Step 4: Fetch activities
    headers = {
        'Authorization': f'Bearer {token}'
    }
    getAllActivities(headers)
    activityId = '14265996018'
    getSingleActivity(headers, activityId)