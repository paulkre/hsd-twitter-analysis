import tweepy
import pandas as pd


def users_to_file(users: list[tweepy.User], filename="users"):
    data = {
        "id": [data.id for data in users],
        "id_str": [data.id_str for data in users],
        "name": [data.name for data in users],
        "screen_name": [data.screen_name for data in users],
        "location": [data.location for data in users],
        "description": [data.description for data in users],
        "url": [data.url for data in users],
        "protected": [data.protected for data in users],
        "followers_count": [data.followers_count for data in users],
        "friends_count": [data.friends_count for data in users],
        "listed_count": [data.listed_count for data in users],
        "created_at": [data.created_at for data in users],
        "favourites_count": [data.favourites_count for data in users],
        "verified": [data.verified for data in users],
        "statuses_count": [data.statuses_count for data in users],
        "has_extended_profile": [data.has_extended_profile for data in users],
        "default_profile": [data.default_profile for data in users],
        "default_profile_image": [data.default_profile_image for data in users],
        "withheld_in_countries": [",".join(data.withheld_in_countries) for data in users]
    }

    df = pd.DataFrame(data, columns=data.keys())
    df.to_csv("{}.csv".format(filename))
    df.to_json("{}.json".format(filename))
