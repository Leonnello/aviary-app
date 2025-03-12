import requests

FIREBASE_API_KEY = "AIzaSyA99h8EWDNa2nXD2LeBnYcloepLYM_vzIM"
ID_TOKEN = "your_user_id_token_here"  # Get this from registration response

url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={FIREBASE_API_KEY}"
payload = {
    "requestType": "VERIFY_EMAIL",
    "idToken": ID_TOKEN
}

response = requests.post(url, json=payload)
print(response.json())  # Check response for errors
