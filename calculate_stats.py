"""
calculate_stats.py

Retrieves anime and manga statistics from MyAnimeList and
returns the values displayed on the Discord widget.
"""


from mal_api import get_profile_statistics, get_all_manga


def calculate_stats():
    # Retrieve official anime statistics directly from the user's profile.
    anime_stats = get_profile_statistics()

    # Get manga list
    manga = get_all_manga()

    # =========================
    # Manga statistics
    # =========================

    manga_completed = 0
    chapters_read = 0
    volumes_read = 0

    for entry in manga:
        status = entry["list_status"]["status"]

        if status == "completed":
            manga_completed += 1

        chapters_read += entry["list_status"]["num_chapters_read"]
        volumes_read += entry["list_status"]["num_volumes_read"]

    return {
        "anime_completed": anime_stats["num_items_completed"],
        "days_watched": round(anime_stats["num_days"], 1),
        "mean_score": round(anime_stats["mean_score"], 1),
        "manga_completed": manga_completed,
        "chapters_read": chapters_read,
        "volumes_read": volumes_read
    }


if __name__ == "__main__":
    stats = calculate_stats()

    print("\nCalculated statistics:\n")

    for key, value in stats.items():
        print(f"{key}: {value}")
