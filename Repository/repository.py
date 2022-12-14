#!/usr/bin/env python3
"""Repository interface."""
import abc


class WordsRepo(metaclass=abc.ABCMeta):
    """Repository interface. Should not follow CRUD."""

    @abc.abstractmethod
    def get_random_word(self) -> str:
        """Return an word from repo which was not previously returned."""
        ...

    @abc.abstractmethod
    def check_word(self, word: str) -> bool:
        """Return true if the word is found in the repo, false otherwise."""
        ...

    @abc.abstractmethod
    def get_words_list(self) -> list[str]:
        """Return a sorted list of all the possible words."""
        ...
