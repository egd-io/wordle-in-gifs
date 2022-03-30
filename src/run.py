import logging

from src.pulls.giphy import get_gif
from src.pulls.wordle import get_answer, get_wordlist
from src.pushes.twitter import push_gif

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

if __name__ == "__main__":
    wordlist = get_wordlist()
    answer = get_answer(wordlist)
    gif = get_gif(answer)
    push_gif(gif)
