import requests
import json

# Define your Strava API access token
access_token = '813cbdf2aba3bfccd906bfeb57afc5f7051cdca5'

# Strava API endpoint for fetching activities
url = 'https://www.strava.com/api/v3/athlete/activities'

# Define headers with authorization
headers = {
    'Authorization': f'Bearer {access_token}',
}

# Parameters for API call (optional: adjust per your needs)
params = {
    'per_page': 200,  # Number of records per page (maximum is 200)
    'page': 1,        # Page number
}

# Fetch data from Strava API with SSL verification disabled
response = requests.get(url, headers=headers, params=params, verify=False)

if response.status_code == 200:
    # Successfully fetched activities, save to a file
    activities = response.json()

    # You can choose to format and store this in a JSON or CSV file
    with open('strava_activities.json', 'w') as f:
        json.dump(activities, f, indent=4)

    print(f"Fetched {len(activities)} activities.")
else:
    print(f"Error: {response.status_code} - {response.text}")
