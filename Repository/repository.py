#!/usr/bin/env python3
"""Repository interface."""
from typing import Protocol


class WordsRepo(Protocol):
    """Repository interface. Should not follow CRUD."""

    def get_random_word(self) -> str:
        """Return an word from repo which was not previously returned."""
        ...

    def check_word(self, word: str) -> bool:
        """Return true if the word is found in the repo, false otherwise."""
        ...
