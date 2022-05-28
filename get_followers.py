import sys
import os
from lib import users_to_file, initialize_tweepy, get_followers

if len(sys.argv) < 2:
    print("Please provide the Twitter username")
    sys.exit(1)

_, username = sys.argv

out_dir = "data/followers"
os.makedirs(out_dir, exist_ok=True)
out_file = "{}/{}".format(out_dir, username)

api = initialize_tweepy()
followers = get_followers(api, username, out_file)
users_to_file(followers, out_file)
