import sys
import os
import tweepy
from lib import users_to_file, initialize_tweepy

if len(sys.argv) < 2:
    print("Please provide the Twitter username")
    sys.exit(1)

_, username = sys.argv

out_dir = "data/followers"
os.makedirs(out_dir, exist_ok=True)
out_file = "{}/{}".format(out_dir, username)


api = initialize_tweepy()

user = api.get_user(screen_name=username)

followers = []
try:
    for page in tweepy.Cursor(api.get_followers, user_id=user.id, count=200).pages():
        followers.extend(page)
        print("Number of followers downloaded: {}".format(len(followers)))
        users_to_file(followers, out_file)
except tweepy.TweepyException as e:
    print("Error during download:")
    print(e)

users_to_file(followers, out_file)
