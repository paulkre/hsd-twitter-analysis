import tweepy
from . import users_to_file


def get_followers(api: tweepy.API, user_id, out_file=None) -> list[tweepy.User]:
    followers: list[tweepy.User] = []
    try:
        for page in tweepy.Cursor(api.get_followers, user_id=user_id, count=200).pages():
            followers.extend(page)
            if out_file:
                users_to_file(followers, out_file, follower_of=user_id)
    except tweepy.TweepyException as e:
        print("Error during download:")
        print(e)

    return followers
