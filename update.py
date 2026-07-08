"""
update.py

Main entry point for the project.

Calculates the latest MyAnimeList statistics and
updates the configured Discord Profile Widget.
"""


import os
import json
import requests
from dotenv import load_dotenv

from calculate_stats import calculate_stats

load_dotenv()

APPLICATION_ID = os.getenv("APPLICATION_ID")
BOT_TOKEN = os.getenv("BOT_TOKEN")
USER_ID = os.getenv("USER_ID")


def update():
    try:
        stats = calculate_stats()
    except Exception as e:
        print("Failed to calculate MAL stats:")
        print(e)
        return

    print("Calculated MAL Stats:")
    print(stats)

    jsonString = {
        "data": {
            "dynamic": [
                {
                    "type": 1,
                    "name": "animecompleted",
                    "value": str(stats["anime_completed"])
                },
                {
                    "type": 1,
                    "name": "dayswatched",
                    "value": str(stats["days_watched"])
                },
                {
                    "type": 1,
                    "name": "meanscore",
                    "value": str(stats["mean_score"])
                },
                {
                    "type": 1,
                    "name": "mangacompleted",
                    "value": str(stats["manga_completed"])
                },
                {
                    "type": 1,
                    "name": "chaptersread",
                    "value": str(stats["chapters_read"])
                },
                {
                    "type": 1,
                    "name": "volumesread",
                    "value": str(stats["volumes_read"])
                }
            ]
        }
    }

    print("\nSending to Discord:")
    print(json.dumps(jsonString, indent=4))

    response = requests.patch(
        url=f"https://discord.com/api/v9/applications/{APPLICATION_ID}/users/{USER_ID}/identities/0/profile",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bot {BOT_TOKEN}",
            "User-Agent": "DiscordBot"
        },
        data=json.dumps(jsonString)
    )

    print(f"\nDiscord response: {response.status_code}")

    if response.status_code != 204:
        print(response.text)


if __name__ == "__main__":
    update()
