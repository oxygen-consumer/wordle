#!/usr/bin/env python3
"""Wordle game service."""
from Repository.repository import WordsRepo
from typing import List


class WordleServ:
    """Manage wordle logic, provide guess feedback."""

    def __init__(self, repo: WordsRepo):
        """Initialize wordle logic with given repo."""
        self.__repo = repo

    def __refresh_word(self):
        # Try to get a new word from repo and set no_more_words accordingly
        try:
            self.__secret_answer = self.__repo.get_random_word()
            self.no_more_words = False
        except IndexError():
            self.no_more_words = True

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

        freq = [0] * 26
        ans = [0] * 5

        # Get frequency of letters in the secret guess
        for char in self.__secret_answer:
            freq[ord(char) - ord('A')] += 1

        # Check for green letters and remove them from freq
        for i in range(5):
            if word[i] == self.__secret_answer[i]:
                freq[ord(word[i]) - ord('A')] -= 1
                ans[i] = 2

        # Check for yellow letters
        for i in range(5):
            if ans[i] == 2:
                continue
            char = ord(word[i]) - ord('A')
            if freq[char] != 0:
                ans[i] = 1
                freq[char] -= 1

        # Check if the whole word is green, and get a new word in that case
        for i in range(5):
            if ans[i] != 2:
                break
        else:
            self.__refresh_word()

        return ans
