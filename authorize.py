"""
authorize.py

Generates a PKCE code verifier and opens the MyAnimeList
authorization page in the user's default web browser.

Run this script only once during the initial setup.
"""


import secrets
import urllib.parse
import webbrowser
import os

from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("MAL_CLIENT_ID")

# MAL uses plain PKCE
code_verifier = secrets.token_urlsafe(64)

with open("code_verifier.txt", "w") as f:
    f.write(code_verifier)

params = {
    "response_type": "code",
    "client_id": CLIENT_ID,
    "redirect_uri": "http://localhost:8000/callback",
    "code_challenge": code_verifier,
    "state": secrets.token_urlsafe(16)
}

url = (
    "https://myanimelist.net/v1/oauth2/authorize?"
    + urllib.parse.urlencode(params)
)

print("Opening browser...")
webbrowser.open(url)

print("\nIf it doesn't open:")
print(url)

print("\nAfter authorizing, copy ONLY the code= parameter from the URL.")
