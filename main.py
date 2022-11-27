#!/usr/bin/env python3
import time
from Controller.gui_ui import GUI
from Controller.cli_ui import CLI
from Logic.game_logic import WordleServ
from Repository.default_repo import DefaultRepo
from Repository.human_repo import HumanRepo
from Controller.bot_handler import BotHandler
import argparse


def main():
    parser = argparse.ArgumentParser(description="Wordle Bot")
    parser.add_argument("--human", action="store_true", dest="human")
    parsed_args = parser.parse_args()

    if parsed_args.human:
        print("Downloading word list...")
        repo = HumanRepo()
        print("Initializing game...")
        serv = WordleServ(repo, buggy=False)
        ui = GUI(serv)
    else:
        print("Downloading word list...")
        repo = DefaultRepo()
        print("Initializing game...")
        serv = WordleServ(repo, gen_files=True)
        print("Starting the bot...")
        bot_handler = BotHandler(repo)
        ui = CLI(serv, bot_handler)

    print("Finished loading. Running...")
    start_time = time.perf_counter()
    ui.run_ui()
    end_time = time.perf_counter()
    if not parsed_args.human:
        print(f"Finished guessing all the words in {end_time - start_time}s.")


if __name__ == "__main__":
    main()
