#!/usr/bin/env python3
"""Wordle game service."""
from Domain.feedback_entity import Feedback, LetterColour
from Repository.repository import WordsRepo


class WordleServ:
    """Manage wordle logic, provide guess feedback."""

    def __init__(self, repo: WordsRepo, buggy: bool = True):
        """Initialize wordle logic with given repo."""
        self.__repo = repo
        self.__buggy = buggy
        self.__init_score()
        self.__refresh_word()
        # HACK:
        # reset previous_plays after initial refresh_word call
        # which calls update_score and increases the play count to 1
        # when it should be 0, since it's the first game
        self.__previous_plays = 0

    def __init_score(self):
        self.__current_score = 0
        self.__avg_score = 0.0
        self.__previous_plays = 0

    def __update_score(self, reset=False):
        """
        Update score variables.

        If reset is set to True, then set the current score to 0 and
        recalculate average score.
        """
        if reset:
            self.__avg_score = (
                self.__avg_score
                - self.__avg_score / (self.__previous_plays + 1)
                + self.__current_score / (self.__previous_plays + 1)
            )

            self.__current_score = 0
            self.__previous_plays += 1
        else:
            self.__current_score += 1

    def __refresh_word(self):
        # Try to get a new word from repo and set no_more_words accordingly
        try:
            self.__secret_answer = self.__repo.get_random_word()
            self.__no_more_words = False
        except IndexError:
            self.__no_more_words = True

        # Reset current score and update average score
        self.__update_score(True)

    def __buggy_free_behaviour(self, word: str) -> list[LetterColour]:
        freq = [0] * 26
        ans = [LetterColour.GRAY] * 5

        # Get frequency of letters in the secret guess
        for char in self.__secret_answer:
            freq[ord(char) - ord("A")] += 1

        # Check for green letters and remove them from freq
        for i in range(5):
            if word[i] == self.__secret_answer[i]:
                freq[ord(word[i]) - ord("A")] -= 1
                ans[i] = LetterColour.GREEN

        # Check for yellow letters
        for i in range(5):
            if ans[i] == LetterColour.GREEN:
                continue
            char = ord(word[i]) - ord("A")
            if freq[char] != 0:
                ans[i] = LetterColour.YELLOW
                freq[char] -= 1

        return ans

    def __buggy_behaviour(self, word: str) -> list[LetterColour]:
        ans = [LetterColour.GRAY] * 5

        for i in range(5):
            if word[i] == self.__secret_answer[i]:
                ans[i] = LetterColour.GREEN
            elif word[i] in self.__secret_answer:
                ans[i] = LetterColour.YELLOW

        return ans

    def check_guess(self, word: str) -> Feedback:
        """
        Provide guess feedback.

        Returns a guess entity (see guess_entity from Domain for details).
        """
        # Check if a word is present in the repo
        if not self.__repo.check_word(word):
            raise ValueError("Not a word.")

        # Increase current score
        self.__update_score()

        # Get the answer based on the given behaviour
        ans = []
        if self.__buggy:
            ans = self.__buggy_behaviour(word)
        else:
            ans = self.__buggy_free_behaviour(word)

        # Check if the whole word is green, and get a new word in that case
        for i in range(5):
            if ans[i] != LetterColour.GREEN:
                break
        else:
            self.__refresh_word()

        # Construct the feedback entity and return it
        feedback = Feedback(ans, word, self.__no_more_words, self.__avg_score)
        return feedback
