from enum import Enum
from dataclasses import dataclass
from typing import List


class LetterColour(Enum):
    """
    Represents the colours of the letters in the guess:
    GRAY means a letter isn't in the guess
    YELLOW means a letter is in the guess but not in the correct position
    GREEN means a letter is in the correct position
    """

    GRAY = 0
    YELLOW = 1
    GREEN = 2


@dataclass
class Guess:
    """Stores the feedback of a guess represented by a list of colours"""
    feedback: List[LetterColour]
