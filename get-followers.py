import sys
import os
import tweepy
import pandas as pd

from dotenv import load_dotenv
load_dotenv()

if len(sys.argv) < 2:
    print("Please provide the Twitter username")
    sys.exit(1)

_, username = sys.argv

out_dir = "data/followers"
os.makedirs(out_dir, exist_ok=True)

auth = tweepy.OAuth1UserHandler(
    os.getenv("TWITTER_CONSUMER_KEY"),
    os.getenv("TWITTER_CONSUMER_SECRET"),
    os.getenv("TWITTER_ACCESS_KEY"),
    os.getenv("TWITTER_ACCESS_SECRET"),
)

api = tweepy.API(auth, wait_on_rate_limit=True)

user = api.get_user(screen_name=username)


def export_data(followers):
    data = {
        "id": [data.id for data in followers],
        "id_str": [data.id_str for data in followers],
        "name": [data.name for data in followers],
        "screen_name": [data.screen_name for data in followers],
        "location": [data.location for data in followers],
        "description": [data.description for data in followers],
        "url": [data.url for data in followers],
        "protected": [data.protected for data in followers],
        "followers_count": [data.followers_count for data in followers],
        "friends_count": [data.friends_count for data in followers],
        "listed_count": [data.listed_count for data in followers],
        "created_at": [data.created_at for data in followers],
        "favourites_count": [data.favourites_count for data in followers],
        "verified": [data.verified for data in followers],
        "statuses_count": [data.statuses_count for data in followers],
        "has_extended_profile": [data.has_extended_profile for data in followers],
        "default_profile": [data.default_profile for data in followers],
        "default_profile_image": [data.default_profile_image for data in followers],
        "withheld_in_countries": [",".join(data.withheld_in_countries) for data in followers]
    }

    df = pd.DataFrame(data, columns=data.keys())
    df.to_csv("{}/{}.csv".format(out_dir, username))
    df.to_json("{}/{}.json".format(out_dir, username))


followers = []
try:
    for page in tweepy.Cursor(api.get_followers, user_id=user.id, count=200).pages():
        followers.extend(page)
        print("Number of followers downloaded: {}".format(len(followers)))
        export_data(followers)
except tweepy.TweepyException as e:
    print("Error during download:")
    print(e)

export_data(followers)
