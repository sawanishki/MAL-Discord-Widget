import os
import requests

from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("MAL_CLIENT_ID")
CLIENT_SECRET = os.getenv("MAL_CLIENT_SECRET")

with open("code_verifier.txt") as f:
    code_verifier = f.read().strip()

authorization_code = input("Paste authorization code: ")

response = requests.post(
    "https://myanimelist.net/v1/oauth2/token",
    data={
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": authorization_code,
        "code_verifier": code_verifier,
        "grant_type": "authorization_code",
        "redirect_uri": "http://localhost:8000/callback"
    }
)

print(response.status_code)
print(response.text)
