#!/usr/bin/env python3
"""Wordle game service."""
from repository import WordsRepo
from typing import List


class WordleServ:
    """Manage wordle logic, provide guess feedback."""

    def __init__(self, repo: WordsRepo):
        """Initialize wordle logic with given repo."""
        self.__repo = repo
        self.__secret_answer = self.__repo.get_random_word()

    def check_guess(self, word: str) -> List[int]:
        """
        Provide guess feedback.

        Returns a list of 5 integers representing each letter like so:
        0 - letter not present in the secret word
        1 - letter present in the secret word but not in the current position
        2 - letter guessed correctly
        """
        # FIXME: maybe should make a class for the guess which also should use
        # enum
        #
        # TODO: implement this

        pass
