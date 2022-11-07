#!/usr/bin/env python3
"""Repository interface."""
import abc


class WordsRepo(abc.ABC):
    """Repository interface. Should not follow CRUD."""

    @abc.abstractmethod
    def get_random_word(self) -> str:
        """Return an word from repo which was not previously returned."""
        ...

    @abc.abstractmethod
    def check_word(self, word: str) -> bool:
        """Return true if the word is found in the repo, false otherwise."""
        ...
