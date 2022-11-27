"""
A sane list for human players
"""
import requests
import re
import random
import bisect

from Repository.repository import WordsRepo


class HumanRepo(WordsRepo):
    def __init__(self) -> None:
        # this file was taken from wordle.ro
        # all the credits go to the author of the site
        self.__url = "https://gist.githubusercontent.com/oxygen-consumer/285e19dae5042b4b8fa8985428a128eb/raw/030238442893c445431e61dc8f96589fe25e6951/wordle.ro%2520wordlist"
        self.__load_repo()

        self.__current_word = 0

    def __load_repo(self):
        r = requests.get(self.__url)

        # clean up the request
        dirty_data = r.text.splitlines()[1:-1]
        data = set()
        for word in dirty_data:
            data.add(re.sub(r"[^a-zA-Z]", "", word).upper())

        self.__sorted_data = list(data)
        self.__sorted_data = sorted(self.__sorted_data)
        self.__data = self.__sorted_data.copy()
        random.shuffle(self.__data)

    def get_random_word(self) -> str:
        """Return an word from repo which was not previously returned."""
        if self.__current_word >= len(self.__data):
            raise IndexError("No more words in repository")

        # __data is always shuffled so we just need to get next word from it
        self.__current_word += 1
        return self.__data[self.__current_word - 1]

    def check_word(self, word: str) -> bool:
        """Return true if the word is found in the repo, false otherwise."""
        # We do a binary search for the word
        i = bisect.bisect_left(self.__sorted_data, word)

        # Then we verify if it was found
        if i != len(self.__sorted_data) and self.__sorted_data[i] == word:
            return True
        return False

    def get_words_list(self) -> list[str]:
        """Return a sorted list of all the possible words."""
        return self.__sorted_data
