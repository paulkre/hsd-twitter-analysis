import sys
import os
from hashlib import md5
import pandas as pd
from lib import users_to_file, initialize_tweepy, get_followers

if len(sys.argv) < 2:
    print("Please provide the name of the CSV file containing the target followers")
    sys.exit(1)

in_file = sys.argv[1]
start_index = 0 if len(sys.argv) < 3 else int(sys.argv[2])

out_dir = "data/followers"
cache_dir = "{}/cache/{}".format(
    out_dir,
    str(md5(in_file.encode("utf-8")).hexdigest())[:6],
)
os.makedirs(cache_dir, exist_ok=True)

df = pd.read_csv(in_file)
df = df.iloc[start_index:len(df.index)]

api = initialize_tweepy()

for i, row in df.iterrows():
    filename = "{}_{}".format(str(i).zfill(6), row["id"])

    out_file = "{}/{}".format(cache_dir, filename)

    followers = get_followers(api, row["id"], out_file)
    users_to_file(followers, out_file, follower_of=row["id"])

df = pd.DataFrame()

for dirent in os.listdir(cache_dir):
    path = os.path.join(cache_dir, dirent)
    if not os.path.isfile(path):
        continue

    file_df = pd.read_csv(path)
    df = pd.concat([df, file_df])

df.to_csv(
    "{}/{}_lvl2.csv".format(out_dir, in_file.split("/")[-1].split(".")[0]),
    index=False,
)

# import shutil
# shutil.rmtree(cache_dir)
