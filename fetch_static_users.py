import os
from lib import users_to_file, initialize_tweepy

out_dir = "data"
os.makedirs(out_dir, exist_ok=True)

api = initialize_tweepy()
users = []

for screen_name in [
    "HSNiederrhein",
    "HochschuleBO",
    "RWTH",
    "fh_dortmund",
    "fh_muenster",
    "hsduesseldorf",
    "hsrheinwaal",
    "th_koeln"
]:
    users.append(api.get_user(screen_name=screen_name))
    print('> User "{}" downloaded'.format(screen_name))

users_to_file(users, "{}/static_users".format(out_dir))
