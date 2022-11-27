#!/usr/bin/env python3
import time
from Controller.gui_ui import GUI
from Controller.cli_ui import CLI
from Logic.game_logic import WordleServ
from Repository.default_repo import DefaultRepo
from Controller.bot_handler import BotHandler
import argparse


def main():
    parser = argparse.ArgumentParser(description="Wordle Bot")
    parser.add_argument(
        "--gui",
        action="store_true",
        dest='gui')
    parsed_args = parser.parse_args()

    print("Downloading word list...")
    repo = DefaultRepo()

    print("Starting the bot...")
    bot_handler = BotHandler(repo)

    print("Initializing game...")
    serv = WordleServ(repo)

    if parsed_args.gui:
        ui = GUI(serv, bot_handler)
    else:
        ui = CLI(serv, bot_handler)

    print("Finisihed loading... Running...")
    start_time = time.perf_counter()
    ui.run_ui()
    end_time = time.perf_counter()
    print(f"Finished guessing all the words in {end_time - start_time}.")


if __name__ == "__main__":
    main()
