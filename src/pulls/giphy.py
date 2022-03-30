import json
import logging
import os
import requests

logger = logging.getLogger(__name__)


def get_gif(term):
    url = "https://api.giphy.com/v1/gifs/search?api_key="
    url += os.environ["GIPHY_API_KEY"]
    url += f"&q={term}"

    response = requests.get(url)
    gif = ""

    try:
        response.raise_for_status()
        logger.info(f"Successfully retrieved {url}")
    except requests.exceptions.HTTPError as e:
        logger.error(f"Failed to retrieve {url}")
        logger.error(e)
        logger.info("Setting gif to False")
        gif = False

    if gif is not False:
        gif_url = json.loads(response.content)
        gif_url = gif_url["data"][0]["images"]["original"]["url"]

        response = requests.get(gif_url)

        try:
            response.raise_for_status()
            logger.info(f"Successfully retrieved {gif_url}")
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to retrieve {gif_url}")
            logger.error(e)
            logger.info("Setting gif to False")
            gif = False

        gif = f"{term}.gif"
        # gif = os.path.join(tempfile.TemporaryDirectory().name, gif)

        try:
            logger.info(f"Writing gif to {gif}")
            with open(gif, "wb") as file:
                file.write(response.content)
        except Exception as e:
            logger.error(f"Failed to write {gif}")
            logger.error(e)
            gif = False

    return gif
