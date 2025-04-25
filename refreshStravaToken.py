import requests
import webbrowser
import json

# === DEINE DATEN HIER EINTRAGEN ===
CLIENT_ID = '156438'
CLIENT_SECRET = 'caf0082f47eb191f24e155e44bf9656467771054'
REDIRECT_URI = 'http://localhost/exchange_token'

SCOPES = 'read,activity:read_all'
TOKEN_FILE = 'strava_tokens.json'

# === 1. Autorisierungs-URL bauen ===
auth_url = (
    f"https://www.strava.com/oauth/authorize?"
    f"client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}"
    f"&approval_prompt=force&scope={SCOPES}"
)

print("Öffne Strava zur Autorisierung...")
webbrowser.open(auth_url)

# === 2. Nutzer-Code abfragen ===
code = input("\n🔑 Füge den 'code' aus der URL ein (nach ?code=...):\n> ").strip()

# === 3. Token anfordern ===
print("📡 Tausche Code gegen Access Token...")
response = requests.post("https://www.strava.com/oauth/token", data={
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "code": code,
    "grant_type": "authorization_code"
})

if response.status_code != 200:
    print("❌ Fehler beim Token-Abruf:")
    print(response.text)
    exit()

data = response.json()
tokens = {
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "refresh_token": data["refresh_token"],
    "access_token": data["access_token"],
    "expires_at": data["expires_at"]
}

with open(TOKEN_FILE, "w") as f:
    json.dump(tokens, f, indent=4)

print("✅ Tokens gespeichert in", TOKEN_FILE)
print("🔁 Du kannst jetzt dein `fetch_strava_data.py` verwenden.")
