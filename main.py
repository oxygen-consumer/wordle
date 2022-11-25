#!/usr/bin/env python3
from Controller.cli_ui import CLI
from Logic.game_logic import WordleServ
from Repository.default_repo import DefaultRepo
from Controller.bot_handler import BotHandler

def main():
    # TODO: we should define some arguments to change programs behaviour
    repo = DefaultRepo()
    serv = WordleServ(repo)
    bot_handler = BotHandler(repo)
    ui = CLI(serv, bot_handler)
    ui.run_ui()


if __name__ == "__main__":
    main()
