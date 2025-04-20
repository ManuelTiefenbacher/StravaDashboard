import requests
import json
from datetime import datetime
import psycopg2


def fetch_strava_data():

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
        print(f"Fetched {len(activities)} activities.")
        return activities

        # You can choose to format and store this in a JSON or CSV file
        #with open('strava_activities.json', 'w') as f:
        #    json.dump(activities, f, indent=4)

    else:
        print(f"Error: {response.status_code} - {response.text}")


def save_to_db(activities):
    USER = "postgres"
    PASSWORD = "123456789Aaasrfg"
    HOST = "db.xyqwpbvdjcqwzkjbnfia.supabase.co"
    PORT = "5432"
    DBNAME = "postgres"

    try:
        connection = psycopg2.connect("postgresql://postgres:123456789Aaasrfg@db.xyqwpbvdjcqwzkjbnfia.supabase.co:5432/postgres")
        print("✅ Connected to the database")

        cursor = connection.cursor()

        # Insert activities into the database
        for act in activities:
            cursor.execute("""
                INSERT INTO activities (id, name, distance, moving_time, type, start_date)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
            """, (
                act["id"],
                act["name"],
                act["distance"],
                act["moving_time"],
                act["type"],
                act["start_date"]
            ))

        connection.commit()
        print("✅ Activities inserted")

        cursor.close()
        connection.close()
        print("🔒 Connection closed")

    except psycopg2.OperationalError as e:
        print(f"❌ OperationalError: {e}")
        import traceback
        traceback.print_exc()


# Main function
if __name__ == '__main__':
    activities = fetch_strava_data()
    if activities:
        save_to_db(activities)