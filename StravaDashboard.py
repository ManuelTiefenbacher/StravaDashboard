import requests

client_id = '156438'
client_secret = '33fed3b9bce5d91e10f51d878b90f9247c723c9e'
code = 'http://localhost/exchange_token?state=&code=306213231b7f277ef42858c8f705a5bcd42bca96&scope=read,activity:read_all'

response = requests.post(
    "https://www.strava.com/api/v3/oauth/token",
    data={
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'grant_type': 'authorization_code'
    }
)

tokens = response.json()

# Check if access token is returned
if 'access_token' in tokens:
    print("Access Token:", tokens['access_token'])
    print("Refresh Token:", tokens['refresh_token'])
else:
    print("Error:", tokens)