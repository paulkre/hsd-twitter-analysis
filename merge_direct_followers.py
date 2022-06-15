import os
import pandas as pd

out_dir = "data"
in_dir = "{}/followers".format(out_dir)
dfs = []

for dirent in os.listdir(in_dir):
    path = os.path.join(in_dir, dirent)

    if not os.path.isfile(path) or not dirent.endswith(".csv") or "_lvl2" in dirent or "_friends" in dirent:
        continue

    print(dirent)
    dfs.append(pd.read_csv(path, lineterminator='\n'))

df_hochschul_friends = pd.read_csv(in_dir + "/hochschulen_friends.csv")
df_hochschul_friends = df_hochschul_friends.rename(columns={"friend_of": "follower_of"})
df = pd.concat(dfs)
df = pd.concat([df, df_hochschul_friends])

df[["id", "follower_of"]].sort_values("id", ascending=True).to_csv(
    "{}/direct_followings.csv".format(out_dir),
    index=False,
)

static_df = pd.read_csv("{}/static_users.csv".format(out_dir))

static_df['follower_of'] = static_df['id']

pd.concat([
    static_df,
    df,
    df_hochschul_friends,
]).drop_duplicates(["id"]).to_csv(
    "{}/direct_users.csv".format(out_dir),
    index=False,
)