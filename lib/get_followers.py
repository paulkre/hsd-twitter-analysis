import tweepy
from . import users_to_file


def get_followers(api: tweepy.API, username, out_file=None) -> list[tweepy.User]:
    user = api.get_user(screen_name=username)

    followers: list[tweepy.User] = []
    try:
        for page in tweepy.Cursor(api.get_followers, user_id=user.id, count=200).pages():
            followers.extend(page)
            print("Number of followers downloaded: {}".format(len(followers)))
            if out_file:
                users_to_file(followers, out_file)
    except tweepy.TweepyException as e:
        print("Error during download:")
        print(e)

    return followers
