#!/usr/bin/env python
"""Define helper classes to provide a more organized feedback from service."""
from enum import Enum
from dataclasses import dataclass
from typing import List


class LetterColour(Enum):
    """
    Represents the colours of the letters in the guess.

    GRAY means a letter isn't in the guess
    YELLOW means a letter is in the guess but not in the correct position
    GREEN means a letter is in the correct position
    """

    GRAY = 0
    YELLOW = 1
    GREEN = 2


@dataclass
class Feedback:
    """
    Store the feedback returned by the game logic.

    * colors: this stores the feedback of the guess based on letter colors;
    * no_more_words: this is set to True when the game has used all the words
    from repository aka player guessed all the words;
    * current_scores: this represents the number of tries for the current word;
    * average_score: this represents the average number of tries for the
    previous words until the word was guessed.
    """

    colors: List[LetterColour]
    no_more_words: bool
    current_score: int
    average_score: float
