import requests
import json
import os
from datetime import datetime


def fetch_strava_data():
    # Define your Strava API access token
    access_token = '0a97268e9a62e1d9c8da012e1d9e1a9241d69f96'

    # Strava API endpoint for fetching activities
    url = 'https://www.strava.com/api/v3/athlete/activities'

    # Define headers with authorization
    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    # Parameters for API call
    params = {
        'per_page': 200,  # Number of records per page (maximum is 200)
        'page': 1,        # Page number
    }

    try:
        # Disabling SSL verification for testing purposes
        response = requests.get(url, headers=headers, params=params, verify=False)
        response.raise_for_status()

        activities = response.json()
        print(f"Fetched {len(activities)} activities.")
        all_keys = set()
        for item in activities:
            all_keys.update(item.keys())

        # Make sure all objects have the same keys
        for item in activities:
            for key in all_keys:
                item.setdefault(key, None)  # Add missing keys with value None

        return activities

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Strava: {e}")
        return None

# Main function
if __name__ == '__main__':
    os.makedirs('StravaDashboard/output', exist_ok=True)
    activities = fetch_strava_data()
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    with open(f"StravaDashboard/output/{timestamp}_StravaActivities.json", "w") as f:
        json.dump(activities, f, indent=2)
