#!/usr/bin/env python3
import time
from Controller.cli_ui import CLI
from Logic.game_logic import WordleServ
from Repository.default_repo import DefaultRepo
from Controller.bot_handler import BotHandler


def main():
    print("Downloading word list...")
    repo = DefaultRepo()

    print("Starting the bot...")
    bot_handler = BotHandler(repo)

    print("Initializing game...")
    serv = WordleServ(repo)
    # TODO: GUI, CLI should be used when --cli is passed
    ui = CLI(serv, bot_handler)
    
    print("Finisihed loading... Running...")
    start_time = time.perf_counter()
    ui.run_ui()
    end_time = time.perf_counter()
    print(f"Finished guessing all the words in {start_time - end_time}.")


if __name__ == "__main__":
    main()
