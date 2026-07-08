"""
mal_api.py

Handles communication with the official MyAnimeList API,
including OAuth authentication, token refreshing,
profile statistics, and paginated list retrieval.
"""


import json
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("MAL_CLIENT_ID")
CLIENT_SECRET = os.getenv("MAL_CLIENT_SECRET")


def load_tokens():
    with open("tokens.json", "r") as f:
        return json.load(f)


def save_tokens(tokens):
    with open("tokens.json", "w") as f:
        json.dump(tokens, f, indent=4)


def refresh_access_token():
    """
    Refresh the OAuth access token if it has expired.

    Returns:
        str: A valid access token.
    """
    tokens = load_tokens()

    print("Refreshing MAL access token...")

    response = requests.post(
        "https://myanimelist.net/v1/oauth2/token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": tokens["refresh_token"],
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        },
        timeout=15
    )

    response.raise_for_status()

    new_tokens = response.json()

    # Keep the refresh token if MAL doesn't send a new one
    if "refresh_token" not in new_tokens:
        new_tokens["refresh_token"] = tokens["refresh_token"]

    # Store the exact expiry timestamp
    new_tokens["expires_at"] = int(time.time()) + new_tokens["expires_in"] - 60

    save_tokens(new_tokens)

    return new_tokens["access_token"]


def get_access_token():
    tokens = load_tokens()

    # If the access token is still valid, use it
    if (
        "expires_at" in tokens
        and time.time() < tokens["expires_at"]
        and "access_token" in tokens
    ):
        return tokens["access_token"]

    # Otherwise refresh it
    return refresh_access_token()


def get_profile_statistics():
    access_token = get_access_token()

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(
        "https://api.myanimelist.net/v2/users/@me?fields=anime_statistics",
        headers=headers,
        timeout=20
    )

    response.raise_for_status()

    return response.json()["anime_statistics"]

def get_all_anime():
    """
    Retrieve the authenticated user's complete anime list.

    Returns:
        list: All anime entries, including NSFW titles.
    """
    access_token = get_access_token()

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    url = (
        "https://api.myanimelist.net/v2/users/@me/animelist"
        "?limit=100&fields=list_status&nsfw=true"
    )

    anime = []

    page = 1

    while url:
        print(f"\nDownloading anime page {page}")
        print(url)

        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        data = response.json()

        print(f"Received {len(data['data'])} entries")

        anime.extend(data["data"])

        url = data.get("paging", {}).get("next")
        page += 1

    print(f"\nTotal anime downloaded: {len(anime)}")

    return anime


def get_all_manga():
    access_token = get_access_token()

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    url = (
        "https://api.myanimelist.net/v2/users/@me/mangalist"
        "?limit=100&fields=list_status&nsfw=true"
    )

    manga = []

    page = 1

    while url:
        print(f"\nDownloading manga page {page}")
        print(url)

        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        data = response.json()

        print(f"Received {len(data['data'])} entries")

        manga.extend(data["data"])

        url = data.get("paging", {}).get("next")
        page += 1

    print(f"\nTotal manga downloaded: {len(manga)}")

    return manga
