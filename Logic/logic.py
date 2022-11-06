#!/usr/bin/env python3
"""Wordle game service."""
from Repository.repository import WordsRepo
from Domain.guess_entity import Guess, LetterColour


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

    def check_guess(self, word: str) -> Guess:
        """
        Provide guess feedback.

        Returns a guess entity (see guess_entity from Domain for details).
        """
        freq = [0] * 26
        ans = [LetterColour.GRAY] * 5

        # Get frequency of letters in the secret guess
        for char in self.__secret_answer:
            freq[ord(char) - ord('A')] += 1

        # Check for green letters and remove them from freq
        for i in range(5):
            if word[i] == self.__secret_answer[i]:
                freq[ord(word[i]) - ord('A')] -= 1
                ans[i] = LetterColour.GREEN

        # Check for yellow letters
        for i in range(5):
            if ans[i] == LetterColour.GREEN:
                continue
            char = ord(word[i]) - ord('A')
            if freq[char] != 0:
                ans[i] = LetterColour.YELLOW
                freq[char] -= 1

        # Check if the whole word is green, and get a new word in that case
        for i in range(5):
            if ans[i] != LetterColour.GREEN:
                break
        else:
            self.__refresh_word()

        feedback = Guess(ans)
        return feedback
