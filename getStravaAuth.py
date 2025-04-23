import requests

response = requests.post(
    'https://www.strava.com/oauth/token',
    data={
        'client_id': '156438',
        'client_secret': 'caf0082f47eb191f24e155e44bf9656467771054',
        'code': '680a953b927326643a9bb5554e938f2ba13c39bb',
        'grant_type': 'authorization_code'
    },
    verify=False  # again, only if needed
)

tokens = response.json()
print('New access token:', tokens)