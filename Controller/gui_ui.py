from Domain.feedback_entity import Feedback, LetterColour
from Logic.game_logic import WordleServ

from Controller.bot_handler import BotHandler
from Controller.ui_interface import UIInterface
import pygame
import pygame.freetype
import time


class GUI(UIInterface):
    def __init__(self, service: WordleServ, bot_handler: BotHandler):
        """Define default constructor."""
        self.__service = service
        self.__bot_handler = bot_handler
        self.__current_score = 0
        self.__guess_list = []
        self.__init_window()
        self.__init_game_settings()
        self.__current_word = ''

    def __init_window(self) -> None:
        pygame.init()
        self.__width, height = 600, 650
        self.__screen = pygame.display.set_mode((self.__width, height))
        pygame.display.set_caption("Wordle GUI")

    def __init_game_settings(self):
        self.__colors = {
            LetterColour.GRAY: "#787c7f",
            LetterColour.YELLOW: "#c8b653",
            LetterColour.GREEN: "#6ca965",
            "WHITE": "#ffffff",
        }
        self.__font = pygame.freetype.SysFont("Arial", 64, bold=True)
        self.__score_font = pygame.freetype.SysFont("Arial", 28)
        self.__square_size = 80
        self.__start_rect_x = 80
        self.__start_rect_y = 80

    def __show_board(self):
        self.__screen.fill((50, 50, 50))
        square = pygame.Rect(0, 0, self.__square_size, self.__square_size)

        # draw square outlines
        for row in range(6):
            for column in range(5):
                x = self.__start_rect_x + (self.__square_size + 10) * column
                y = self.__start_rect_y + (self.__square_size + 10) * row
                square.topleft = (x, y)
                pygame.draw.rect(
                    self.__screen, self.__colors['WHITE'], square, 2)

        # from what guess to start printing from (based on scrolling)
        if self.__current_score <= 5:
            list_to_show = self.__guess_list
            # current_row = self.__current_score
        else:
            list_to_show = self.__guess_list[-6:]
            # current_row = 5

        # print the selected guesses
        for row, feedback in enumerate(list_to_show):
            for column, (char_w, char_f) in enumerate(
                    zip(feedback.guess, feedback.colors)):
                x = self.__start_rect_x + (self.__square_size + 10) * column
                y = self.__start_rect_y + (self.__square_size + 10) * row
                square.topleft = (x, y)
                pygame.draw.rect(self.__screen, self.__colors[char_f], square)
                text_surface, text_rect = self.__font.render(
                    char_w, self.__colors['WHITE'])
                text_rect.center = (x + 40, y + 40)
                self.__screen.blit(text_surface, text_rect)

        # print average/current scores
        try:
            text_surface, text_rect = self.__score_font.render(
                "Average score: {:.2f}".format(
                    self.__guess_list[-1].average_score), self.__colors['WHITE'])
            text_rect.topleft = (10, 10)
            self.__screen.blit(text_surface, text_rect)
        except IndexError:
            pass

        text_surface, text_rect = self.__score_font.render(
            "Current score: {:.2f}".format(
                self.__current_score), self.__colors['WHITE'])
        text_rect.topright = (self.__width - 10, 10)
        self.__screen.blit(text_surface, text_rect)

    def __process_feedback(self, feedback: Feedback):
        self.__current_score += 1
        self.__guess_list.append(feedback)

        if feedback.colors == [LetterColour.GREEN] * 5:
            print(f"Guessed in {self.__current_score} guesses.")
            print(f"Average score: {feedback.average_score}.")
            self.__current_score = 0
            self.__guess_list.clear()

        self.__bot_handler.give_feedback_to_bot(feedback.colors)

    def __try_guess(self, guess: str) -> Feedback:
        return self.__service.check_guess(guess)

    def __handle_input(self) -> str:
        return self.__bot_handler.get_bot_guess()

    def run_ui(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                clock.tick(30)
                if event.type == pygame.QUIT:
                    running = False
                    break

                self.__show_board()
                guess = self.__handle_input()
                feedback = self.__try_guess(guess)
                self.__process_feedback(feedback)

                if feedback.no_more_words:
                    self.__bot_handler.stop_bot()
                    running = False
                    break
                pygame.display.update()
                pygame.time.wait(100)
