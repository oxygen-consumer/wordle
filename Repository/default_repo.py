#!/usr/bin/env python3
"""Defines the class for words repo."""
import bisect
import random

import requests

from Repository.repository import WordsRepo


class DefaultRepo(WordsRepo):
    """Keeps a list of words and manages them."""

    def __init__(self):
        """Initialize words repo."""
        self.__url = "https://cs.unibuc.ro/~crusu/asc/cuvinte_wordle.txt"
        self.__load_repo()

        self.__current_word = 0

    def __load_repo(self):
        # HACK: the request returns the words in a sorted order
        # should we sort it just in case?
        r = requests.get(self.__url)
        # there is an empty line at the end so we remove it by :-1
        self.__sorted_data = r.text.splitlines()[:-1]

        # __data should always be shuffled, see get_random_word
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
