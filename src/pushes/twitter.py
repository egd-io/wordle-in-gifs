import logging
import os
import tweepy

from datetime import datetime

logger = logging.getLogger(__name__)


def push_gif(path):
    ck = os.environ.get("TWITTER_CONSUMER_KEY")
    cs = os.environ.get("TWITTER_CONSUMER_SECRET")
    at = os.environ.get("TWITTER_ACCESS_TOKEN")
    ats = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuthHandler(ck, cs)
    auth.set_access_token(at, ats)
    api = tweepy.API(auth)

    media = api.media_upload(path)
    delta = datetime.now() - datetime(2021, 6, 19)
    text = f"Wordle #{delta.days} in a GIF:"

    try:
        logger.info(f"Posting {path}")
        api.update_status(status=text, media_ids=[media.media_id])
    except Exception as e:
        logger.error("Failed to post tweet")
        logger.error(e)
