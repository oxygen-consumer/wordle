#!/usr/bin/env python3
"""Simple CLI UI."""
import colorama
from Domain.feedback_entity import Feedback, LetterColour
from Logic.game_logic import WordleServ

from Controller.bot_handler import BotHandler
from Controller.ui_interface import UIInterface


class CLI(UIInterface):
    """Simple CLI UI."""

    def __init__(self, service: WordleServ, bot_handler: BotHandler):
        """Define default constructor."""
        self.__service = service
        self.__bot_handler = bot_handler
        self.__current_score = 0
        colorama.init(autoreset=True)

    def __process_feedback(self, feedback: Feedback):
        colors = {
            LetterColour.GRAY: colorama.Back.BLACK,
            LetterColour.YELLOW: colorama.Back.YELLOW,
            LetterColour.GREEN: colorama.Back.GREEN,
        }

        for letter, color in zip(feedback.guess, feedback.colors):
            print(colors[color] + letter, end="")
        print()

        self.__current_score += 1

        if feedback.colors == [LetterColour.GREEN] * 5:
            print(f"Guessed in {self.__current_score} guesses.")
            print(f"Average score: {feedback.average_score}.")
            self.__current_score = 0

        self.__bot_handler.give_feedback_to_bot(feedback.colors)

    def __try_guess(self, guess: str) -> Feedback:
        return self.__service.check_guess(guess)

    def __get_input(self) -> str:
        return self.__bot_handler.get_bot_guess()

    def run_ui(self):
        """Run the UI."""
        while True:
            guess = self.__get_input()

            feedback = Feedback
            try:
                feedback = self.__try_guess(guess)
            except ValueError:
                print("Not a word!")
                continue

            self.__process_feedback(feedback)

            if feedback.no_more_words:
                self.__bot_handler.stop_bot()
                break
