#!/usr/bin/env python3
"""UI interface."""
import abc

from Logic.game_logic import WordleServ

from Controller.bot_handler import BotHandler


class UIInterface(metaclass=abc.ABCMeta):
    """UI Interface."""

    @abc.abstractmethod
    def __init__(self, service: WordleServ, bot_handler: BotHandler = None):
        """Define default constructor."""
        self.__service = service
        self.__bot_handler = bot_handler

    @abc.abstractmethod
    def run_ui(self):
        """Run the UI."""
        ...
