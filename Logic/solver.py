from multiprocessing import Queue
from Domain.feedback_entity import LetterColour


class WordleSolver:
    def __init__(
            self,
            word_list: list[str],
            guess_queue: Queue,
            feedback_queue: Queue) -> None:
        self.__words = word_list
        self.__guess_queue = guess_queue
        self.__feedback_queue = feedback_queue

    def __process_feedback(self, feedback: list[LetterColour]) -> str:
        """Process the provided feedback and return a new guess."""
        return "TAREI"

    def runner(self) -> None:
        """
        Run the bot and does input/ouptut on the provided queues.

        This function should be a subprocess!!!
        """
        while True:
            feedback = self.__feedback_queue.get()
            guess = self.__process_feedback(feedback)
            self.__guess_queue.put(guess)
