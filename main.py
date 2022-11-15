#!/usr/bin/env python3
from Repository.default_repo import DefaultRepo
from Logic.game_logic import WordleServ
from Controller.cli_ui import CLI

repo = DefaultRepo()
serv = WordleServ(repo)
ui = CLI(serv)


def main():
    ui.run_ui()


if __name__ == "__main__":
    main()
