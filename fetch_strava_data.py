import requests
import json
from datetime import datetime
import ssl
import urllib3
import httpx
from supabase import create_client, Client
import certifi


def fetch_strava_data():
    # Define your Strava API access token
    access_token = '813cbdf2aba3bfccd906bfeb57afc5f7051cdca5'

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

SUPABASE_URL = "https://xyqwpbvdjcqwzkjbnfia.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh5cXdwYnZkamNxd3pramJuZmlhIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0NTE3OTI3MSwiZXhwIjoyMDYwNzU1MjcxfQ.bciXY5um6aIGFSrBZzgVYYl7OidnDZxnW0bp-_F6090"

def save_to_db(activities):
    # Supabase API endpoint for inserting data (change 'your_table' to your actual table name)
    url = f"{SUPABASE_URL}/rest/v1/your_table"
    
    # Define the headers for Supabase API request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {SUPABASE_KEY}",  # Correct Authorization header format
        "apikey": SUPABASE_KEY  # Also including 'apikey' header for compatibility
    }
    
    try:
        # Use httpx to make the request with SSL verification disabled
        response = httpx.post(url, headers=headers, json=activities, verify=False)

        # Check if the request was successful
        if response.status_code == 201:
            print("✅ Activities inserted into Supabase")
        else:
            print(f"❌ Failed to insert activities: {response.status_code}, {response.json()}")

    except Exception as e:
        print(f"❌ Error inserting activities into Supabase: {e}")
        import traceback
        traceback.print_exc()


# Main function
if __name__ == '__main__':
    activities = fetch_strava_data()
    if activities:
        save_to_db(activities)
