import os
import pandas as pd

out_dir = "data"
in_dir = "{}/followers".format(out_dir)
dfs = []

for dirent in os.listdir(in_dir):
    path = os.path.join(in_dir, dirent)
    if not os.path.isfile(path) or not dirent.endswith(".csv"):
        continue

    dfs.append(pd.read_csv(path, lineterminator='\n'))

df = pd.concat(dfs)

df[["id", "follower_of"]].sort_values("id", ascending=True).to_csv(
    "{}/followings.csv".format(out_dir),
    index=False,
)

pd.concat([
    pd.read_csv("{}/static_users.csv".format(out_dir)),
    df.drop(["follower_of"], axis=1),
]).drop_duplicates(["id"]).to_csv(
    "{}/users.csv".format(out_dir),
    index=False,
)
