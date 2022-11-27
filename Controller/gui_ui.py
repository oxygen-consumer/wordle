from Domain.feedback_entity import Feedback, LetterColour
from Logic.game_logic import WordleServ

from Controller.ui_interface import UIInterface
import pygame
import pygame.freetype


class GUI(UIInterface):
    def __init__(self, service: WordleServ):
        """Define default constructor."""
        self.__service = service
        self.__current_score = 0
        self.__average_score = 0.0
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
        self.__font = pygame.freetype.SysFont("Lucida Console", 64, bold=True)
        self.__score_font = pygame.freetype.SysFont("Lucida Console", 20)
        self.__square_size = 80
        self.__start_rect_x = 80
        self.__start_rect_y = 80
        self.__print_from_line = 0
        self.__game_finished = False

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

        # from what guess to start displaying from (based on scrolling)
        if self.__current_score <= 5:
            list_to_show = self.__guess_list
            current_row = self.__current_score
        else:
            list_to_show = self.__guess_list[
                self.__print_from_line:self.__print_from_line + 5]
            current_row = 5

        # show the selected guesses
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

        # show the input text
        for column, char in enumerate(self.__current_word):
            x = self.__start_rect_x + (self.__square_size + 10) * column
            y = self.__start_rect_y + (self.__square_size + 10) * current_row
            square.topleft = (x, y)
            text_surface, text_rect = self.__font.render(
                char, self.__colors['WHITE'])
            text_rect.center = (x + 40, y + 40)
            self.__screen.blit(text_surface, text_rect)

        # show average score
        text_surface, text_rect = self.__score_font.render(
            "Average score: {:.2f}".format(
                self.__average_score), self.__colors['WHITE'])
        text_rect.topleft = (10, 10)
        self.__screen.blit(text_surface, text_rect)

        # show current score
        text_surface, text_rect = self.__score_font.render(
            "Current score: {0}".format(
                self.__current_score), self.__colors['WHITE'])
        text_rect.topright = (self.__width - 10, 10)
        self.__screen.blit(text_surface, text_rect)

    def __process_feedback(self, feedback: Feedback):
        """Processes the given feedback"""
        self.__current_word = ""
        self.__current_score += 1
        self.__average_score = feedback.average_score
        self.__guess_list.append(feedback)

        if self.__current_score < 5:
            self.__print_from_line = 0
        else:
            self.__print_from_line = self.__current_score - 5

        if feedback.colors == [LetterColour.GREEN] * 5:
            print(f"Guessed in {self.__current_score} guesses.")
            print(f"Average score: {feedback.average_score}.")
            self.__game_finished = True

    def __reset_game(self):
        """Clears screen"""
        self.__guess_list.clear()
        self.__current_score = 0
        self.__print_from_line = 0
        self.__current_word = ""
        self.__game_finished = False

    def __try_guess(self, guess: str) -> Feedback:
        return self.__service.check_guess(guess)

    def run_ui(self):
        # clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                self.__show_board()
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:

                        # press enter to restart game after it's finished
                        if self.__game_finished:
                            self.__reset_game()

                        # else, tries to submit the current word
                        else:
                            try:
                                feedback = self.__try_guess(
                                    self.__current_word)
                                self.__process_feedback(feedback)
                            except ValueError:
                                pass

                    # deleting characters with backspace
                    elif event.key == pygame.K_BACKSPACE:
                        if len(self.__current_word) > 0:
                            self.__current_word = self.__current_word[:-1]

                    # scrolling with up/down arrow keys
                    elif event.key == pygame.K_UP:
                        if self.__print_from_line != 0:
                            self.__print_from_line -= 1
                    elif event.key == pygame.K_DOWN:
                        if self.__current_score >= 6 and self.__print_from_line != self.__current_score - 5:
                            self.__print_from_line += 1

                    # scrolling with up/down arrow keys
                    elif not self.__game_finished \
                            and len(self.__current_word) != 5:
                        char = event.unicode.upper()
                        if char.isalpha():
                            self.__current_word += char
                pygame.display.update()
