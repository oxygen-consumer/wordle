#!/usr/bin/env python3
"""Defines the class for words repo."""
import requests
import random
import bisect


class WordsRepo:
    """Keeps a list of words and manages them."""

    def __init__(self):
        """Initialize words repo."""
        self.__url = "https://cs.unibuc.ro/~crusu/asc/cuvinte_wordle.txt"
        self.__load_repo()

        self.__current_word = 0

    def __load_repo(self):
        r = requests.get(self.__url)
        self.__sorted_data = r.text.splitlines()[:-1]

        self.__data = self.__sorted_data.copy()
        random.shuffle(self.__data)

    def get_random_word(self) -> str:
        """Return an word from repo which was not previously returned."""
        if self.__current_word >= len(self.__data):
            raise IndexError("No more words in repository")

        self.__current_word += 1
        return self.__data[self.__current_word - 1]

    def check_word(self, word: str) -> bool:
        """Return true if the word is found in the repo, false otherwise."""
        i = bisect.bisect_left(self.__sorted_data, word)

        if i != len(self.__sorted_data) and self.__sorted_data[i] == word:
            return True
        return False
