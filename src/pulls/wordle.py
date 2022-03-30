import ast
import logging
import re
import requests

from bs4 import BeautifulSoup
from datetime import datetime

logger = logging.getLogger(__name__)


def get_answer(answers):
    delta = datetime.now() - datetime(2021, 6, 19)

    return answers[delta.days]


def get_wordlist():
    wordlist = ""
    base_url = "https://www.nytimes.com/games/wordle/"

    response = requests.get(f"{base_url}index.html")

    try:
        response.raise_for_status()
        logger.info(f"Successfully retrieved {base_url}index.html")
    except requests.exceptions.HTTPError as e:
        logger.error(f"Failed to retrieve {base_url}index.html")
        logger.error(e)
        logger.info("Setting wordlist to False")
        wordlist = False

    if wordlist is not False:
        soup = BeautifulSoup(response.content, "html.parser")
        tags = soup.find_all("script")

        for tag in tags:
            if "src" in tag.attrs:
                if "main" in tag.attrs["src"] and ".js" in tag.attrs["src"]:
                    script = tag.attrs["src"]

        response = requests.get((f"{base_url}{script}"))

        try:
            response.raise_for_status()
            logger.info(f"Successfully retrieved {base_url}{script}")
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to retrieve {base_url}{script}")
            logger.error(e)
            logger.info("Setting wordlist to False")
            wordlist = False

        wordlist = re.search("Ma=[^O]+", response.text)
        wordlist = re.search(r"\[(.*)\]", wordlist.group())
        words = ""
        for word in wordlist.group():
            words += word

        wordlist = ast.literal_eval(words)

    return wordlist
