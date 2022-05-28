import os
import tweepy

from dotenv import load_dotenv
load_dotenv()


def initialize_tweepy():
    auth = tweepy.OAuth1UserHandler(
        os.getenv("TWITTER_CONSUMER_KEY"),
        os.getenv("TWITTER_CONSUMER_SECRET"),
        os.getenv("TWITTER_ACCESS_KEY"),
        os.getenv("TWITTER_ACCESS_SECRET"),
    )

    return tweepy.API(auth, wait_on_rate_limit=True)
