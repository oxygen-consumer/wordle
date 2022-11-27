from multiprocessing import Queue
from Domain.feedback_entity import LetterColour
import math


class WordleSolver:
    """
    Creates the solver and get the word list and connect with the queues
    from the IPC.
    """

    def __init__(
        self,
        word_list: list[str],
        guess_queue: Queue,
        feedback_queue: Queue,
    ) -> None:
        self.__words = word_list
        self.__guess_queue = guess_queue
        self.__feedback_queue = feedback_queue

    def __gen_key(self, word: str, possible_ans: str) -> str:
        """
        Generates the key for the dictionary, the key being the feedback we
        would get if the secret word were possible_ans.
        """
        case = ["0"] * 5

        for i, c in enumerate(word):
            if c == possible_ans[i]:
                case[i] = "2"
            elif c in possible_ans:
                case[i] = "1"

        return "".join(case)

    def __entropy(self, word: str) -> float:
        """Calculates the entropy of a word in __possible_answers"""
        entropy = 0.0
        fr = dict()

        for possible_ans in self.__possible_answers:
            key = self.__gen_key(word, possible_ans)

            if key in fr.keys():
                fr[key] += 1
            else:
                fr[key] = 1

        for key in fr.keys():
            entropy += fr[key] * math.log2(
                len(self.__possible_answers) / fr[key]
            )

        entropy /= len(self.__possible_answers)
        return entropy

    def __get_best_entropy(self) -> str:
        """
        Gets the word with the biggest entropy from the __possible_answers.
        """
        max_entropy = -1
        ans = ""

        for word in self.__possible_answers:
            entropy = self.__entropy(word)

            if entropy > max_entropy:
                max_entropy = entropy
                ans = word

        return ans

    def __check_match(self, word) -> bool:
        """
        Checks if the new guess matches the requirements from the feedback.
        """
        if self.__previous_word == word:
            return False

        for i, color in enumerate(self.__current_feedback):
            if color == LetterColour.GREEN:
                if word[i] != self.__previous_word[i]:
                    return False

            elif color == LetterColour.YELLOW:
                if (
                    not self.__previous_word[i] in word
                    or self.__previous_word[i] == word[i]
                ):
                    return False

            else:
                if self.__previous_word[i] in word:
                    return False

        return True

    def __clean_possible_answers(self) -> None:
        """Get rid of the words that cannot be the correct answer"""
        new_pos_ans = set()
        for word in self.__possible_answers:
            if self.__check_match(word):
                new_pos_ans.add(word)

        self.__possible_answers = new_pos_ans

    def __process_feedback(self) -> str:
        """Process the provided feedback and return a new guess."""
        if self.__current_feedback == [LetterColour.GREEN] * 5:
            self.__possible_answers = set(self.__words)

            # HACK:
            # we found out that "TAREI" is the best word in the default repo
            # so we hardcoded it to save some running time (from 6h to 10m).

            # FIXME:
            # this behaviour should be changed to make the bot compatible with
            # other custom word lists, maybe we should determine it when the
            # bot starts.
            self.__previous_word = "TAREI"
        else:
            self.__clean_possible_answers()
            self.__previous_word = self.__get_best_entropy()

        return self.__previous_word

    def runner(self) -> None:
        """
        Run the bot and does input/ouptut on the provided queues.

        This function should be a subprocess!!!
        """
        while True:
            self.__current_feedback = self.__feedback_queue.get()
            guess = self.__process_feedback()
            self.__guess_queue.put(guess)
