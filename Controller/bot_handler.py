#!/usr/bin/env python3
"""BotHandler class."""
from Domain.feedback_entity import LetterColour
from Repository.repository import WordsRepo
from Logic.solver import WordleSolver
from multiprocessing import Process, Queue


class BotHandler:
    def __init__(self, repo: WordsRepo) -> None:
        self.__words = repo.get_words_list()

        # queues used for communicating with the bot subprocess
        self.__guess_queue = Queue()
        self.__feedback_queue = Queue()

        # run the bot as a subprocess
        self.__solver = WordleSolver(
            self.__words, self.__guess_queue, self.__feedback_queue)
        self.__bot = Process(target=self.__solver.runner)
        self.__bot.start()

        # we need to give the bot something to work with
        self.__feedback_queue.put([LetterColour.GREEN] * 5)

    def get_bot_guess(self) -> str:
        """Ask the bot for its next guess."""
        guess = self.__guess_queue.get()
        return guess

    def give_feedback_to_bot(self, feedback: list[LetterColour]) -> None:
        """Tell the bot how the good its answer was."""
        self.__feedback_queue.put(feedback)

    def stop_bot(self) -> None:
        """Kill bot subprocess."""
        self.__bot.kill()
